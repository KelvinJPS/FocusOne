import Xlib
import Xlib.display
from ewmh import EWMH
from notifypy import Notify

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

