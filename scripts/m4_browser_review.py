"""Local Chrome/Chromium review helper; screenshots/profile stay in reports/private.

Uses the existing M4 websockets dependency and an installed browser, not a new
application dependency. No personal browser profile or public server is used.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import socket
import subprocess
import time
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

from websockets.sync.client import connect

ROOT = Path(__file__).resolve().parents[1]


def free_port() -> int:
    with socket.socket() as connection:
        connection.bind(("127.0.0.1", 0))
        return connection.getsockname()[1]


def wait_for(predicate, timeout: float = 40):
    deadline = time.monotonic()+timeout
    while time.monotonic() < deadline:
        try:
            value = predicate()
            if value:
                return value
        except (OSError, ValueError, RuntimeError):
            pass  # Navigation contexts and local endpoints may not exist yet.
        time.sleep(0.2)
    raise RuntimeError("Browser review wait timed out")


def get_json(url: str):
    with urllib.request.urlopen(url, timeout=2) as response:
        return json.load(response)


class Page:
    def __init__(self, websocket):
        self.websocket = websocket
        self.sequence = 0
        self.exceptions = []
        self.hosts = set()
        self.output = None

    def call(self, method: str, params: dict | None = None) -> dict:
        self.sequence += 1
        current = self.sequence
        self.websocket.send(json.dumps({"id": current, "method": method, "params": params or {}}))
        while True:
            answer = json.loads(self.websocket.recv(timeout=20))
            if answer.get("method") == "Runtime.exceptionThrown":
                self.exceptions.append(answer["params"])
            if answer.get("method") == "Network.requestWillBeSent":
                host = urllib.parse.urlparse(answer["params"]["request"]["url"]).hostname
                if host:
                    self.hosts.add(host)
            if answer.get("id") == current:
                if "error" in answer:
                    raise RuntimeError("Browser protocol command failed")
                return answer.get("result", {})

    def js(self, expression: str):
        result = self.call("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        if "exceptionDetails" in result:
            raise RuntimeError("Browser expression failed")
        return result.get("result", {}).get("value")

    def text(self) -> str:
        return self.js('(document.body?.innerText || "")')

    def key(self, key: str, code: str, number: int) -> None:
        for kind in ("keyDown", "keyUp"):
            params = {"type": kind, "key": key, "code": code,
                      "windowsVirtualKeyCode": number, "nativeVirtualKeyCode": number}
            if kind == "keyDown" and key in ("Enter", " "):
                params.update(text="\r" if key == "Enter" else " ",
                              unmodifiedText="\r" if key == "Enter" else " ")
            self.call("Input.dispatchKeyEvent", params)

    def choose_last(self, label: str) -> None:
        selector = f'[role="combobox"][aria-label="{label}"]'
        assert self.js(f"(() => {{const e=document.querySelector({json.dumps(selector)}); "
                       "if(!e)return false;e.scrollIntoView({block:'center',behavior:'instant'});"
                       "e.focus();return document.activeElement===e;})()")
        time.sleep(0.4)  # Finish focus scrolling before opening the popover.
        self.key("ArrowDown", "ArrowDown", 40)
        try:
            wait_for(lambda: self.js("!!document.querySelector('[role=listbox]')"))
        except RuntimeError:
            if self.output:
                (self.output/"failed_control.png").write_bytes(base64.b64decode(
                    self.call("Page.captureScreenshot", {"format": "png"})["data"]))
                state = self.js("({text:document.body.innerText,active:document.activeElement"
                                "?.outerHTML,combos:[...document.querySelectorAll('[role=combobox]')]"
                                ".map(e=>({html:e.outerHTML,top:e.getBoundingClientRect().top}))})")
                (self.output/"failed_control.json").write_text(json.dumps(state, indent=2),
                                                              encoding="utf-8")
            raise
        self.key("End", "End", 35)
        time.sleep(0.1)  # Allow the native listbox focus update before confirming.
        self.key("Enter", "Enter", 13)

    def view(self, label: str) -> None:
        assert self.js("(() => {const label=[...document.querySelectorAll('label')].find(e=>"
                       f"e.innerText.trim()==={json.dumps(label)});"
                       "const input=label?.querySelector('input[type=radio]');"
                       "if(!input)return false;input.focus();return document.activeElement===input;})()")
        self.key(" ", "Space", 32)

    def button(self, label: str) -> None:
        # Match the visible label only; icon glyph names are part of a button's innerText.
        assert self.js("(() => {const b=[...document.querySelectorAll('button')].find(e=>"
                       "(e.querySelector('[data-testid=stMarkdownContainer]')||e)"
                       f".innerText.trim()==={json.dumps(label)});"
                       "if(!b)return false;b.scrollIntoView({block:'center'});b.focus();"
                       "return document.activeElement===b;})()")
        time.sleep(0.2)
        self.key("Enter", "Enter", 13)

    def resize(self, width: int, height: int) -> None:
        self.call("Emulation.setDeviceMetricsOverride", {"width": width, "height": height,
                                                        "deviceScaleFactor": 1, "mobile": False})
        time.sleep(0.5)

    def sidebar(self, opened: bool) -> None:
        visible = "(() => {const r=document.querySelector('[data-testid=stSidebar]')" \
                  "?.getBoundingClientRect();return !!r && r.left>=0 && r.right>0;})()"
        if bool(self.js(visible)) == opened:
            return
        if not opened:
            # Focusing technical navigation can scroll a long mobile drawer.
            # Return to its header before locating the native close control.
            self.js("(() => {const s=document.querySelector('[data-testid=stSidebar]');"
                    "if(s){s.scrollTop=0;s.querySelectorAll('*').forEach(e=>{"
                    "if(e.scrollTop)e.scrollTop=0;});}})()")
            time.sleep(0.2)
        scope = "document" if opened else "document.querySelector('[data-testid=stSidebar]')"
        max_x = 70 if opened else 390
        assert self.js("(() => {const scope="+scope+";const button=[...scope.querySelectorAll('button')]"
                       ".find(e=>{const r=e.getBoundingClientRect();return r.width>0 && r.height>0"
                       f" && r.y>=0 && r.y<70 && r.x>=0 && r.x<{max_x};}});"
                       "if(!button)return false;button.focus();return document.activeElement===button;})()")
        self.key("Enter", "Enter", 13)
        try:
            wait_for(lambda: bool(self.js(visible)) == opened)
        except RuntimeError:
            if self.output:
                (self.output/"failed_sidebar.png").write_bytes(base64.b64decode(
                    self.call("Page.captureScreenshot", {"format": "png"})["data"]))
                state = self.js("(() => {const e=document.querySelector('[data-testid=stSidebar]');"
                                "return {sidebar:e?.outerHTML.slice(0,1500),rect:e?.getBoundingClientRect()"
                                ".toJSON(),active:document.activeElement?.outerHTML,"
                                "buttons:[...document.querySelectorAll('button')].map(b=>"
                                "({text:b.innerText,label:b.getAttribute('aria-label'),"
                                "rect:b.getBoundingClientRect().toJSON()}))};})()")
                (self.output/"failed_sidebar.json").write_text(json.dumps(state, indent=2),
                                                              encoding="utf-8")
            raise

    def rendered_chart(self) -> None:
        wait_for(lambda: self.js("!!document.querySelector('[data-testid=stVegaLiteChart] canvas,"
                                 "[data-testid=stVegaLiteChart] svg')"))

    def capture(self, output: Path, name: str, bottom: bool = False,
                anchor: str | None = None) -> dict:
        wait_for(lambda: self.js("document.querySelector('[data-testid=stApp]')"
                                 "?.getAttribute('data-test-script-state') === 'notRunning'"))
        self.js("(() => {const m=document.querySelector('[data-testid=stMain]');"
                f"if(m)m.scrollTop={'m.scrollHeight' if bottom else '0'};}})()")
        if anchor:
            assert self.js(f"(() => {{const e=document.querySelector({json.dumps(anchor)});"
                           "if(!e)return false;e.scrollIntoView({block:'start'});"
                           "return true;})()")
        time.sleep(0.4)
        image = self.call("Page.captureScreenshot", {"format": "png"})
        (output/f"{name}.png").write_bytes(base64.b64decode(image["data"]))
        layout = self.js("(() => {const m=document.querySelector('[data-testid=stMain]');"
                         "return {width:innerWidth,height:innerHeight,documentWidth:"
                         "document.documentElement.scrollWidth,mainWidth:m?.clientWidth,"
                         "mainScrollWidth:m?.scrollWidth,mainTop:m?.scrollTop};})()")
        assert layout["documentWidth"] <= layout["width"]
        assert layout["mainScrollWidth"] <= layout["mainWidth"]+1
        return {"screenshot": f"{name}.png", "layout": layout}


def stop_processes(processes: list) -> list[str]:
    """Attempt every owned process even if one process handle fails to settle."""
    notes = []
    for process in reversed(processes):
        try:
            if process.poll() is None:
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                   capture_output=True, check=False, timeout=10)
                else:
                    process.terminate()
            process.wait(timeout=5)
        except (subprocess.TimeoutExpired, OSError):
            try:
                process.kill()
                process.wait(timeout=5)
            except (subprocess.TimeoutExpired, OSError):
                notes.append(f"Process {process.pid}: exit could not be confirmed")
    return notes


def review(browser: Path) -> Path:
    output = ROOT/"reports/private/m4_browser_review"/datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    output.mkdir(parents=True)
    app_port, browser_port = free_port(), free_port()
    processes = []
    audit = {"started_at_utc": datetime.now(UTC).isoformat(), "status": "incomplete",
             "captures": [], "checks": {}, "cleanup": {}}
    audit["source_sha256"] = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                              for name in ("research_explorer_app.py", "src/agrisight/reporting_ui.py",
                                           "src/agrisight/reporting_brand.py",
                                           "src/agrisight/reporting_pages.py",
                                           "src/agrisight/assets/dashboard.css",
                                           "src/agrisight/assets/agricultural-landscape-v1.webp",
                                           "src/agrisight/reporting_adapter.py",
                                           "src/agrisight/reporting/artifact_manifest_v2.json",
                                           ".streamlit/config.toml", "requirements/m4.lock",
                                           "scripts/m4_browser_review.py")}
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    try:
        server = subprocess.Popen([str(Path(os.sys.executable)), "-m", "streamlit", "run",
                                   "research_explorer_app.py", "--server.address", "127.0.0.1",
                                   "--server.port", str(app_port), "--server.headless", "true",
                                   "--browser.gatherUsageStats", "false"], cwd=ROOT,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  creationflags=flags)
        processes.append(server)

        def healthy():
            with urllib.request.urlopen(f"http://127.0.0.1:{app_port}/_stcore/health",
                                        timeout=2) as response:
                return response.status == 200

        wait_for(healthy)
        processes.append(subprocess.Popen([
            str(browser), "--headless=new", "--disable-gpu", "--no-first-run",
            "--no-default-browser-check", "--disable-background-networking", "--disable-sync",
            f"--user-data-dir={output/'profile'}", f"--remote-debugging-port={browser_port}",
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
            page.resize(1440, 1000)
            page.call("Page.navigate", {"url": f"http://127.0.0.1:{app_port}"})
            wait_for(lambda: "The survey at a glance" in page.text() and "92.84%" in page.text())
            wait_for(lambda: page.js("(() => {const i=document.querySelector('.agri-hero img');"
                                     "return i?.complete && i.naturalWidth > 0;})()"))
            audit["checks"]["packaged_hero_image_loaded"] = True
            assert "Evidence & provenance" not in page.text()
            assert "Where the evidence comes from" in page.text()
            assert "AI-generated illustration ·" not in page.text()
            audit["captures"].append(page.capture(output, "desktop_overview"))
            for name, anchor in (("stats", ".st-key-stat_households"),
                                 ("story", ".st-key-story_participation"),
                                 ("map", ".agri-map")):
                audit["captures"].append(page.capture(output, f"desktop_overview_{name}",
                                                      anchor=anchor))
            audit["captures"].append(page.capture(output, "desktop_overview_bottom", True))
            page.button("Explore agricultural insights")
            wait_for(lambda: "What missing plot areas can change" in page.text())
            audit["captures"].append(page.capture(output, "desktop_insights"))
            page.button("Inspect area evidence")
            wait_for(lambda: "Known-area-only median" in page.text() and "6,070.29" in page.text())
            audit["checks"]["stakeholder_area_link"] = True
            page.button("Engineering studies")
            wait_for(lambda: "Testing the analytical foundations" in page.text())
            audit["captures"].append(page.capture(output, "desktop_engineering"))
            page.button("Inspect matching evidence")
            wait_for(lambda: "Evaluation seed" in page.text() and "90.91%" in page.text())
            audit["checks"]["stakeholder_matching_link"] = True
            page.button("About")
            wait_for(lambda: "Who it is designed to support" in page.text())
            audit["captures"].append(page.capture(output, "desktop_about"))
            page.button("Agricultural insights")
            wait_for(lambda: "Inspect participation evidence" in page.text())
            page.button("Inspect participation evidence")
            wait_for(lambda: "Valid household responses" in page.text() and "92.84%" in page.text())
            audit["checks"]["stakeholder_participation_link"] = True
            audit["captures"].append(page.capture(output, "desktop_survey"))
            audit["captures"].append(page.capture(output, "desktop_survey_table", True))
            page.choose_last("Indicator")
            wait_for(lambda: "6,070.29" in page.text() and "bounds coincide" in page.text())
            audit["checks"]["keyboard_indicator_selection"] = True
            audit["captures"].append(page.capture(output, "desktop_area"))
            page.view("Synthetic quality")
            wait_for(lambda: "90.91%" in page.text() and "50.00%" in page.text())
            audit["checks"]["keyboard_view_selection"] = True
            assert "SYNTHETIC DEMONSTRATION DATA" in page.text()
            page.choose_last("Evaluation seed")
            wait_for(lambda: "87.72%" in page.text())
            audit["checks"]["keyboard_seed_selection"] = True
            audit["captures"].append(page.capture(output, "desktop_synthetic_quality"))
            audit["captures"].append(page.capture(output, "desktop_synthetic_quality_counts", True))
            page.view("Workload measurements")
            wait_for(lambda: "1.071" in page.text() and "Every measured repetition" in page.text())
            page.rendered_chart()
            assert "39,363" in page.text() and "47,181" in page.text()
            audit["captures"].append(page.capture(output, "desktop_synthetic_workload"))
            audit["captures"].append(page.capture(output, "desktop_synthetic_chart", True))
            page.choose_last("Workload")
            wait_for(lambda: "Rejected: candidate budget exceeded" in page.text())
            assert "499,500 potential pairs / 250,000 allowed" in page.text()
            audit["checks"]["browser_collision_rejection"] = True
            audit["captures"].append(page.capture(output, "desktop_synthetic_rejection", True))
            page.resize(390, 844)
            audit["captures"].append(page.capture(output, "narrow_synthetic_rejection"))
            audit["captures"].append(page.capture(output, "narrow_synthetic_rejection_bottom", True))
            # A new session now lands in the stakeholder layer, including on narrow screens.
            page.call("Page.reload")
            wait_for(lambda: "The survey at a glance" in page.text() and "92.84%" in page.text())
            audit["captures"].append(page.capture(output, "narrow_default_overview"))
            page.button("Open technical evidence")
            wait_for(lambda: "92.84%" in page.text() and "Evidence & provenance" in page.text())
            audit["checks"]["reload_opens_stakeholder_overview"] = True
            audit["captures"].append(page.capture(output, "narrow_survey"))
            audit["captures"].append(page.capture(output, "narrow_survey_table", True))
            page.choose_last("Indicator")
            wait_for(lambda: "6,070.29" in page.text() and "bounds coincide" in page.text())
            audit["captures"].append(page.capture(output, "narrow_area"))
            audit["captures"].append(page.capture(output, "narrow_area_table", True))
            page.view("Synthetic quality")
            wait_for(lambda: "90.91%" in page.text() and "50.00%" in page.text())
            audit["captures"].append(page.capture(output, "narrow_synthetic_quality"))
            audit["captures"].append(page.capture(output, "narrow_synthetic_quality_counts", True))
            page.view("Workload measurements")
            wait_for(lambda: "1.071" in page.text())
            page.rendered_chart()
            audit["captures"].append(page.capture(output, "narrow_synthetic_timing_chart", True))
            page.view("Traced allocation")
            wait_for(lambda: "16.65" in page.text() and "Not process RSS" in page.text())
            page.rendered_chart()
            audit["captures"].append(page.capture(output, "narrow_synthetic_memory_chart", True))
            assert page.js("(() => {const e=[...document.querySelectorAll('summary')]"
                           ".find(e=>e.innerText.includes('Evidence & provenance'));"
                           "if(!e)return false;e.focus();return document.activeElement===e;})()")
            page.key("Enter", "Enter", 13)
            wait_for(lambda: page.js("!!document.querySelector('details[open]')"))
            audit["captures"].append(page.capture(output, "narrow_synthetic_provenance", True))
            audit["checks"]["narrow_keyboard_navigation_and_provenance"] = True
            page.button("Back to the stakeholder website")
            wait_for(lambda: "What missing plot areas can change" in page.text())
            audit["checks"]["narrow_back_to_website"] = True
            page.button("Overview")
            wait_for(lambda: "The survey at a glance" in page.text())
            audit["captures"].append(page.capture(output, "narrow_overview"))
            for name, anchor in (("stats", ".st-key-stat_households"),
                                 ("story", ".st-key-story_participation"),
                                 ("area", ".st-key-story_area")):
                audit["captures"].append(page.capture(output, f"narrow_overview_{name}",
                                                      anchor=anchor))
            audit["captures"].append(page.capture(output, "narrow_overview_bottom", True))
            page.button("Explore agricultural insights")
            wait_for(lambda: "What missing plot areas can change" in page.text())
            audit["captures"].append(page.capture(output, "narrow_insights"))
            page.button("Inspect area evidence")
            wait_for(lambda: "Known-area-only median" in page.text() and "6,070.29" in page.text())
            audit["captures"].append(page.capture(output, "narrow_stakeholder_area_link"))
            audit["checks"]["narrow_stakeholder_to_evidence"] = True
            audit["checks"]["narrow_no_page_horizontal_overflow"] = True
            audit["runtime_exception_count"] = len(page.exceptions)
            audit["request_hosts"] = sorted(page.hosts)
            assert not page.exceptions
            audit["status"] = "browser_checks_passed_visual_inspection_pending"
            print("Browser interactions and screenshots captured; visual inspection still required")
    finally:
        audit["cleanup_notes"] = stop_processes(processes)
        for name, port in (("app", app_port), ("debugger", browser_port)):
            with socket.socket() as probe:
                audit["cleanup"][name+"_port_closed"] = probe.connect_ex(("127.0.0.1", port)) != 0
        (output/"review.json").write_text(json.dumps(audit, indent=2)+"\n", encoding="utf-8")
        print(output.relative_to(ROOT).as_posix())
    if not all(audit["cleanup"].values()):
        raise RuntimeError("Review test process cleanup incomplete")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", type=Path, default=Path(os.environ.get(
        "PROGRAMFILES", "C:/Program Files"))/"Google/Chrome/Application/chrome.exe")
    arguments = parser.parse_args()
    if not arguments.browser.is_file():
        parser.error("Supply an installed Chrome/Chromium executable with --browser")
    review(arguments.browser)
