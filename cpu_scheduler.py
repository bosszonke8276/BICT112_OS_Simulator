from process import Process


class CPUScheduler:

    def __init__(self):

        self.processes = [
            Process("P1", 0, 7, 2, 55),
            Process("P2", 1, 4, 1, 35),
            Process("P3", 2, 9, 3, 80),
            Process("P4", 4, 5, 2, 60)
        ]

        # Data used by the website
        self.last_algorithm = ""
        self.results = []
        self.gantt = []

        self.average_waiting = 0
        self.average_turnaround = 0

    # ==================================================
    # RESET PROCESSES
    # ==================================================

    def reset_processes(self):

        self.processes = [
            Process("P1", 0, 7, 2, 55),
            Process("P2", 1, 4, 1, 35),
            Process("P3", 2, 9, 3, 80),
            Process("P4", 4, 5, 2, 60)
        ]

    # ==================================================
    # DISPLAY PROCESSES
    # ==================================================

    def display_processes(self):

        print("\n--- CPU Processes ---")
        print("-" * 75)

        print(
            f"{'ID':<8}"
            f"{'Arrival':<10}"
            f"{'Burst':<10}"
            f"{'Priority':<10}"
            f"{'Memory':<10}"
            f"{'State':<15}"
        )

        print("-" * 75)

        for process in self.processes:

            print(
                f"{process.process_id:<8}"
                f"{process.arrival_time:<10}"
                f"{process.burst_time:<10}"
                f"{process.priority:<10}"
                f"{process.memory:<10}"
                f"{process.state:<15}"
            )

        print("-" * 75)

    # ==================================================
    # FCFS
    # ==================================================

    def fcfs(self):

        self.reset_processes()

        self.last_algorithm = "FCFS"

        self.results = []
        self.gantt = []

        print("\n===== FIRST COME FIRST SERVED (FCFS) =====")

        current_time = 0

        for process in self.processes:

            # Handle CPU idle time
            if current_time < process.arrival_time:

                current_time = process.arrival_time

            process.set_state("Running")

            start_time = current_time

            current_time += process.burst_time

            process.completion_time = current_time

            process.set_state("Terminated")

            process.calculate_times()

            # Store Gantt information
            self.gantt.append({
                "id": process.process_id,
                "start": start_time,
                "end": current_time
            })

            # Store result
            self.results.append({
                "id": process.process_id,
                "arrival": process.arrival_time,
                "burst": process.burst_time,
                "priority": process.priority,
                "completion": process.completion_time,
                "waiting": process.waiting_time,
                "turnaround": process.turnaround_time
            })

            print(
                f"{process.process_id}: "
                f"Start = {start_time}, "
                f"Completion = {process.completion_time}, "
                f"Waiting = {process.waiting_time}, "
                f"Turnaround = {process.turnaround_time}"
            )

        self.calculate_averages()

        return self.results

    # ==================================================
    # ROUND ROBIN
    # ==================================================

    def round_robin(self, quantum=3):

        self.reset_processes()

        self.last_algorithm = "Round Robin"

        self.results = []
        self.gantt = []

        print("\n===== ROUND ROBIN =====")
        print(f"Time Quantum = {quantum}")

        current_time = 0

        queue = []

        completed = 0

        processes = sorted(
            self.processes,
            key=lambda process: process.arrival_time
        )

        # Keep track of processes already placed
        # into the ready queue
        added = set()

        while completed < len(processes):

            # ------------------------------------------
            # ADD ARRIVED PROCESSES
            # ------------------------------------------

            for process in processes:

                if (
                    process.arrival_time <= current_time
                    and process.process_id not in added
                    and process.remaining_time > 0
                ):

                    queue.append(process)

                    added.add(
                        process.process_id
                    )

            # ------------------------------------------
            # CPU IDLE
            # ------------------------------------------

            if len(queue) == 0:

                current_time += 1

                continue

            # ------------------------------------------
            # GET NEXT PROCESS
            # ------------------------------------------

            process = queue.pop(0)

            process.set_state("Running")

            start_time = current_time

            execution_time = min(
                quantum,
                process.remaining_time
            )

            current_time += execution_time

            process.remaining_time -= execution_time

            # ------------------------------------------
            # GANTT CHART
            # ------------------------------------------

            self.gantt.append({
                "id": process.process_id,
                "start": start_time,
                "end": current_time
            })

            print(
                f"{process.process_id} runs from "
                f"{start_time} to {current_time}"
            )

            # ------------------------------------------
            # ADD NEW ARRIVALS
            # ------------------------------------------

            for new_process in processes:

                if (
                    new_process.arrival_time <= current_time
                    and new_process.remaining_time > 0
                    and new_process != process
                    and new_process not in queue
                ):

                    queue.append(new_process)

            # ------------------------------------------
            # PROCESS FINISHED?
            # ------------------------------------------

            if process.remaining_time > 0:

                process.set_state("Ready")

                queue.append(process)

            else:

                process.set_state("Terminated")

                process.completion_time = current_time

                process.calculate_times()

                completed += 1

        # ------------------------------------------
        # STORE RESULTS
        # ------------------------------------------

        for process in processes:

            self.results.append({
                "id": process.process_id,
                "arrival": process.arrival_time,
                "burst": process.burst_time,
                "priority": process.priority,
                "completion": process.completion_time,
                "waiting": process.waiting_time,
                "turnaround": process.turnaround_time
            })

        # Keep P1, P2, P3, P4 order
        self.results.sort(
            key=lambda result: result["id"]
        )

        self.calculate_averages()

        return self.results

    # ==================================================
    # CALCULATE AVERAGES
    # ==================================================

    def calculate_averages(self):

        if len(self.results) == 0:

            self.average_waiting = 0

            self.average_turnaround = 0

            return

        total_waiting = 0

        total_turnaround = 0

        for result in self.results:

            total_waiting += result["waiting"]

            total_turnaround += result["turnaround"]

        self.average_waiting = round(
            total_waiting / len(self.results),
            2
        )

        self.average_turnaround = round(
            total_turnaround / len(self.results),
            2
        )

    # ==================================================
    # DISPLAY AVERAGES
    # ==================================================

    def display_averages(self):

        print("\n--- PROCESS RESULTS ---")
        print("-" * 60)

        for result in self.results:

            print(
                f"{result['id']}: "
                f"Waiting Time = {result['waiting']}, "
                f"Turnaround Time = {result['turnaround']}"
            )

        print("-" * 60)

        print(
            "Average Waiting Time:",
            self.average_waiting
        )

        print(
            "Average Turnaround Time:",
            self.average_turnaround
        )

    # ==================================================
    # TERMINAL MENU
    # ==================================================

    def scheduler_menu(self):

        while True:

            print("\n===== CPU SCHEDULER =====")

            print("1. Display Processes")

            print("2. FCFS")

            print("3. Round Robin")

            print("4. Return to Main Menu")

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":

                self.display_processes()

            elif choice == "2":

                self.fcfs()

                self.display_averages()

            elif choice == "3":

                self.round_robin()

                self.display_averages()

            elif choice == "4":

                break

            else:

                print("Invalid choice.")