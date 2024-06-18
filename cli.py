import argparse
import app

def main():
    parser = argparse.ArgumentParser(
        prog='FocusOne',
        description='Focus on one task for a period of time',
        epilog='Get thigns done!')

    parser.add_argument('name', help="name of the task")
    parser.add_argument('time', help="time to focus on the task in format:") 
    parser.add_argument('-desc', '--description')
    parser.add_argument('-d','--date', help='date in which the task will be perfomed')
    parser.add_argument('-p','--programs',help='list of programs allowed ')
    parser.add_argument('-w','--websites',help='list of websites allowed')
    parser.add_argument('-a','--action',help='action to be perfomed during block')
    parser.add_argument('-l','--list tasks', help='list tasks')


    args = parser.parse_args()
    app.add_task(name=args.name,time=args.time)




if __name__ == "__main__":
    main()
