import argparse
import bridgescape
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?')
    parsed_args = parser.parse_args()

    parsed_lin = bridgescape.linparse.extract_deals(parsed_args.file)
    
    board_no = 1
    for line in parsed_lin:
        print('qx|o{0},Bd {0}|rh||ah|Bd {0}|{1}|sk||pg|mc|6|pg||'.format(board_no, line))
        board_no += 1

if __name__ == "__main__":
    main()