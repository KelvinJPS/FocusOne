import Xlib
import Xlib.display
from ewmh import EWMH
from notifypy import Notify
import json
import sys
import struct

ewmh = EWMH()


def get_open_programs():
    ewmh = EWMH()
    programs = set()

    for window in ewmh.getClientList():
        try:
            window_class = window.get_wm_class()
            if window_class and len(window_class) > 1:
                program_name = window_class[1]
                programs.add(program_name)
        except Xlib.error.BadWindow:
            pass  # Window has been destroyed

    return programs


def close_programs(allowed_programs):
    active_window = ewmh.getActiveWindow()

    # Check if the active window is valid
    if active_window:
        # Get the window's class (which includes the program name)
        window_class = active_window.get_wm_class()

        if window_class:
            # The second element is typically the program name
            program_name = window_class[1].lower()
            if program_name not in (p.lower() for p in allowed_programs):
                ewmh.setCloseWindow(active_window)
                ewmh.display.flush()
                notification = Notify()
                notification.title = "Focusone"
                notification.message = "program not allowed, Focus!"
                notification.send()

            else:
                pass

    else:
        pass


def send_to_browser_extension(allowed_websites):
    message = json.dumps({"allowed_websites": allowed_websites})
    # Write message size as 4 byte unsigned integer (native messaging protocol)
    sys.stdout.buffer.write(struct.pack("<I", len(message)))
    sys.stdout.buffer.write(message.encode("utf-8"))
    sys.stdout.flush()


def parse_time(time_input: str) -> int:
    """Convert natural language time input into seconds. Example: '1h 30m 45s' to 5445 seconds."""

    if not time_input.strip():
        raise ValueError("Input string is empty or invalid")

    time_units = {"h": 3600, "m": 60, "s": 1}

    time_input = time_input.split()
    time_parsed = 0

    if len(time_input) > 3:
        raise ValueError("More than 3 time units are not allowed")

    for time in time_input:
        time_tail = time[-1]
        try:
            n = int(time[:-1])
        except ValueError:
            raise ValueError(
                f"Invalid time value: '{time[:-1]}' cannot be converted to an integer"
            )

        if time_tail in time_units:
            time_parsed += n * time_units[time_tail]
        else:
            raise ValueError(f"Invalid time unit: '{time_tail}'")

    return time_parsed
