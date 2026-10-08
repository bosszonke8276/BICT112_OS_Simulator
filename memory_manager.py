class MemoryManager:

    def __init__(self):

        # Memory holes
        self.holes = [
            {
                "name": "H1",
                "size": 40,
                "free": True,
                "job": None
            },
            {
                "name": "H2",
                "size": 95,
                "free": True,
                "job": None
            },
            {
                "name": "H3",
                "size": 60,
                "free": True,
                "job": None
            },
            {
                "name": "H4",
                "size": 130,
                "free": True,
                "job": None
            }
        ]

        # Jobs will come from the website
        self.jobs = []

        # Website results
        self.last_algorithm = ""
        self.allocations = []

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        for hole in self.holes:

            hole["free"] = True
            hole["job"] = None

        self.allocations = []
        self.last_algorithm = ""

    # ==================================================
    # DISPLAY HOLES
    # ==================================================

    def display_holes(self):

        print("\n===== MEMORY HOLES =====")
        print("-" * 50)

        for hole in self.holes:

            if hole["free"]:

                status = "Free"

            else:

                status = (
                    f"Allocated to {hole['job']}"
                )

            print(
                f"{hole['name']} : "
                f"{hole['size']}K - {status}"
            )

        print("-" * 50)

    # ==================================================
    # FIRST-FIT
    # ==================================================

    def first_fit(self):

        self.reset()

        self.last_algorithm = "First-Fit"

        print("\n===== FIRST-FIT ALLOCATION =====")
        print("-" * 50)

        for job in self.jobs:

            allocated = False

            for hole in self.holes:

                if (
                    hole["free"]
                    and hole["size"] >= job["size"]
                ):

                    hole["free"] = False

                    hole["job"] = job["name"]

                    self.allocations.append({
                        "job": job["name"],
                        "job_size": job["size"],
                        "hole": hole["name"],
                        "hole_size": hole["size"],
                        "status": "Allocated"
                    })

                    print(
                        f"{job['name']} "
                        f"({job['size']}K) "
                        f"allocated to "
                        f"{hole['name']} "
                        f"({hole['size']}K)"
                    )

                    allocated = True

                    break

            if not allocated:

                self.allocations.append({
                    "job": job["name"],
                    "job_size": job["size"],
                    "hole": "Not Allocated",
                    "hole_size": 0,
                    "status": "Failed"
                })

                print(
                    f"{job['name']} "
                    f"({job['size']}K) "
                    f"could not be allocated"
                )

        return self.allocations

    # ==================================================
    # BEST-FIT
    # ==================================================

    def best_fit(self):

        self.reset()

        self.last_algorithm = "Best-Fit"

        print("\n===== BEST-FIT ALLOCATION =====")
        print("-" * 50)

        for job in self.jobs:

            possible_holes = []

            for hole in self.holes:

                if (
                    hole["free"]
                    and hole["size"] >= job["size"]
                ):

                    possible_holes.append(hole)

            if len(possible_holes) > 0:

                best_hole = possible_holes[0]

                for hole in possible_holes:

                    if (
                        hole["size"]
                        < best_hole["size"]
                    ):

                        best_hole = hole

                best_hole["free"] = False

                best_hole["job"] = job["name"]

                self.allocations.append({
                    "job": job["name"],
                    "job_size": job["size"],
                    "hole": best_hole["name"],
                    "hole_size": best_hole["size"],
                    "status": "Allocated"
                })

                print(
                    f"{job['name']} "
                    f"({job['size']}K) "
                    f"allocated to "
                    f"{best_hole['name']} "
                    f"({best_hole['size']}K)"
                )

            else:

                self.allocations.append({
                    "job": job["name"],
                    "job_size": job["size"],
                    "hole": "Not Allocated",
                    "hole_size": 0,
                    "status": "Failed"
                })

                print(
                    f"{job['name']} "
                    f"({job['size']}K) "
                    f"could not be allocated"
                )

        return self.allocations

    # ==================================================
    # TERMINAL MENU
    # ==================================================

    def memory_menu(self):

        while True:

            print(
                "\n===== MEMORY MANAGEMENT ====="
            )

            print("1. Display Memory Holes")
            print("2. First-Fit")
            print("3. Best-Fit")
            print("4. Reset Memory")
            print("5. Return to Main Menu")

            choice = input(
                "Enter your choice: "
            )

            if choice == "1":

                self.display_holes()

            elif choice == "2":

                self.first_fit()

            elif choice == "3":

                self.best_fit()

            elif choice == "4":

                self.reset()

                print(
                    "Memory has been reset."
                )

            elif choice == "5":

                break

            else:

                print("Invalid choice.")