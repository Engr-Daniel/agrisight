"""Known-truth median bounds and validation, synthetic fixtures only."""

import hashlib
import io
import itertools
import json
import math
import sqlite3
import statistics
import zipfile

import pytest

pd = pytest.importorskip("pandas")

from agrisight import nass02


def frame(areas):
    return pd.DataFrame({"hhid": [1]*len(areas),
                         "s02_plotRoster__id": list(range(1, len(areas)+1)),
                         "s02_q15": [1]*len(areas), "s02_q16a": areas})


@pytest.mark.parametrize("areas,observed,low,high,status", [
    ([1,3,5,7,None],4,3,5,'bounded'),
    ([1,3,5,None],3,2,4,'bounded'),
    ([1,3,5],3,3,3,'bounded'),
    ([1,3,5,7],4,4,4,'bounded'),
    ([None,None],None,0,None,'unbounded'),
    ([1,None],1,0.5,None,'unbounded'),
    ([0,0,None],0,0,0,'bounded'),
    ([],None,None,None,'undefined'),
])
def test_known_truth(areas, observed, low, high, status):
    result=nass02.calculate(frame(areas))['estimates']
    assert result['observed_only_median_m2']==observed
    assert result['full_roster_lower_m2']==low
    assert result['full_roster_upper_m2']==high
    assert result['status']==status


def test_tagged_missing_order_invariance_and_no_mutation():
    data=frame([1,3,5,7,pd.io.stata.StataMissingValue(102)])
    before=data.copy(deep=True)
    assert nass02.calculate(data)==nass02.calculate(data.iloc[::-1])
    assert nass02.calculate(data)['estimates']['missing_areas']==1
    pd.testing.assert_frame_equal(data,before)


@pytest.mark.parametrize('area', [-1,math.inf,-math.inf])
def test_invalid_area_is_not_silently_excluded(area):
    with pytest.raises(ValueError,match='Negative/nonfinite'):
        nass02.calculate(frame([area]))


@pytest.mark.parametrize('area', ['1',True])
def test_wrong_area_type_fails(area):
    with pytest.raises(TypeError,match='numeric'):
        nass02.calculate(frame([area]))


def test_key_status_and_schema_guards():
    data=frame([1,3])
    data.loc[1,'s02_plotRoster__id']=1
    with pytest.raises(ValueError,match='plot key'):
        nass02.calculate(data)
    data=frame([1])
    data.loc[0,'hhid']=None
    with pytest.raises(ValueError,match='plot key'):
        nass02.calculate(data)
    data=frame([1])
    data.loc[0,'s02_q15']=9
    with pytest.raises(ValueError,match='plot status'):
        nass02.calculate(data)
    with pytest.raises(ValueError,match='columns'):
        nass02.calculate(frame([1]).drop(columns='s02_q16a'))


def test_sql_rejects_negative_and_duplicate_keys():
    with sqlite3.connect(':memory:') as db:
        db.executescript(nass02.sql_model())
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("INSERT INTO stg_nass_plot_area VALUES('A','1',-1)")
        db.execute("INSERT INTO stg_nass_plot_area VALUES('A','1',NULL)")
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("INSERT INTO stg_nass_plot_area VALUES('A','1',2)")


def test_large_finite_areas_do_not_overflow_the_median():
    result=nass02.calculate(frame([1e308,1e308]))['estimates']
    assert result['full_roster_lower_m2']==1e308
    assert result['full_roster_upper_m2']==1e308


def test_complete_source_to_private_bounds(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data=frame([1,3,5,7,None])
    data['areaAcresPlot']=0
    stream=io.BytesIO()
    data.to_stata(stream,write_index=False,version=114,variable_labels={
        's02_q16a':'Area of plot in square meter', 'areaAcresPlot':'Plot area in Acres'})
    source=tmp_path/'synthetic.zip'
    with zipfile.ZipFile(source,'w') as archive:
        archive.writestr('3_Plot_mainSeason.dta',stream.getvalue())
    monkeypatch.setattr(nass02,'ARCHIVE_SHA256',hashlib.sha256(source.read_bytes()).hexdigest())
    (tmp_path/'requirements').mkdir()
    (tmp_path/'requirements/e1.lock').write_text('# synthetic fixture lock\n')
    output=tmp_path/'reports/private/test.json'
    nass02.run(source,output)
    result=json.loads(output.read_text())
    assert result['estimates']['full_roster_lower_m2']==3
    assert result['estimates']['full_roster_upper_m2']==5
    assert result['companion_audit']['companion_zero_when_m2_missing']==1
    assert result['companion_audit']['companion_zero_when_m2_positive']==4
    assert result['definition']['corrections'].startswith('none')


def test_output_and_source_guards(tmp_path,monkeypatch):
    monkeypatch.chdir(tmp_path)
    source=tmp_path/'bad.zip'
    source.write_bytes(b'not an acquired source')
    with pytest.raises(ValueError,match='reports/private'):
        nass02.run(source,tmp_path/'public.json')
    with pytest.raises(ValueError,match='hash'):
        nass02.run(source,tmp_path/'reports/private/test.json')


@pytest.mark.parametrize('known,missing', [([0,2],1),([0,2,2],1),([1,3,5],2),
                                         ([1,3,5,7],3),([0,0],1)])
def test_bounds_match_exhaustive_small_completions(known,missing):
    result=nass02.calculate(frame(known+[None]*missing))['estimates']
    candidates=[statistics.median(known+list(completion))
                for completion in itertools.product([0,1,2,3,5,7,10],repeat=missing)]
    assert min(candidates)==result['full_roster_lower_m2']
    if result['status']=='bounded':
        assert max(candidates)==result['full_roster_upper_m2']


def test_plot_id_is_not_globally_unique():
    data=frame([1,3])
    data['hhid']=[1,2]
    data['s02_plotRoster__id']=[1,1]
    assert nass02.calculate(data)['estimates']['total_plots']==2
