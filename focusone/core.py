import threading
import time
import focusone.utils
import json
import os


def block_distractions(programs, websites, stop_event):
    while not stop_event.is_set():
        if programs:
            focusone.utils.close_programs(allowed_programs=programs)
        if websites:
            block_websites(websites)
        time.sleep(1)  # Check the stop_event every second


def block_websites(allowed_websites):
    try:
        focusone.utils.send_to_browser_extension(allowed_websites)
    except Exception as e:
        print(f"Error communicating with browser extension: {e}")


def save_timer_state(title, end_time, duration_seconds):
    state = {
        "title": title,
        "end_time": end_time,
        "duration": duration_seconds,
        "running": True,
    }
    with open("/tmp/focusone.state", "w") as f:
        json.dump(state, f)


def show_progress(duration_seconds, title, bar_opt):
    # Save initial state when timer starts
    end_time = time.time() + int(duration_seconds)
    save_timer_state(title, end_time, duration_seconds)

    while duration_seconds > 0:
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        timer = f"{title} {hours:02d}:{minutes:02d}:{secs:02d}"
        if bar_opt:
            print(timer, flush=True)
        else:
            print(timer, end="\r")
        duration_seconds -= 1
        time.sleep(1)

    # Clean up state when done
    if os.path.exists("/tmp/focusone.state"):
        os.remove("/tmp/focusone.state")


def start_focus_session(
    duration, block_name, programs_allowed=None, websites_allowed=None
):
    stop_event = threading.Event()
    timer_thread = threading.Thread(
        target=show_progress, args=(duration, block_name, False)
    )

    if programs_allowed or websites_allowed:
        blocker_thread = threading.Thread(
            target=block_distractions,
            args=(programs_allowed or [], websites_allowed or [], stop_event),
        )
        blocker_thread.start()

    timer_thread.start()
    timer_thread.join()

    if programs_allowed or websites_allowed:
        stop_event.set()  # Signal the blocker to stop
        blocker_thread.join()  # Wait for the blocker to finish


def get_act_block():
    try:
        with open("/tmp/focusone.state", "r") as f:
            state = json.load(f)
            remaining = state["end_time"] - time.time()
            if remaining > 0:
                return {"name": state["title"], "duration": int(remaining)}
    except (FileNotFoundError, json.JSONDecodeError):
        pass
