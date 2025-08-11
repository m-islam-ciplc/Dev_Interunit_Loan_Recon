### Project Status — Interunit Loan Reconciler

Last updated: updated after audit_info storage and exporter changes

## Overview
- Flask-based web app for interunit loan reconciliation
- Modular, service-oriented backend under `core/`
- Data stored in MySQL via SQLAlchemy
- Excel ingestion (Tally) via Pandas/Openpyxl
- Multiple matching algorithms with JSON audit trail per match

## Architecture
- Entry point: `app_interunit_loan_recon.py`
  - Registers UI and API blueprints from `core/routes`
- Core modules: `core/`
  - `config.py`: MySQL config, manual company pairs
  - `database.py`: DB I/O, queries, match persistence, audit JSON builder
  - `matching/`: Refactored single-responsibility matchers and orchestrator
  - `services/reconciliation_service.py`: Orchestrates reconciliation flow
  - `bank_config.py`: Bank mappings and helpers (see below)
- UI: `templates/index.html` + `static/app.js` + Bootstrap

## Matching modules (core/matching/)
- `po_matcher.py`: `extract_po(text)`
- `lc_matcher.py`: `extract_lc(text)`, `normalize_lc_number(text)`
- `loan_matcher.py`: `has_time_loan_phrase(text)`, `extract_normalized_loan_id(text)`, `extract_normalized_loan_id_after_time_loan_phrase(text)`, `extract_loan_id(text)`
- `account_matcher.py`: `extract_account_number(text)`
- `salary_matcher.py`: `extract_salary_details(text)`
- `settlement_matcher.py`: `extract_final_settlement_details(text)`
- `text_matcher.py`: `calculate_jaccard_similarity(a,b)`, `extract_common_text(a,b)`, `extract_phrases(text)`
- `interunit_matcher.py`: dictionary-based interunit matching (see below)
- `main_matcher.py`: `find_matches(data)` – orchestrates all matchers
- Backward-compat layer: `core/matching.py` re-exports key functions

## Interunit loan matching (dictionary-based)
- Mapping location: `core/bank_config.py`
  - `INTERUNIT_ACCOUNT_MAPPING = { 'FULL_ACCOUNT_FORMAT': 'SHORT_REFERENCE', ... }`
  - Helpers: `get_interunit_account_mapping()`, `get_short_reference(full)`, `get_full_account(short)`, `add_interunit_account_mapping(full, short)`, `remove_interunit_account_mapping(full)`
- Current sample entries:
  - `Midland Bank PLC-CD-A/C-0011-1050011026` → `MDB#11026`
  - `Midland-CE-0011-1060000331-CI` → `MDB#0331`
- Matching logic (strict two-way):
  1) If lender particulars contain a full account from the mapping, borrower must contain the lender’s short reference
  2) If borrower particulars contain a full account from the mapping, lender must contain the borrower’s short reference
  3) Both must succeed; otherwise, return None and fall back to other matchers
- Function: `core/matching/interunit_matcher.py::match_interunit_loans(lender_particulars, borrower_particulars)`
  - Returns on success: `{ lender_account, borrower_account, lender_short_ref, borrower_short_ref }`
- Orchestrator (`main_matcher.py`) builds minimal audit:
  - `audit_trail: { lender_account, borrower_account, lender_short_ref, borrower_short_ref }`

## Audit info JSON formats (stored in `tally_data.audit_info`)
Storage & format
- Column type: `LONGTEXT` (ordered JSON string preserved exactly as constructed)
- Quotes: kept (downstream tools parse JSON for formatting/export)
- Common envelope (built in `core/database.py`):
  - Always includes: `match_type`, `match_method`
  - Adds type-specific keys and amounts

- PO
```json
{
  "match_type": "PO",
  "match_method": "reference_match",
  "po_number": "ABC/PO/123/456",
  "lender_amount": "50000.00",
  "borrower_amount": "50000.00"
}
```

- LC
```json
{
  "match_type": "LC",
  "match_method": "reference_match",
  "lc_number": "L/C-308524027065/24",
  "lender_amount": "1575.00",
  "borrower_amount": "1575.00"
}
```

- INTERUNIT_LOAN (dictionary-based)
```json
{
  "match_type": "INTERUNIT_LOAN",
  "match_method": "cross_reference",
  "lender_account": "Midland Bank PLC-CD-A/C-0011-1050011026",
  "lender_short_ref": "MDB#11026",
  "borrower_account": "Midland-CE-0011-1060000331-CI",
  "borrower_short_ref": "MDB#0331",
  "lender_amount": "12000000.00",
  "borrower_amount": "12000000.00"
}
```

Exporter rendering for INTERUNIT_LOAN
- Lender: `<account> (<short_ref>)`
- Borrower: `<account> (<short_ref>)`

- FINAL_SETTLEMENT
```json
{
  "match_type": "FINAL_SETTLEMENT",
  "match_method": "reference_match",
  "person": "John Doe (EID 12345)",
  "lender_amount": "10000.00",
  "borrower_amount": "10000.00",
  "match_reason": "Final settlement match",
  "person_name": "John Doe",
  "person_id": "12345"
}
```

- SALARY (manual review by default)
```json
{
  "match_type": "SALARY",
  "match_method": "similarity_match",
  "person": "Jane Smith",
  "period": "Aug-2025",
  "lender_amount": "25000.00",
  "borrower_amount": "25000.00",
  "jaccard_score": 0.35
}
```

- COMMON_TEXT (fallback)
```json
{
  "match_type": "COMMON_TEXT",
  "match_method": "similarity_match",
  "common_text": "Transfer for utilities",
  "matched_text": "Transfer for utilities",
  "matched_phrase": "Transfer for utilities",
  "lender_amount": "5000.00",
  "borrower_amount": "5000.00",
  "jaccard_score": 0.42
}
```

## Frontend behavior
- `templates/index.html` renders the SPA
- `static/app.js` renders matched results table and now displays raw JSON for the "Audit Info" column (no formatting)
- Auto-accept badge shown for PO, LC, LOAN_ID, FINAL_SETTLEMENT, INTERUNIT_LOAN

## Export behavior
- Exporter prefers `match_audit_info` (falls back to `audit_info`) and pretty-prints audit details
- INTERUNIT_LOAN shows account and short ref one after another for both sides

## Configuration
- `core/config.py` – MySQL creds (`MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_DB`), manual company pairs
- `core/bank_config.py` – bank name mapping, account patterns, interunit account mapping + helpers
- Modularization: `bank_config.py` is a dedicated module with read/update helper functions

## Database / schema
- SQL file: `db_query_interunit_loan_recon.sql` (creates `tally_data`)
- `core/database.py` ensures table exists before operations and handles all query/update flows

Schema changes
- `audit_info` column is `LONGTEXT` to preserve key order in stored JSON string
- Migration SQL for existing DBs:
```sql
ALTER TABLE tally_data MODIFY audit_info LONGTEXT NULL;
```

## How to run
- Development (Windows):
  - Activate venv: `.venv\Scripts\activate`
  - Run: `python app_interunit_loan_recon.py`
  - App: `http://127.0.0.1:5001`
- Production: see `# Server Controls - Start & Stop.md` for Gunicorn commands

## Recent refactors and fixes
- Split `core/matching.py` into modular matchers under `core/matching/`
- Implemented dictionary-based interunit matching with strict two-way validation
- Simplified audit JSON for interunit to minimal fields; included short refs on request
- UI now displays raw audit JSON in table
- Import guard in `interunit_matcher.py` to avoid relative import issues in different contexts
- Exporter updated to read `match_audit_info` and format INTERUNIT_LOAN as "Account (ShortRef)"
- `audit_info` stored as ordered JSON string (LONGTEXT) with exact key order for INTERUNIT_LOAN

## Pending / next
- Expand `INTERUNIT_ACCOUNT_MAPPING` as new accounts arrive
- Add unit tests (prefix test files with `TEST_` per convention)
- Optional: toggle to switch between raw/pretty audit JSON in UI
- Optional: admin UI to manage interunit account mapping
