import json
from argparse import ArgumentParser

from tb_utils import result_handler


def main() :

    parser = ArgumentParser(description = "Dump test summary results from test summary json output from tests.")
    parser.add_argument("-i", "--inputs", nargs = "*", help = "Input *.json files")
    parser.add_argument("--event-detail", action = "store_true", default = False,
        help = "Print out more detailed event info"
    )
    args = parser.parse_args()
    inputs = sorted(args.inputs)
    test_results = []
    for input_file in inputs :
        with open(input_file, "r") as json_file :
            data = json.load(json_file)
            test_results.append(data)
    result_handler.dump_test_results(test_results, event_detail = args.event_detail)

if __name__ == "__main__" :
    main()
