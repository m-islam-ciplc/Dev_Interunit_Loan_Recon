# Gunicorn Commands for Interunit Loan Reconciliation

## Quick Start Commands

### Start the Server
```bash
gunicorn -w 4 -b 0.0.0.0:5001 interunit_loan_recon:app --daemon
```

### Stop the Server
```bash
pkill -f "interunit_loan_recon.py"
```

### Restart the Server
```bash
pkill -f "interunit_loan_recon.py" && gunicorn -w 4 -b 0.0.0:5001 interunit_loan_recon:app --daemon
```

### Check if Running
```bash
lsof -i :5001
```

## What These Commands Do

- **Port**: 5001 (your app runs here)
- **Workers**: 4 processes for better performance
- **Binding**: All network interfaces (0.0.0.0)
- **Mode**: Background daemon (--daemon)
- **File**: interunit_loan_recon.py (project-specific naming)

## Access Your App

Once running, access your interunit loan reconciliation software at:
- **Local**: http://localhost:5001
- **Network**: http://your-server-ip:5001

## Prerequisites

1. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Ensure you're in the project directory:**
   ```bash
   cd /opt/Dev_Interunit_Loan_Recon
   ```

## Why This Setup is Better

- ✅ **Project-specific filename**: `interunit_loan_recon.py` (not generic `app.py`)
- ✅ **Safe process management**: Won't affect other projects
- ✅ **Clear identification**: Easy to see which app is running
- ✅ **No conflicts**: Won't accidentally stop wrong processes

## Troubleshooting

- **Port already in use**: `lsof -i :5001` to check
- **Can't start**: Make sure virtual environment is activated
- **App not responding**: Check if Gunicorn is running with `lsof -i :5001`
- **Wrong process killed**: Use `pkill -f "interunit_loan_recon.py"` for safety
