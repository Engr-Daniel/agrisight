"""Review current grouped stakeholder navigation; local evidence/screenshots only."""

import json
import os
import socket
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

from m4_browser_review import Page, free_port, get_json, stop_processes, wait_for
from stakeholder_browser_review import choose_activity
from websockets.sync.client import connect

ROOT = Path(__file__).resolve().parents[1]


def chip(page: Page, label: str, ready: str) -> None:
    """Select one subject chip with a real pointer click at its position, then wait for content."""
    find = ("[...document.querySelectorAll('button[data-variant=pills]')].find(e=>"
            f"e.innerText.trim().endsWith({json.dumps(label)}))")
    wait_for(lambda: page.js(f"!!{find}"))
    page.js(f"{find}.scrollIntoView({{block:'center',behavior:'instant'}})")
    time.sleep(.2)
    box = page.js(f"(() => {{const r={find}.getBoundingClientRect();return [r.x+r.width/2, r.y+r.height/2];}})()")
    for kind in ("mousePressed", "mouseReleased"):
        page.call("Input.dispatchMouseEvent", {"type": kind, "x": box[0], "y": box[1],
                                               "button": "left", "clickCount": 1})
    wait_for(lambda: ready in page.text() and page.js(f"{find}.getAttribute('aria-checked')==='true'"))
    time.sleep(.2)


def review() -> None:
    output = ROOT/"reports/private"/datetime.now(UTC).strftime("grouped-browser-%Y%m%dT%H%M%SZ")
    output.mkdir(parents=True)
    app_port, browser_port = free_port(), free_port()
    processes, audit = [], {"checks": {}, "captures": [], "cleanup": {}}
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    browser = Path(os.environ.get("PROGRAMFILES", "C:/Program Files"))/"Google/Chrome/Application/chrome.exe"
    try:
        processes.append(subprocess.Popen([sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.address", "127.0.0.1", "--server.port", str(app_port), "--server.headless", "true",
            "--browser.gatherUsageStats", "false"], cwd=ROOT, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, creationflags=flags))
        processes.append(subprocess.Popen([str(browser), "--headless=new", "--disable-gpu", "--no-first-run",
            "--no-default-browser-check", "--disable-background-networking", "--disable-sync",
            f"--user-data-dir={output/'profile'}", f"--remote-debugging-port={browser_port}",
            "--remote-debugging-address=127.0.0.1", "about:blank"], stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, creationflags=flags))
        target = wait_for(lambda: next((t for t in get_json(f"http://127.0.0.1:{browser_port}/json/list") if t["type"] == "page"), None))
        with connect(target["webSocketDebuggerUrl"], proxy=None, max_size=16777216, ping_interval=None) as ws:
            page = Page(ws)
            audit["browser"] = page.call("Browser.getVersion")["product"]
            for method in ("Page.enable", "Runtime.enable", "Network.enable"):
                page.call(method)
            page.call("Page.navigate", {"url": f"http://127.0.0.1:{app_port}"})
            wait_for(lambda: "92.8%" in page.text() and "Households surveyed" in page.text())
            for mode, width, height in (("desktop", 1440, 1000), ("narrow", 390, 844)):
                page.resize(width, height)
                page.button("Overview")
                wait_for(lambda: "Households surveyed" in page.text())
                assert "143,105" in page.text() and "64% reported both crops and livestock" in page.text()
                assert page.js("document.querySelectorAll('.agri-slide').length") == 6
                audit["captures"].append(page.capture(output, mode+"_overview"))
                page.button("Agricultural insights")
                chip(page, "Activities", "Agricultural activity explorer")
                assert not page.js("document.querySelector('[role=tab]')")  # no nested tab bars
                assert page.js("document.querySelectorAll('button[data-variant=pills]').length") == 9
                assert "these are not national estimates" in page.text()
                assert "Households may report multiple activities" in page.text()
                audit["captures"].append(page.capture(output, mode+"_activities"))
                for _group, subject, ready, anchor in (
                    ("Crops & seeds", "Crop portfolio", "Crop portfolio and diversity", ".st-key-crop_portfolio"),
                    ("Crops & seeds", "Seed sources", "Explore seed records", ".st-key-seed_sources"),
                    ("Crops & seeds", "Input records", "quantity information gaps", ".st-key-input_records"),
                    ("Water & land", "Water management", "Explore water management", ".st-key-water_management"),
                    ("Water & land", "Land & travel", "Explore land and travel", ".st-key-land_travel"),
                    ("Water & land", "Plot types", "What kinds of plots", None),
                    ("Harvest & markets", "Harvest difficulties", "Explore harvest response branch", ".st-key-harvest_difficulties"),
                    ("Harvest & markets", "Sales & storage", "Explore crop destinations", ".st-key-crop_destinations")):
                    chip(page, subject, ready)
                    if subject == "Crop portfolio":
                        assert "119,909 households with recorded temporary crops" in page.text()
                        assert "Crop-roster coverage differs" not in page.text()
                        assert "profitability" not in page.text()
                        choose_activity(page, 1, "Explore crop records")
                        wait_for(lambda: "Mean recorded temporary crop categories" in page.text())
                        choose_activity(page, 0, "Explore crop records")
                        wait_for(lambda: "observed temporary crop categories" in page.text())
                        assert page.js("(() => {const e=[...document.querySelectorAll('.st-key-crop_portfolio summary')].find(e=>"
                                       "e.innerText.includes('Understanding these figures'));"
                                       "if(!e)return false;e.scrollIntoView({block:'center',behavior:'instant'});"
                                       "e.focus();return document.activeElement===e;})()")
                        page.key("Enter", "Enter", 13)
                        wait_for(lambda: "profitability" in page.text())
                        page.key("Enter", "Enter", 13)
                        wait_for(lambda: "profitability" not in page.text())
                        audit["checks"][mode+"_disclosure_open_close"] = True
                    if subject == "Land & travel":
                        choose_activity(page, 1, "Explore land and travel")
                        wait_for(lambda: "268,052" in page.text())
                    if subject == "Sales & storage":
                        choose_activity(page, 1, "Explore crop destinations")
                        wait_for(lambda: "334,133 records valid for both" in page.text())
                    audit["captures"].append(page.capture(output, mode+"_"+subject.replace(" ", "_"), anchor=anchor))
                    audit["checks"][mode+"_"+subject] = True
                page.button("Data quality")
                wait_for(lambda: "12,950" in page.text())
                assert "119,909" in page.text() and "Input quantity completeness" in page.text()
                audit["captures"].append(page.capture(output, mode+"_quality"))
                audit["checks"][mode+"_quality_coverage"] = True
                page.button("About AgriSight")
                wait_for(lambda: "Source and scope" in page.text())
                assert "not a photograph" not in page.text() and "AI-generated" not in page.text()
                page.button("Overview")
                wait_for(lambda: "Nine questions, four topics" in page.text())
                page.button("Seed sources")  # topic card deep link
                wait_for(lambda: "Explore seed records" in page.text())
                audit["checks"][mode+"_topic_deep_link"] = True
            audit.update(runtime_exception_count=len(page.exceptions), request_hosts=sorted(page.hosts))
            assert not page.exceptions and page.hosts == {"127.0.0.1"}
            audit["status"] = "passed_pending_visual_inspection"
    finally:
        audit["cleanup_notes"] = stop_processes(processes)
        for name, port in (("app", app_port), ("debugger", browser_port)):
            with socket.socket() as probe:
                audit["cleanup"][name] = probe.connect_ex(("127.0.0.1", port)) != 0
        (output/"review.json").write_text(json.dumps(audit, indent=2)+"\n", encoding="utf-8", newline="\n")
        print(output.relative_to(ROOT).as_posix())
    assert all(audit["cleanup"].values())


if __name__ == "__main__":
    review()
