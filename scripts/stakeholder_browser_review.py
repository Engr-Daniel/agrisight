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


def choose_activity(page: Page, index: int) -> None:
    selector = '[role="combobox"][aria-label="Explore agricultural activities"]'
    assert page.js(f"(() => {{const e=document.querySelector({json.dumps(selector)});"
                   "if(!e)return false;e.scrollIntoView({block:'center'});e.focus();return true;})()")
    page.key("ArrowDown", "ArrowDown", 40)
    wait_for(lambda: page.js("!!document.querySelector('[role=listbox]')"))
    page.key("Home", "Home", 36)
    for _ in range(index):
        page.key("ArrowDown", "ArrowDown", 40)
    time.sleep(0.1)
    page.key("Enter", "Enter", 13)


def bar_values(page: Page) -> list:
    return page.js("[...document.querySelectorAll('.agri-activity-chart strong')].map(e=>e.textContent)")


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
