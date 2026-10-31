# Chart figures on hover — 2026-10-31

The owner requested figures only when hovering over charts. Activity, crop,
seed-source and water-management HTML bars now hide their value labels until
their row is hovered or receives keyboard focus. Activity response details use
the same behavior. Values remain in the accessibility tree; rows are reachable
with Tab and have a visible focus outline. Fixed space prevents layout movement.

Category names, scales, denominator/period notes, interpretations and exact-value
tables stay visible. Existing native plot-chart and map tooltips are unchanged.
No analytical calculations, data inputs, manifests or dependency pins changed.

Validation: 85 targeted tests passed in 30.69 seconds; full development suite
378 passed in 126.58 seconds. Ruff passed for changed Python files; diff check
passed. The actual local Chrome review now checks default-hidden values, pointer
entry/exit, keyboard focus/Tab exit and stable row height in every HTML chart
section at desktop and narrow widths. Browser results are recorded in MEMORY.md
after execution. Desktop and narrow default activity screenshots were inspected.

The verified workspace preview was restarted on loopback port 8501; health
endpoint returned HTTP 200. This is a local preview, with no new deployment.
