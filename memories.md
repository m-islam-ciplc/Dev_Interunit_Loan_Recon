# User Memories

## Rules and Preferences

- The user requires that any internal testing, debugging, or diagnostic files created should always be prefixed with TEST_ or DIAGNOSE_ as a universal rule.
- The user prefers naming all internal testing and debugging files with a prefix.
- The user prefers using Bootstrap for all styling, removing unnecessary custom CSS, and modifying Bootstrap classes when changes are needed.
- The user prefers that only DEBUG print statements be commented out, not all print statements.
- Generate concise commit messages using conventional format: "type: brief description" (e.g., "feat: add auto-match button", "fix: reduce button padding", "style: update table column widths")

## Project Context

- Working on an interunit loan reconciliation system
- Flask-based web application with MySQL database
- Uses Bootstrap for styling and responsive design
- Complex matching logic for financial transactions
- Auto-acceptance for certain match types (INTERUNIT_LOAN)
- Audit trail system for transparency 