import argparse
import focusone
import os 
from datetime import date, datetime

def main():
    parser = argparse.ArgumentParser(
        prog='focusone',
        description='focus on one task for a period of time',
        epilog='get things done!'
    )
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    subparsers = parser.add_subparsers(dest='command')

    parser_add = subparsers.add_parser('add', help="add a new task")
    
    # add command 
    parser_add.add_argument('name', help="name of the task")
    parser_add.add_argument('time', nargs='+', help="time to focus on the task (e.g., '1h 45m')")
    parser_add.add_argument('-desc', '--description', help="description of the task")
    parser_add.add_argument('-d', '--date', help="date when the task will be performed")
    parser_add.add_argument('-p', '--programs', help="list of allowed programs")
    parser_add.add_argument('-w', '--websites', help="list of allowed websites")
    
    # show command 
    parser_show = subparsers.add_parser('show', help="show current task and time")
    parser_show.add_argument('--bar', action='store_true', help="Option for bars, the output will not be buffered")
    args = parser.parse_args()

    if args.command == 'add':
        # combine time arguments
        time_input = ' '.join(args.time)
        s_time = focusone.parse_time(time_input)
        if args.date == None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            focusone.add_block(args.name, s_time,date=date,active=1)

        else:
            focusone.add_block(args.name, s_time,date=args.date,active=0)

    if args.command == 'show':
        if args.bar:
            focusone.show_act(bar_opt=True)
    else:
        focusone.show_act()

 
    

if __name__ == "__main__":
    main()
