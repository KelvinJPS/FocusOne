import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='FocusOne',
        description='Focus on one task for a period of time',
        epilog='Get thigns done!')

    # positional argument
    parser.add_argument('-n', '--name', required=True, help="name of the task")
    parser.add_argument('-t', '--time', type=int,
                        help="time to focus on the task in format:",
                        required=True)
    parser.add_argument('-d', '--description')
    parser.add_argument('-p','--list of programs allowed ')
    parser.add_argument('-w','--list of websites allowed')
    parser.add_argument('a','--action to perfom during block')
    
    parser.parse_args()


if __name__ == "__main__":
    main()
