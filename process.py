class Process:

    def __init__(
        self,
        process_id,
        arrival_time,
        burst_time,
        priority,
        memory
    ):

        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.memory = memory

        self.remaining_time = burst_time

        self.state = "Ready"

        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

    def set_state(self, state):

        self.state = state

    def calculate_times(self):

        self.turnaround_time = (
            self.completion_time
            - self.arrival_time
        )

        self.waiting_time = (
            self.turnaround_time
            - self.burst_time
        )

    def display(self):

        print(
            f"{self.process_id:<8}"
            f"{self.memory:<10}"
            f"{self.arrival_time:<10}"
            f"{self.burst_time:<10}"
            f"{self.priority:<10}"
            f"{self.state:<15}"
        )