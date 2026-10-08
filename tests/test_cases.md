# Website Test Cases

## Test Run Summary

- **Run method:** Flask's built-in `app.test_client()` from the Vercel entrypoint (`api/index.py`); no browser automation was used.
- **Result:** 22 checks passed in one local run.
- **Deployment:** The Vercel configuration was parsed and its catch-all route checked locally. A live Vercel deployment was not tested.
- **State:** Tests used a fresh in-process simulator. Website data is held in memory and is not persistent.

## Checks Executed

| ID | Area | Test | Expected result | Actual result |
|---|---|---|---|---|
| WEB-01 | Homepage | Request `/` | HTTP 200; dashboard section is present | **PASS** |
| WEB-02 | Page sections | Check the rendered page for Jobs, Memory, CPU, States, Devices, Events, and Help sections | All seven sections are present | **PASS** |
| WEB-03 | Static assets | Request `/static/style.css` | HTTP 200 and non-empty response | **PASS** |
| WEB-04 | Static assets | Request `/static/script.js` | HTTP 200 and non-empty response | **PASS** |
| JOB-01 | Add job | Submit T1 with memory 30K, burst 4, arrival 0, priority 1 | Redirect; one T1 job is created | **PASS** |
| JOB-02 | Duplicate validation | Submit another job with ID `t1` | Case-insensitive duplicate is ignored | **PASS** |
| JOB-03 | Required-field handling | Submit with a blank job ID | Redirect; no additional job is created | **PASS** |
| JOB-04 | Add job | Submit T2 with memory 50K, burst 5, arrival 1, priority 2 | A second job is created | **PASS** |
| MEM-01 | First-Fit | Run First-Fit with T1 (30K) and T2 (50K) | T1 is allocated to first fitting hole H1 | **PASS** |
| MEM-02 | Best-Fit | Run Best-Fit with T1 (30K) and T2 (50K) | T1 is allocated to smallest fitting hole H1 | **PASS** |
| MEM-03 | Reset memory | Run Reset Memory | All memory holes are free and have no assigned job | **PASS** |
| CPU-01 | FCFS | Run FCFS | Scheduler selects FCFS and returns results for four built-in sample processes | **PASS** |
| CPU-02 | Round Robin | Run Round Robin | Scheduler selects Round Robin and returns results for four built-in sample processes | **PASS*** |
| STATE-01 | Process states | Set T1 state to Waiting | T1's state changes to Waiting | **PASS** |
| DEV-01 | Printer | Request printer for T1 while available | Printer becomes busy | **PASS** |
| DEV-02 | Printer queue | Request printer for T2 while printer is busy | T2 is added to the waiting queue | **PASS** |
| DEV-03 | Printer queue | Release printer with T2 waiting | T2 is removed from the queue and printer remains busy | **PASS** |
| DEV-04 | Printer | Release printer with no queued process | Printer becomes available | **PASS** |
| LOG-01 | Event log | Confirm actions have added events | Event history is non-empty | **PASS** |
| LOG-02 | Event log | Select Clear Log | Event history is empty | **PASS** |
| WEB-05 | Regression | Request homepage after the actions above | HTTP 200 | **PASS** |
| DEP-01 | Vercel config | Parse `vercel.json` and inspect catch-all route | Route destination is `api/index.py` | **PASS** |

\* The Round Robin check verified that the route ran and returned four results; it did **not** validate the schedule's timing correctness. The run printed a `P2` slice from time 19 to 19. See Follow-up Tests.

## Follow-up Tests Not Run

| ID | Area | Test | Expected result | Status |
|---|---|---|---|---|
| VAL-01 | Form validation | Submit missing memory, CPU burst, arrival time, or priority | Invalid submission is rejected without creating a job | Not run |
| VAL-02 | Form validation | Try zero/negative memory, burst, and priority in a browser | Browser validation prevents values below the form's minimums | Not run |
| VAL-03 | Form validation | Submit non-numeric values directly to `/add-job` | Invalid submission is rejected without creating a job | Not run |
| MEM-04 | Memory limits | Submit a job larger than every memory hole and allocate it | Job is reported as not allocated; no hole is incorrectly assigned | Not run |
| CPU-03 | Round Robin correctness | Check every Gantt interval for positive duration, correct time progression, and completion | No zero-duration slices; process completion/waiting/turnaround times are correct | Not run; zero-duration P2 slice was observed |
| CPU-04 | CPU display | Run FCFS and Round Robin from the website and inspect visible results | Results/metrics expected by the UI are displayed | Not run; current page appears to show only the input process table and event log |
| DEV-05 | Empty printer form | Submit printer request with no process selected | Request is rejected without changing printer or queue | Not run |
| NAV-01 | Browser navigation | Click each navigation link and action control | Correct section or action opens without browser errors | Not run in a real browser |
| UI-01 | Responsive layout | Inspect the website at desktop and mobile viewport sizes | Controls and text remain visible and usable without overlap | Not run |
| DEP-02 | Live deployment | Deploy the repository on Vercel and exercise its public URL | Site and assets load; form actions work in deployment | Not run |
| DEP-03 | Persistence | Add a job and revisit after a new request, cold start, or redeploy | Data persists only if durable storage is configured | Not run; current simulator stores data in process memory |

## Notes

- CPU scheduling currently operates on four built-in sample processes, not the jobs entered through the website.
- The local checks do not prove that Vercel can build or serve the live deployment; that requires deploying and testing the Vercel URL.
