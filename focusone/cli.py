import argparse
import os
from datetime import date, datetime

import focusone.core
import focusone.utils
import focusone.blocks_db


def main():
    parser = argparse.ArgumentParser(
        prog="focusone",
        description="focus on one task for a period of time",
        epilog="get things done!",
    )
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    subparsers = parser.add_subparsers(dest="command")

    parser_start = subparsers.add_parser("start", help="start a new focus session")

    # add command
    parser_start.add_argument("name", help="name of the task")
    parser_start.add_argument(
        "time", nargs="*", help="time to focus on the task (e.g., '1h 45m')"
    )
    parser_start.add_argument("-desc", "--description", help="description of the task")
    parser_start.add_argument(
        "-d", "--date", help="date when the task will be performed"
    )
    parser_start.add_argument(
        "-p", "--programs", nargs="+", help="list of allowed programs"
    )
    parser_start.add_argument("-w", "--websites", help="list of allowed websites")

    # show command
    parser_show = subparsers.add_parser("show", help="show current task and time")
    parser_show.add_argument(
        "--bar",
        action="store_true",
        help="Option for bars, the output will not be buffered",
    )
    args = parser.parse_args()

    if args.command == "start":
        # validate time is present
        if not args.time:
            parser_start.error("Time argument is required")

        time_input = " ".join(args.time)
        s_time = focusone.utils.parse_time(time_input)

        # if not focusone.core is provided, date is now
        if args.date == None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            active = 1

        else:
            date = args.date
            active = 0

        focusone.core.start_focus_session(
            duration=s_time,
            block_name=args.name,
            programs_allowed=args.programs if args.programs else [],
            websites_allowed=args.websites if args.websites else [],
        )

    if args.command == "show":
        block_act = focusone.d.get_act_block()
        if args.bar:
            focusone.core.show_progress(
                title=block_act["name"],
                duration_seconds=block_act["duration"],
                bar_opt=True,
            )
        else:
            focusone.core.show_progress(
                title=block_act["name"],
                duration_seconds=block_act["duration"],
                bar_opt=False,
            )


if __name__ == "__main__":
    main()
