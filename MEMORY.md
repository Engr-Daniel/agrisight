# MEMORY.md — AgriSight project memory
Updated: 2026-10-27.

- Repository: private `Engr-Daniel/agrisight`. Work on `master`; mentor-guided learning.
- Independent from confidential client materials. No real registrations or real farm positions.
- Official survey samples and simulated role-registration entries are separate populations.
- M0-04: six submitted role fixtures; four accepted roles but only three distinct persons. Python and SQLite reconcile.
- M0-05: dependency-free quality-contract baseline and catalog-level NASS/GHS source review.
- Initial Pandera/GX Core workflow succeeded. Logged versions: Pandas 2.3.3, Pandera 0.35.0, GX Core 1.24.1 on Python 3.11.
- Second-stage comparison: seven matched synthetic pass/fail scenarios in `src/agrisight/framework_comparison.py`; verify CI results before claiming parity.
- Pandera provisionally preferred for local ingestion; GX Core remains potential monitoring alternative. No final ADR approval.
- Outstanding: source codebooks/weights/permissions, null and error diagnostics parity, precise KPI dictionary, geography/privacy model and M0 owner sign-off.
