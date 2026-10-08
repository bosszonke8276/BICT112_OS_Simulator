class DeviceManager:

    def __init__(self):
        self.printer_available = True
        self.waiting_queue = []

    def request_printer(self, process_id):

        if self.printer_available:

            self.printer_available = False

            print(
                f"{process_id} has been allocated the printer."
            )

        else:

            self.waiting_queue.append(process_id)

            print(
                f"{process_id} has been placed in the printer queue."
            )

    def release_printer(self):

        if len(self.waiting_queue) > 0:

            next_process = self.waiting_queue.pop(0)

            print(
                f"Printer released and allocated to "
                f"{next_process}."
            )

            self.printer_available = False

        else:

            self.printer_available = True

            print("Printer is now available.")

    def display_status(self):

        print("\n===== PRINTER STATUS =====")

        if self.printer_available:
            print("Printer: Available")
        else:
            print("Printer: Busy")

        if len(self.waiting_queue) == 0:
            print("Waiting Queue: Empty")
        else:
            print(
                "Waiting Queue:",
                ", ".join(self.waiting_queue)
            )

    def device_menu(self):

        while True:

            print("\n===== DEVICE MANAGER =====")
            print("1. Request Printer")
            print("2. Release Printer")
            print("3. Display Printer Status")
            print("4. Return to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":

                process_id = input(
                    "Enter Process ID: "
                )

                self.request_printer(process_id)

            elif choice == "2":

                self.release_printer()

            elif choice == "3":

                self.display_status()

            elif choice == "4":

                break

            else:

                print("Invalid choice.")