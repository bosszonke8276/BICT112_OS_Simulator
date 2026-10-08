# BICT112 Operating Systems Simulator

## Project
UMP Computer Laboratory Resource Manager

## Run the website locally

Install Python 3, then run:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. `main.py` starts the command-line simulator; `app.py` starts the website.

## Deploy to Vercel

Import this GitHub repository into Vercel and keep the project root as the Root Directory. The included `vercel.json`, `api/index.py`, and `requirements.txt` configure the Flask app as a Python function. No build command or output directory is needed.

The simulator currently keeps jobs and event history in process memory. Vercel functions are temporary, so this data can reset between requests or deployments; persistent user data requires a database or another durable store.

## Current features

- Add jobs/processes
- Input validation
- Ready state
- Job display
- Event log
- Help/About section

## Planned compulsory modules

- First-Fit memory allocation
- Best-Fit memory allocation
- Memory deallocation and merging
- External fragmentation
- FCFS CPU scheduling
- Round Robin CPU scheduling
- Waiting and turnaround time
- Process state transitions
- Printer/device queue
- Dashboard
