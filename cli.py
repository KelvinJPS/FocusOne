import argparse
import focusone

def main():
    parser = argparse.ArgumentParser(
        prog='FocusOne',
        description='Focus on one task for a period of time',
        epilog='Get things done!'
    )
    
    subparsers = parser.add_subparsers(dest='command')

    parser_add = subparsers.add_parser('add', help="Add a new task")
    parser_add.add_argument('name', help="Name of the task")
    parser_add.add_argument('time', nargs='+', help="Time to focus on the task (e.g., '1h 45m')")
    parser_add.add_argument('-desc', '--description', help="Description of the task")
    parser_add.add_argument('-d', '--date', help="Date when the task will be performed")
    parser_add.add_argument('-p', '--programs', help="List of allowed programs")
    parser_add.add_argument('-w', '--websites', help="List of allowed websites")

    args = parser.parse_args()

    if args.command == 'add':
        # Combine time arguments
        time_input = ' '.join(args.time)
        focusone.parse_time(time_input)
        seconds = focusone.parse_time(time_input)
        print(seconds)
        

if __name__ == "__main__":
    main()

