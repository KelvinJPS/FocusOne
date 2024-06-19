import argparse
from os import name
import app

def main():
    parser = argparse.ArgumentParser(
        prog='FocusOne',
        description='Focus on one task for a period of time',
        epilog='Get thigns done!')
    
    subparsers = parser.add_subparsers()
    parser_add = subparsers.add_parser('add',help="add tasks")
    parser_add.add_argument('name', help="name of the task")
    parser_add.add_argument('time', help="time to focus on the task in format:") 
    parser_add.add_argument('-desc', '--description')
    parser_add.add_argument('-d','--date', help='date in which the task will be perfomed')
    parser_add.add_argument('-p','--programs',help='list of programs allowed ')
    parser_add.add_argument('-w','--websites',help='list of websites allowed')

    parser.add_argument('-l','--list_tasks', help='list tasks',
                        action='store_true')

    
    args = parser.parse_args()
    if args.list_tasks:
        app.get_tasks()
    
    else:
        app.add_task(name=args.name,time=args.date)



if __name__ == "__main__":
    main()
