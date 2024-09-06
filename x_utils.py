from os import close
import Xlib
import Xlib.display
from ewmh import EWMH

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

def close_programs(programs):
    open_programs = get_open_programs()
    for program in programs:
        program = program.lower()
        if any(program == p.lower() for p in open_programs):
            print("found")
            print(program)
    
if __name__ == "__main__":
    close_programs(['firefox','alacritty'])
