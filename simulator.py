from process import Process
from memory_manager import MemoryManager
from cpu_scheduler import CPUScheduler
from device_manager import DeviceManager


class OSSimulator:

    def __init__(self):

        self.jobs = []
        self.event_log = []

        self.memory_manager = MemoryManager()
        self.cpu_scheduler = CPUScheduler()
        self.device_manager = DeviceManager()

    # -------------------------------
    # ADD JOB
    # -------------------------------

    def add_job(self):

        print("\n--- Add New Job / Process ---")

        # Validate Job ID
        while True:

            job_id = input("Enter Job ID/name: ").strip()

            if job_id == "":
                print("ERROR: Job ID/name cannot be blank.")

            elif any(
                job.process_id.lower() == job_id.lower()
                for job in self.jobs
            ):
                print("ERROR: A job with that ID already exists.")

            else:
                break

        # Validate memory
        while True:

            try:

                memory = int(
                    input("Enter memory required (K): ")
                )

                if memory <= 0:
                    print("ERROR: Memory must be greater than 0.")

                else:
                    break

            except ValueError:

                print("ERROR: Please enter a valid number.")

        # Validate CPU burst
        while True:

            try:

                cpu_burst = int(
                    input("Enter CPU burst time: ")
                )

                if cpu_burst <= 0:
                    print(
                        "ERROR: CPU burst must be greater than 0."
                    )

                else:
                    break

            except ValueError:

                print("ERROR: Please enter a valid number.")

        # Arrival time
        while True:

            try:

                arrival_time = int(
                    input("Enter arrival time: ")
                )

                if arrival_time < 0:
                    print(
                        "ERROR: Arrival time cannot be negative."
                    )

                else:
                    break

            except ValueError:

                print("ERROR: Please enter a valid number.")

        # Priority
        while True:

            try:

                priority = int(
                    input("Enter priority: ")
                )

                if priority <= 0:
                    print(
                        "ERROR: Priority must be greater than 0."
                    )

                else:
                    break

            except ValueError:

                print("ERROR: Please enter a valid number.")

        job = Process(
            job_id,
            arrival_time,
            cpu_burst,
            priority,
            memory
        )

        self.jobs.append(job)

        message = f"{job_id} added to the Ready queue."

        self.event_log.append(message)

        print("\nSUCCESS:", message)

    # -------------------------------
    # VIEW JOBS
    # -------------------------------

    def show_jobs(self):

        print("\n--- Jobs / Processes ---")

        if len(self.jobs) == 0:

            print("No jobs have been entered yet.")

            return

        print("-" * 80)

        print(
            f"{'ID':<8}"
            f"{'Memory':<10}"
            f"{'Arrival':<10}"
            f"{'Burst':<10}"
            f"{'Priority':<10}"
            f"{'State':<15}"
        )

        print("-" * 80)

        for job in self.jobs:

            print(
                f"{job.process_id:<8}"
                f"{job.memory:<10}"
                f"{job.arrival_time:<10}"
                f"{job.burst_time:<10}"
                f"{job.priority:<10}"
                f"{job.state:<15}"
            )

        print("-" * 80)

    # -------------------------------
    # EVENT LOG
    # -------------------------------

    def show_event_log(self):

        print("\n--- Event Log ---")

        if len(self.event_log) == 0:

            print("No events recorded yet.")

            return

        for number, event in enumerate(
            self.event_log,
            start=1
        ):

            print(f"{number}. {event}")

    # -------------------------------
    # HELP
    # -------------------------------

    def show_help(self):

        print("""
========================================================
BICT112 OPERATING SYSTEM SIMULATOR - HELP
========================================================

This simulator demonstrates how an operating system
manages computer laboratory resources.

MEMORY MANAGER
- First-Fit
- Best-Fit
- Memory allocation
- Memory reset
- External fragmentation

CPU SCHEDULER
- First Come First Served (FCFS)
- Round Robin
- Waiting time
- Turnaround time
- Time Quantum = 3

PROCESS STATES
- Ready
- Running
- Waiting
- Terminated

DEVICE MANAGER
- Printer allocation
- Printer waiting queue
- Printer release

The simulator is an educational model and does not
represent a real operating system.

========================================================
""")

    # -------------------------------
    # MAIN MENU
    # -------------------------------

    def run(self):

        while True:

            print("""
========================================================
       BICT112 OPERATING SYSTEMS MINI PROJECT
       UMP COMPUTER LABORATORY RESOURCE MANAGER
========================================================

1. Add Job / Process
2. View Jobs
3. Memory Manager
4. CPU Scheduler
5. Process States
6. Device Manager
7. View Event Log
8. Help / About
9. Exit

========================================================
""")

            choice = input(
                "Select an option: "
            ).strip()

            if choice == "1":

                self.add_job()

            elif choice == "2":

                self.show_jobs()

            elif choice == "3":

                self.memory_manager.memory_menu()

            elif choice == "4":

                self.cpu_scheduler.scheduler_menu()

            elif choice == "5":

                self.process_state_menu()

            elif choice == "6":

                self.device_manager.device_menu()

            elif choice == "7":

                self.show_event_log()

            elif choice == "8":

                self.show_help()

            elif choice == "9":

                print("\nSimulator closed.")

                break

            else:

                print(
                    "\nERROR: Please select an option "
                    "from 1 to 9."
                )

    # -------------------------------
    # PROCESS STATE MENU
    # -------------------------------

    def process_state_menu(self):

        while True:

            print("\n===== PROCESS STATE MANAGER =====")

            print("1. View Process States")
            print("2. Set Process to Running")
            print("3. Set Process to Waiting")
            print("4. Set Process to Ready")
            print("5. Terminate Process")
            print("6. Return to Main Menu")

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":

                self.show_jobs()

            elif choice == "2":

                self.change_process_state("Running")

            elif choice == "3":

                self.change_process_state("Waiting")

            elif choice == "4":

                self.change_process_state("Ready")

            elif choice == "5":

                self.change_process_state("Terminated")

            elif choice == "6":

                break

            else:

                print("Invalid choice.")

    # -------------------------------
    # CHANGE PROCESS STATE
    # -------------------------------

    def change_process_state(self, new_state):

        if len(self.jobs) == 0:

            print("No processes available.")

            return

        process_id = input(
            "Enter Process ID: "
        ).strip()

        found = False

        for job in self.jobs:

            if job.process_id.lower() == process_id.lower():

                job.set_state(new_state)

                message = (
                    f"{job.process_id} state changed "
                    f"to {new_state}."
                )

                self.event_log.append(message)

                print("SUCCESS:", message)

                found = True

                break

        if not found:

            print("ERROR: Process not found.")