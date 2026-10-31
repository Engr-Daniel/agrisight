# Dependency licence review - 2026-10-31

Scope: all 45 pins in requirements/m4.lock, including runtime, test and build tools. Installed versions match the lock. Evidence: installed distribution licence declarations and shipped LICENSE/COPYING/NOTICE text. Generic BSD declarations were reconciled against the shipped three-clause texts. File hashes are in the private review inventory.

| Distribution | Version | Declared / inspected licence | Shipped notice files |
|---|---|---|---:|
| altair | 6.3.0 | BSD-3-Clause | 1 |
| anyio | 4.15.1 | MIT | 1 |
| attrs | 26.1.0 | MIT | 1 |
| certifi | 2026.10.23 | MPL-2.0 | 1 |
| charset-normalizer | 3.5.2 | MIT | 1 |
| click | 8.5.0 | BSD-3-Clause | 1 |
| colorama | 0.4.6 | BSD-3-Clause | 1 |
| h11 | 0.16.0 | MIT | 1 |
| idna | 3.20 | BSD-3-Clause | 1 |
| iniconfig | 2.3.1 | MIT | 1 |
| itsdangerous | 2.2.0 | BSD-3-Clause | 1 |
| Jinja2 | 3.1.6 | BSD-3-Clause | 1 |
| jsonschema-specifications | 2025.9.1 | MIT | 1 |
| jsonschema | 4.26.0 | MIT | 1 |
| MarkupSafe | 3.0.4 | BSD-3-Clause | 1 |
| narwhals | 2.28.0 | MIT | 1 |
| numpy | 2.4.6 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | 17 |
| packaging | 26.3 | Apache-2.0 OR BSD-2-Clause | 3 |
| pandas | 2.3.3 | BSD-3-Clause | 1 |
| pillow | 13.0.0 | MIT-CMU | 1 |
| pip | 24.0 | MIT | 1 |
| pluggy | 1.7.0 | MIT | 1 |
| protobuf | 7.36.2 | BSD-3-Clause | 1 |
| pyarrow | 26.0.0 | Apache-2.0 | 2 |
| pydeck | 0.9.3 | Apache License 2.0 | 1 |
| Pygments | 2.21.0 | BSD-2-Clause | 2 |
| pytest | 9.2.0 | MIT | 1 |
| python-dateutil | 3.0.0 | Apache-2.0 / BSD-3-Clause (mixed contributions) | 1 |
| python-multipart | 0.0.32 | Apache-2.0 | 1 |
| pytz | 2026.5 | MIT | 1 |
| referencing | 0.37.0 | MIT | 1 |
| requests | 2.34.2 | Apache-2.0 | 2 |
| rpds-py | 2026.9.1 | MIT | 1 |
| ruff | 0.17.3 | MIT | 1 |
| setuptools | 80.9.0 | MIT | 19 |
| six | 1.17.0 | MIT | 1 |
| starlette | 1.10.0 | BSD-3-Clause | 1 |
| streamlit | 1.66.1 | Apache-2.0 | 0 |
| typing_extensions | 4.16.0 | PSF-2.0 | 1 |
| tzdata | 2026.6 | Apache-2.0 | 2 |
| urllib3 | 2.8.0 | MIT | 1 |
| uvicorn | 0.54.0 | BSD-3-Clause | 1 |
| watchdog | 6.0.0 | Apache-2.0 | 2 |
| websockets | 17.3 | BSD-3-Clause | 1 |
| wheel | 0.45.1 | MIT | 1 |

## Decision and obligations

Review completed for the current source-based deployment: dependencies are installed from upstream distributions, not vendored or relicensed as AgriSight MIT code. Keep upstream copyright, licence and applicable NOTICE material. This is not a vulnerability audit or legal opinion.

- NumPy declares composite terms; retain its bundled-component notices. PyArrow includes third-party NOTICE text alongside Apache LICENSE.
- certifi is MPL-2.0; its files are not modified or vendored here. File-level obligations remain applicable to later redistribution/modification.
- python-dateutil has Apache/BSD contribution terms; preserve its full notice.
- Streamlit declares Apache-2.0 in installed metadata but this installed distribution contains no LICENSE/NOTICE file. That packaging limitation is recorded rather than treating absence as permission to discard upstream terms; preserve upstream notices when distributing a bundled app.
- Platform-specific wheels may have additional bundled notices. Re-review changed pins, wheels, vendoring or modified dependencies. This review does not exhaustively cover hosting infrastructure or embedded browser dependencies.

Geographic boundaries, survey-result citation and application MIT are separate rights scopes; see THIRD_PARTY_NOTICES.md and PUBLIC_HOSTING_REVIEW.md.
