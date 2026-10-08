from flask import Flask, render_template, request, redirect, url_for

from simulator import OSSimulator

app = Flask(__name__)

simulator = OSSimulator()


@app.route("/")
def index():

    return render_template(
        "index.html",
        jobs=simulator.jobs,
        event_log=simulator.event_log,
        memory_holes=simulator.memory_manager.holes,
        printer_available=simulator.device_manager.printer_available,
        printer_queue=simulator.device_manager.waiting_queue
    )


@app.route("/add-job", methods=["POST"])
def add_job():

    job_id = request.form.get("job_id", "").strip()
    memory = request.form.get("memory", "")
    cpu_burst = request.form.get("cpu_burst", "")
    arrival_time = request.form.get("arrival_time", "")
    priority = request.form.get("priority", "")

    # Basic validation
    if not job_id or not memory or not cpu_burst:
        return redirect(url_for("index"))

    try:
        memory = int(memory)
        cpu_burst = int(cpu_burst)
        arrival_time = int(arrival_time)
        priority = int(priority)

    except ValueError:
        return redirect(url_for("index"))

    # Check duplicate ID
    for job in simulator.jobs:

        if job.process_id.lower() == job_id.lower():

            return redirect(url_for("index"))

    # Create process
    from process import Process

    job = Process(
        job_id,
        arrival_time,
        cpu_burst,
        priority,
        memory
    )

    simulator.jobs.append(job)

    message = f"{job_id} added to the Ready queue."

    simulator.event_log.append(message)

    return redirect(url_for("index"))


@app.route("/memory/<algorithm>")
def memory_algorithm(algorithm):

    # Get the jobs entered on the website
    simulator.memory_manager.jobs = [
        {
            "name": job.process_id,
            "size": job.memory
        }
        for job in simulator.jobs
    ]

    if algorithm == "first-fit":

        simulator.memory_manager.first_fit()

        simulator.event_log.append(
            "First-Fit memory allocation was executed."
        )

    elif algorithm == "best-fit":

        simulator.memory_manager.best_fit()

        simulator.event_log.append(
            "Best-Fit memory allocation was executed."
        )

    return redirect(
        url_for("index")
    )


@app.route("/memory/reset")
def reset_memory():

    simulator.memory_manager.reset()

    simulator.event_log.append(
        "Memory was reset."
    )

    return redirect(url_for("index"))


@app.route("/cpu/<algorithm>")
def cpu_algorithm(algorithm):

    if algorithm == "fcfs":

        simulator.cpu_scheduler.fcfs()

        simulator.event_log.append(
            "FCFS CPU scheduling was executed."
        )

    elif algorithm == "round-robin":

        simulator.cpu_scheduler.round_robin(3)

        simulator.event_log.append(
            "Round Robin CPU scheduling was executed with quantum 3."
        )

    return redirect(url_for("index"))


@app.route("/process-state", methods=["POST"])
def process_state():

    process_id = request.form.get("process_id")
    new_state = request.form.get("state")

    for job in simulator.jobs:

        if job.process_id.lower() == process_id.lower():

            job.set_state(new_state)

            message = (
                f"{job.process_id} state changed to {new_state}."
            )

            simulator.event_log.append(message)

            break

    return redirect(url_for("index"))


@app.route("/printer/request", methods=["POST"])
def printer_request():

    process_id = request.form.get("process_id")

    if process_id:

        simulator.device_manager.request_printer(process_id)

        simulator.event_log.append(
            f"{process_id} requested the printer."
        )

    return redirect(url_for("index"))


@app.route("/printer/release")
def printer_release():

    simulator.device_manager.release_printer()

    simulator.event_log.append(
        "Printer was released."
    )

    return redirect(url_for("index"))


@app.route("/clear-log")
def clear_log():

    simulator.event_log.clear()

    return redirect(url_for("index"))


if __name__ == "__main__":

    app.run(
        debug=True
    )