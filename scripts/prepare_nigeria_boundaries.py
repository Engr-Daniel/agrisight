"""Prepare licensed, public state boundaries from reviewed local downloads (no survey data)."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from agrisight.geographic_coverage import STATE_NAMES

SOURCE_URL = ("https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/"
              "NGA/ADM1/geoBoundaries-NGA-ADM1_simplified.geojson")


def prepare(source: Path, metadata: Path, output: Path) -> None:
    raw = source.read_bytes()
    data, meta = json.loads(raw), json.loads(metadata.read_bytes())
    if (meta["boundaryID"] != "NGA-ADM1-27671186" or meta["boundaryYearRepresented"] != "2022"
            or meta["boundaryLicense"] != "Creative Commons Attribution 4.0 International (CC BY 4.0)"
            or meta["simplifiedGeometryGeoJSON"] != SOURCE_URL
            or data.get("crs", {}).get("properties", {}).get("name") != "urn:ogc:def:crs:OGC:1.3:CRS84"):
        raise ValueError("Boundary source/metadata differs from review")
    features, seen = [], set()
    for feature in data["features"]:
        properties = feature["properties"]
        name = properties["shapeName"].upper()
        if name == "ABUJA FEDERAL CAPITAL TERRITORY":
            name = "FCT"
        if name not in STATE_NAMES or name in seen or properties["shapeGroup"] != "NGA":
            raise ValueError("Boundary/state crosswalk mismatch")
        seen.add(name)
        geometry = feature["geometry"]
        if geometry["type"] not in ("Polygon", "MultiPolygon"):
            raise ValueError("Expected polygon geometry")
        # D3 spherical rendering expects clockwise exterior rings, counterclockwise holes.
        polygons = [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]
        for polygon in polygons:
            for index, ring in enumerate(polygon):
                if len(ring) < 4 or ring[0] != ring[-1]:
                    raise ValueError("Unclosed boundary ring")
                if any(len(p) != 2 or not (2 <= p[0] <= 15 and 4 <= p[1] <= 14) for p in ring):
                    raise ValueError("Boundary coordinates outside reviewed Nigeria extent")
                signed = sum(a[0]*b[1] - b[0]*a[1] for a, b in itertools.pairwise(ring))
                if (index == 0 and signed > 0) or (index > 0 and signed < 0):
                    ring.reverse()
        features.append({"type": "Feature", "properties": {
            "code": STATE_NAMES.index(name)+1, "name": name}, "geometry": geometry})
    if seen != set(STATE_NAMES):
        raise ValueError("Expected all 37 states/FCT")
    result = {"type": "FeatureCollection", "features": sorted(features, key=lambda f: f["properties"]["code"]),
              "provenance": {"boundary_id": meta["boundaryID"], "year": "2022", "source": "GRID3 / geoBoundaries gbOpen",
                  "source_url": SOURCE_URL, "source_sha256": hashlib.sha256(raw).hexdigest(),
                  "metadata_sha256": hashlib.sha256(metadata.read_bytes()).hexdigest(),
                  "licence": "CC BY 4.0", "licence_url": "https://creativecommons.org/licenses/by/4.0/",
                  "crs": "OGC:CRS84 (longitude, latitude)",
                  "changes": "Upstream simplified geometry; reviewed name/code crosswalk; ring orientation normalized for D3"}}
    output.write_text(json.dumps(result, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    print("37 public boundaries matched one-to-one; FCT alias explicit")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    prepare(args.source, args.metadata, args.output)
