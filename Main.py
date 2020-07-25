from argparse import ArgumentParser
from Utils.Dijkstra import exe

parser = ArgumentParser()

RAIN = None
RUNTIME_OUTPUT = None
SAVE_OUTPUT = None


def arguments():
    global parser, RAIN, RUNTIME_OUTPUT, SAVE_OUTPUT

    choices = list(range(302))
    parser.add_argument('Start',
                        help='Where start your trip. [0 to 301]',
                        type=int,
                        metavar='START',
                        choices=choices)
    parser.add_argument('Finish',
                        help='Where finish yor trip. [0 to 301]',
                        type=int,
                        metavar='FINISH',
                        choices=choices)
    parser.add_argument('-r', '--rain',
                        help='If enable, it activates the rain time',
                        action='store_true')
    parser.add_argument('-o', '--runtime_output',
                        help='If enable, it shows graphics in runtime',
                        action='store_true')
    parser.add_argument('-s', '--save_output',
                        help='If enable, it saves graphics in two files',
                        action='store_true')
    args = parser.parse_args()

    RAIN = args.rain
    RUNTIME_OUTPUT = args.runtime_output
    SAVE_OUTPUT = args.save_output

    return args.Start, args.Finish


if __name__ == '__main__':
    node_1, node_2 = arguments()

    if RAIN is None:
        RAIN = False
    if RUNTIME_OUTPUT is None:
        RUNTIME_OUTPUT = False
    if SAVE_OUTPUT is None:
        RUNTIME_OUTPUT = False

    exe(node_1, node_2, RAIN, RUNTIME_OUTPUT, SAVE_OUTPUT)
