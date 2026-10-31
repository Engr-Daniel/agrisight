"""Actual local Chrome review of the stakeholder product, with private captures."""

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

from m4_browser_review import Page, free_port, get_json, stop_processes, wait_for
from websockets.sync.client import connect

ROOT = Path(__file__).resolve().parents[1]


def choose_activity(page: Page, index: int, label: str = "Explore agricultural activities") -> None:
    selector = f'[role="combobox"][aria-label="{label}"]'
    wait_for(lambda: page.js(f"!!document.querySelector({json.dumps(selector)})"))
    assert page.js(f"(() => {{const e=document.querySelector({json.dumps(selector)});"
                   "if(!e)return false;e.scrollIntoView({block:'center'});e.focus();return true;})()")
    time.sleep(0.4)  # Finish scrolling to controls lower on the longer insights page.
    page.key("ArrowDown", "ArrowDown", 40)
    wait_for(lambda: page.js("!!document.querySelector('[role=listbox]')"))
    page.key("Home", "Home", 36)
    for _ in range(index):
        page.key("ArrowDown", "ArrowDown", 40)
    time.sleep(0.1)
    page.key("Enter", "Enter", 13)


def bar_values(page: Page) -> list:
    return page.js("[...document.querySelectorAll('.agri-activity-chart:not(.agri-water-chart):not(.agri-crop-chart):not(.agri-seed-chart) strong')].map(e=>e.textContent)")


def water_unit(page: Page, label: str, key: str = "water_unit") -> None:
    selector = json.dumps('.st-key-' + key + ' label')
    assert page.js(f"(() => {{const e=[...document.querySelectorAll({selector})]"
                   f".find(e=>e.innerText.trim()==={json.dumps(label)});"
                   "const i=e?.querySelector('input');if(!i)return false;i.focus();return true;})()")
    page.key(" ", "Space", 32)


def water_values(page: Page) -> list:
    return page.js("[...document.querySelectorAll('.agri-water-chart strong')].map(e=>e.textContent)")


def crop_values(page: Page) -> list:
    return page.js("[...document.querySelectorAll('.agri-crop-chart strong')].map(e=>e.textContent)")


def seed_values(page: Page) -> list:
    return page.js("[...document.querySelectorAll('.agri-seed-chart strong')].map(e=>e.textContent)")


def check_hover_figures(page: Page) -> int:
    """Values stay visible; the detail line follows real pointer entry/exit and keyboard focus."""
    count = page.js("document.querySelectorAll('.agri-activity-chart').length")
    assert count == 4
    for index in range(count):
        row = f"document.querySelectorAll('.agri-activity-chart')[{index}].querySelector('li')"
        page.js(f"{row}.scrollIntoView({{block:'center',behavior:'instant'}})")
        page.js("document.activeElement.blur()")
        page.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 0, "y": 0})
        value = f"getComputedStyle({row}.querySelector('strong')).opacity"
        opacity = f"getComputedStyle({row}.querySelector('small')||{row}.querySelector('strong')).opacity"
        assert page.js(value) == "1"  # value visible without hover
        detail = page.js(f"!!{row}.querySelector('small')")
        assert page.js(opacity) == ("0" if detail else "1")
        before = page.js(f"{row}.getBoundingClientRect().height")
        point = page.js(f"(() => {{const r={row}.getBoundingClientRect();"
                        "return {x:r.x+r.width/2,y:r.y+r.height/2};})()")
        page.call("Input.dispatchMouseEvent", {"type": "mouseMoved", **point})
        assert page.js(opacity) == "1"
        assert page.js(f"{row}.getBoundingClientRect().height") == before
        page.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 0, "y": 0})
        assert page.js(opacity) == ("0" if detail else "1") and page.js(value) == "1"
        page.js(f"{row}.focus()")
        assert page.js(opacity) == "1"
        page.key("Tab", "Tab", 9)
        assert page.js(opacity) == ("0" if detail else "1") and page.js(value) == "1"
    return count


def check_farming_conditions(page: Page, output: Path, mode: str, audit: dict) -> None:
    """Visit every FC1 question and check real rendered chart types and hover."""
    wait_for(lambda: page.js("document.querySelector('[data-testid=stApp]')?.getAttribute('data-test-script-state')==='notRunning'"))
    wait_for(lambda: page.js("[...document.querySelectorAll('[role=tab]')].some(e=>e.textContent.trim()==='Land & travel')"))
    def tab(label):
        # Streamlit 1.66 uses React Aria tab divs, not button elements.
        assert page.js("(() => {const e=[...document.querySelectorAll('[role=tab]')].find(e=>"
                       f"e.textContent.trim()==={json.dumps(label)});"
                       "if(!e)return false;e.scrollIntoView({block:'center'});e.focus();return true;})()")
        page.key("Enter", "Enter", 13)
        wait_for(lambda: page.js("[...document.querySelectorAll('[role=tab]')].some(e=>"
                                 f"e.textContent.trim()==={json.dumps(label)} && e.getAttribute('aria-selected')==='true')"))
    tab("Land & travel")
    wait_for(lambda: page.js("!!document.querySelector('.st-key-farming_conditions [role=combobox]')"))
    for index, name in ((0, "tenure"), (1, "travel"), (2, "transport")):
        choose_activity(page, index, "Explore land and travel")
        mark = "arc" if index == 0 else "symbol"
        wait_for(lambda mark=mark: page.js(f"!!document.querySelector('.st-key-farming_conditions svg .mark-{mark} path')"))
        if index == 1:
            wait_for(lambda: "268,052" in page.text() and "5,835" in page.text())
        audit["captures"].append(page.capture(output, f"{mode}_fc_{name}", anchor=".st-key-farming_conditions"))
        audit["checks"][mode + "_fc_" + name] = True
    tab("Harvest difficulties")
    wait_for(lambda: page.js("!!document.querySelector('[aria-label=\"Explore harvest response branch\"]')"))
    for branch in (0, 1):
        choose_activity(page, branch, "Explore harvest response branch")
        for question in range(4):
            choose_activity(page, question, "Explore harvest difficulties")
            assert "crop failure" in page.text()
        audit["captures"].append(page.capture(output, f"{mode}_fc_harvest_{branch}", anchor=".st-key-farming_conditions"))
        audit["checks"][f"{mode}_fc_harvest_branch_{branch}_all_questions"] = True
    tab("Sales & storage")
    wait_for(lambda: page.js("!!document.querySelector('[aria-label=\"Explore crop destinations\"]')"))
    for index, name in ((0, "destinations"), (1, "overlap"), (2, "losses")):
        choose_activity(page, index, "Explore crop destinations")
        if index == 0:
            choose_activity(page, 1, "Focus harvested crop")
            choose_activity(page, 0, "Focus harvested crop")
        audit["captures"].append(page.capture(output, f"{mode}_fc_{name}", anchor=".st-key-farming_conditions"))
        audit["checks"][mode + "_fc_" + name] = True
    wait_for(lambda: "334,133" in page.text() and "post-harvest-only loss rate" in page.text())
    tab("Input records")
    water_unit(page, "Record counts", "fc_unit")
    water_unit(page, "Percentages", "fc_unit")
    wait_for(lambda: "15,409" in page.text())
    audit["captures"].append(page.capture(output, f"{mode}_fc_inputs", anchor=".st-key-farming_conditions"))
    cells = ".st-key-farming_conditions svg [role=graphics-symbol][aria-label*=\"Status:\"]"
    wait_for(lambda: page.js(f"document.querySelectorAll({json.dumps(cells)}).length===84"))
    assert page.js(f"new Set([...document.querySelectorAll({json.dumps(cells)})].map(e=>Math.round(e.getBoundingClientRect().y*1000))).size") == 21
    point = page.js("(() => {const e=[...document.querySelectorAll('.st-key-farming_conditions svg [role=graphics-symbol]')]"
                    ".find(e=>(e.getAttribute('aria-label')||'').includes('Status: Missing'));"
                    "if(!e)return null;e.scrollIntoView({block:'center',behavior:'instant'});const r=e.getBoundingClientRect();"
                    "return {x:r.x+r.width/2,y:r.y+r.height/2};})()")
    assert point
    page.call("Input.dispatchMouseEvent", {"type": "mouseMoved", **point})
    tip = wait_for(lambda: page.js("(() => {const e=document.querySelector('#vg-tooltip-element');"
                                  "return e?.classList.contains('visible')?e.innerText:'';})()"))
    assert "Missing" in tip and "Denominator" in tip
    audit["checks"][mode + "_fc_four_topics_controls_hover"] = True
    audit["captures"].append(page.capture(output, f"{mode}_fc_inputs_table", anchor=".st-key-farming_conditions [data-testid=stDataFrame]"))


def review(fc_only: bool = False):
    output = ROOT / "reports/private" / datetime.now(UTC).strftime("stakeholder-browser-%Y%m%dT%H%M%SZ")
    output.mkdir(parents=True)
    app_port, browser_port = free_port(), free_port()
    processes = []
    audit = {"checks": {}, "captures": [], "cleanup": {}}
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    browser = Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / "Google/Chrome/Application/chrome.exe"
    try:
        processes.append(subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.address",
            "127.0.0.1", "--server.port", str(app_port), "--server.headless", "true",
            "--browser.gatherUsageStats", "false"], cwd=ROOT, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, creationflags=flags))
        processes.append(subprocess.Popen([
            str(browser), "--headless=new", "--disable-gpu", "--no-first-run",
            "--no-default-browser-check", "--disable-background-networking", "--disable-sync",
            f"--user-data-dir={output / 'profile'}", f"--remote-debugging-port={browser_port}",
            "--remote-debugging-address=127.0.0.1", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags))
        target = wait_for(lambda: next((t for t in get_json(
            f"http://127.0.0.1:{browser_port}/json/list") if t["type"] == "page"), None))
        with connect(target["webSocketDebuggerUrl"], proxy=None, max_size=16777216,
                     ping_interval=None) as websocket:
            page = Page(websocket)
            page.output = output
            audit["browser"] = page.call("Browser.getVersion")["product"]
            for method in ("Page.enable", "Runtime.enable", "Network.enable"):
                page.call(method)
            page.call("Page.navigate", {"url": f"http://127.0.0.1:{app_port}"})
            wait_for(lambda: "92.84%" in page.text())
            for mode, width, height in (("desktop", 1440, 1000), ("narrow", 390, 844)):
                page.resize(width, height)
                if fc_only:
                    page.button("Agricultural insights")
                    wait_for(lambda: "Farming conditions, harvest and input records" in page.text())
                    check_farming_conditions(page, output, mode, audit)
                    continue
                for name, anchor in (("Overview", "Understand agricultural activity"),
                                     ("Agricultural insights", "Where crop and livestock"),
                                     ("Data quality", "Plot-area coverage"),
                                     ("Recommendations", "Investigate households"),
                                     ("About AgriSight", "Source and scope")):
                    page.button(name)
                    wait_for(lambda anchor=anchor: anchor in page.text())
                    assert "Engineering studies" not in page.text()
                    assert "Evidence & methods" not in page.text()
                    assert "NASS" in page.text()
                    audit["captures"].append(page.capture(output, f"{mode}_{name.replace(' ', '_')}"))
                    audit["captures"].append(page.capture(output, f"{mode}_{name.replace(' ', '_')}_bottom", True))
                    if name == "Agricultural insights":
                        choose_activity(page, 0)
                        page.view("Percentages")
                        wait_for(lambda: bar_values(page) == ["92.84%", "69.45%", "4.62%", "2.62%"])
                        audit["captures"].append(page.capture(output, f"{mode}_all_percentages", anchor=".agri-activity-chart"))
                        page.view("Household counts")
                        wait_for(lambda: bar_values(page) == ["132,859", "99,389", "6,607", "3,747"])
                        audit["captures"].append(page.capture(output, f"{mode}_all_counts", anchor=".agri-activity-chart"))
                        choose_activity(page, 3)
                        wait_for(lambda: bar_values(page) == ["6,607"])
                        audit["captures"].append(page.capture(output, f"{mode}_focused_count", anchor=".agri-activity-chart"))
                        page.view("Percentages")
                        wait_for(lambda: bar_values(page) == ["4.62%"])
                        audit["captures"].append(page.capture(output, f"{mode}_focused_percentage", anchor=".agri-activity-chart"))
                        choose_activity(page, 0)
                        wait_for(lambda: len(bar_values(page)) == 4)
                        audit["checks"][mode + "_activity_keyboard_and_units"] = True
                        choose_activity(page, 0, "Explore crop records")
                        water_unit(page, "Percentages", "crop_unit")
                        wait_for(lambda: crop_values(page)[:1] == ["61.53%"])
                        assert "119,909" in page.text() and "12,950" in page.text()
                        audit["captures"].append(page.capture(output, f"{mode}_crop_portfolio", anchor=".st-key-crop_portfolio"))
                        water_unit(page, "Household counts", "crop_unit")
                        wait_for(lambda: crop_values(page)[:1] == ["73,779"])
                        audit["captures"].append(page.capture(output, f"{mode}_crop_counts", anchor=".st-key-crop_portfolio"))
                        choose_activity(page, 1, "Explore crop records")
                        wait_for(lambda: crop_values(page) == ["22,764", "32,799", "29,187", "18,350", "16,809"])
                        audit["captures"].append(page.capture(output, f"{mode}_crop_diversity_counts", anchor=".st-key-crop_portfolio"))
                        water_unit(page, "Percentages", "crop_unit")
                        wait_for(lambda: crop_values(page) == ["18.98%", "27.35%", "24.34%", "15.30%", "14.02%"])
                        assert "2.91" in page.text()
                        audit["captures"].append(page.capture(output, f"{mode}_crop_diversity", anchor=".st-key-crop_portfolio"))
                        choose_activity(page, 0, "Explore crop records")
                        wait_for(lambda: len(crop_values(page)) == 10)
                        audit["checks"][mode + "_crop_modes_units_scope"] = True
                        choose_activity(page, 0, "Explore seed records")
                        water_unit(page, "Percentages", "seed_unit")
                        wait_for(lambda: seed_values(page) == ["62.83%", "3.59%", "42.08%", "2.97%", "1.50%"])
                        assert "349,046" in page.text() and "119,897" in page.text()
                        assert "Variety and certification percentages are not shown" in page.text()
                        audit["captures"].append(page.capture(output, f"{mode}_seed_sources", anchor=".st-key-seed_sources"))
                        water_unit(page, "Record counts", "seed_unit")
                        wait_for(lambda: seed_values(page)[:1] == ["219,313"])
                        audit["captures"].append(page.capture(output, f"{mode}_seed_counts", anchor=".st-key-seed_sources"))
                        choose_activity(page, 1, "Explore seed records")
                        wait_for(lambda: seed_values(page)[:3] == ["183,079", "110,515", "29,056"])
                        audit["captures"].append(page.capture(output, f"{mode}_seed_combinations_counts", anchor=".st-key-seed_sources"))
                        water_unit(page, "Percentages", "seed_unit")
                        wait_for(lambda: seed_values(page)[:1] == ["52.45%"])
                        assert "Rare combinations are not individually exposed" in page.text()
                        audit["captures"].append(page.capture(output, f"{mode}_seed_combinations", anchor=".st-key-seed_sources"))
                        choose_activity(page, 0, "Explore seed records")
                        wait_for(lambda: len(seed_values(page)) == 5)
                        audit["checks"][mode + "_seed_modes_units_denominators_variety_gate"] = True
                        choose_activity(page, 0, "Explore water management")
                        water_unit(page, "Percentages")
                        wait_for(lambda: water_values(page) == ["4.11%", "95.89%"])
                        audit["captures"].append(page.capture(output, f"{mode}_water_infrastructure", anchor=".st-key-water_management"))
                        for index, question, first in ((1, "methods", "76.47%"), (2, "sources", "56.03%")):
                            choose_activity(page, index, "Explore water management")
                            wait_for(lambda first=first: water_values(page)[0] == first)
                            assert "11,268" in page.text() and "expected skips" in page.text()
                            audit["captures"].append(page.capture(output, f"{mode}_water_{question}", anchor=".st-key-water_management"))
                        water_unit(page, "Plot counts")
                        wait_for(lambda: water_values(page)[0] == "6,313")
                        audit["captures"].append(page.capture(output, f"{mode}_water_source_counts", anchor=".st-key-water_management"))
                        choose_activity(page, 0, "Explore water management")
                        wait_for(lambda: water_values(page) == ["11,268", "262,619"])
                        water_unit(page, "Percentages")
                        wait_for(lambda: water_values(page)[0] == "4.11%")
                        audit["checks"][mode + "_water_questions_units_denominators"] = True
                        audit["checks"][mode + "_hover_focus_exit_stable_layout"] = check_hover_figures(page)
                        page.rendered_chart()
                        assert "coverage map is unavailable" not in page.text()
                        assert "143,105" in page.text() and "CC BY 4.0" in page.text()
                        audit["captures"].append(page.capture(output, f"{mode}_coverage_map", anchor=".st-key-coverage_map"))
                        point = wait_for(lambda: page.js("(() => {const e=document.querySelector('.st-key-coverage_map path[aria-label*=SOKOTO]');"
                                                        "if(!e)return null;const r=e.getBoundingClientRect();"
                                                        "return {x:r.x+r.width*.5,y:r.y+r.height*.5};})()"))
                        page.call("Input.dispatchMouseEvent", {"type": "mouseMoved", **point})
                        tooltip = wait_for(lambda: page.js("(() => {const e=document.querySelector('#vg-tooltip-element');"
                                                          "return e?.classList.contains('visible') ? e.innerText : '';})()"))
                        assert "SOKOTO" in tooltip and "4,590" in tooltip
                        audit["checks"][mode + "_map_tooltip"] = tooltip
                        audit["captures"].append(page.capture(output, f"{mode}_map_tooltip", anchor=".st-key-coverage_map"))
                        assert page.js("(() => {const e=[...document.querySelectorAll('summary')]"
                                       ".find(e=>e.innerText.includes('Read the state coverage table'));"
                                       "if(!e)return false;e.focus();return true;})()")
                        page.key("Enter", "Enter", 13)
                        wait_for(lambda: page.js("!!document.querySelector('details[open]')"))
                        audit["captures"].append(page.capture(output, f"{mode}_coverage_table", True))
                        audit["checks"][mode + "_map_and_accessible_table"] = True
                        check_farming_conditions(page, output, mode, audit)
                    audit["checks"][mode + "_" + name] = True
            audit["runtime_exception_count"] = len(page.exceptions)
            audit["request_hosts"] = sorted(page.hosts)
            assert not page.exceptions
            audit["status"] = "passed_pending_visual_inspection"
    finally:
        audit["cleanup_notes"] = stop_processes(processes)
        for name, port in (("app", app_port), ("debugger", browser_port)):
            with socket.socket() as probe:
                audit["cleanup"][name + "_port_closed"] = probe.connect_ex(("127.0.0.1", port)) != 0
        (output / "review.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
        print(output.relative_to(ROOT).as_posix())
    assert all(audit["cleanup"].values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fc-only", action="store_true", help="Compatibility flag; current grouped review covers all topics")
    parser.parse_args()
    from grouped_browser_review import review as grouped_review

    grouped_review()
