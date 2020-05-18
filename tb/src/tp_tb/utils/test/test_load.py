import sys
from tb_utils import events, utils
from argparse import ArgumentParser


def main():

    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename",
        default="/home/dantrim/work/tdaq-htt-firmware/testvecs/20200124/BoardToBoardInput_AMTP0_Pixel0.evt",
    )
    parser.add_argument(
        "--ids", action="store_true", default=False, help="Print L0IDs of loaded events"
    )
    parser.add_argument(
        "-n", "--n-events", default=-1, help="Number of events to load [default:all]"
    )
    parser.add_argument(
        "--l0id", default="", help="Load data for specific l0id (hex string)"
    )
    parser.add_argument("--dump", action="store_true", default=False)
    args = parser.parse_args()

    loaded_events = events.load_events_from_file(
        filename=args.filename, n_to_load=int(args.n_events)
    )

    if args.l0id:
        tmp = []
        for le in loaded_events:
            if le.l0id == int(args.l0id, 16):
                tmp.append(le)
                break
        if len(tmp) == 0:
            print("No events with requested L0ID (={})".format(args.l0id))
            sys.exit()
        loaded_events = tmp

    print("Loaded {} events".format(len(loaded_events)))

    if args.ids:
        for i, l in enumerate(loaded_events):
            print("{:02}: {}".format(i, hex(l.l0id)))

    else:
        for i, l in enumerate(loaded_events):
            print("Event {:02}: {}".format(i, l))

    if args.dump and loaded_events:
        event = loaded_events[0]
        for iword, word in enumerate(event):
            print(word.hex())


if __name__ == "__main__":
    main()
