"""Actual local Chrome review of the stakeholder product, with private captures."""

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
    return page.js("[...document.querySelectorAll('.agri-activity-chart:not(.agri-water-chart):not(.agri-crop-chart) strong')].map(e=>e.textContent)")


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


def review():
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
    review()
