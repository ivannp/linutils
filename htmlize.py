from jinja2 import Environment, FileSystemLoader

import argparse
import bridgescape as bs
import codecs
import glob
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_patterns', nargs=argparse.REMAINDER)
    parser.add_argument('-o', '--output', type=str, default='output.html', help='The output file name')
    parsed_args = parser.parse_args()

    deals = []

    for file_pattern in parsed_args.file_patterns:
        files = glob.glob(file_pattern)
        for file in files:
            hand, board = bs.linparse.parse_linfile(file)
            deals.append({'board': board, 'hand': bridge_hand_to_dict(hand)})

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("deals_template.html")

    html_out = template.render({'deals':deals})

    with codecs.open(parsed_args.output, 'w', 'utf8') as f:
        f.write(html_out)

def hand_to_dict(hand):
    ans = {'S': '', 'H': '', 'D': '', 'C': ''}

    for card in reversed(hand.cards):
        suit_name = card.suitname
        if ans[suit_name]:
            ans[suit_name] += " "
        rank_name = "T" if card.rankname == "10" else card.rankname
        ans[suit_name] += rank_name

    for key in ans.keys():
        if not ans[key]:
            ans[key] = '---'

    return ans

VUL_DICT = { 'none': 'None Vul', 'both': 'Both Vul', 'ns': 'N-S Vul', 'we': 'E-W Vul' }

# The diagrams begin with the West column
def format_bidding(dealer, bids):
    # Replace the closing passes with 'ap' (all pass) if possible.
    last_id = len(bids) - 1
    last_pass = last_id
    while last_pass > 0 and bids[last_pass - 1] == 'p':
        last_pass -= 1
    if last_pass < last_id and last_pass >= 0 and bids[last_pass] == 'p':
        bids[last_pass] = 'ap'
        bids = bids[0:(last_pass+1)]

    ans = []
    if dealer == 'N':
        ans += [''] 
    elif dealer == 'E':
        ans += ['', '']
    elif dealer == 'S':
        ans += ['', '', '']

    for bid in bids:
        if bid.lower() == 'p':
            ans.append('Pass')
        elif bid.lower() == 'ap':
            ans.append('All Pass')
        elif bid.lower() == 'd':
            ans.append('Dbl')
        elif bid.lower() == 'r':
            ans.append('RDbl')
        elif len(bid) == 2 and bid.lower()[1] == 'n':
            ans.append(bid[0] + 'NT')
        else:
            ans.append(bid.upper())

    return ans

def next_direction(dir):
    if dir == 'W':
        return 'N'
    elif dir == 'N':
        return 'E'
    elif dir == 'E':
        return 'S'
    elif dir == 'S':
        return 'W'
    assert(False)

def format_play(play):
    ans = []
    for trick in play:
        new_trick = {'lead': trick['lead'], 'cards': []}
        if 'S' not in trick or 'W' not in trick or 'N' not in trick or 'E' not in trick:
            break

        dir = trick['lead']
        for i in range(4):
            card = trick[dir]
            if card.rankname == '10':
                new_trick['cards'].append(f'T{card.suitname}')
            else:
                new_trick['cards'].append(f'{card.rankname}{card.suitname}')

            dir = next_direction(dir)

        ans.append(new_trick)
        
    return ans

def bridge_hand_to_dict(bridge_hand):
    ans = {}

    # Vulnerability
    ans['vul'] = VUL_DICT[bridge_hand.vuln.lower()]
    ans['dealer'] = bridge_hand.dealer

    # Player's hands
    ans['W'] = hand_to_dict(bridge_hand.hands['W'])
    ans['N'] = hand_to_dict(bridge_hand.hands['N'])
    ans['E'] = hand_to_dict(bridge_hand.hands['E'])
    ans['S'] = hand_to_dict(bridge_hand.hands['S'])

    ans['bids'] = format_bidding(bridge_hand.dealer, bridge_hand.bids)

    ans['contract'] = bridge_hand.contract
    ans['doubled'] = bridge_hand.doubled
    ans['delcarer'] = bridge_hand.declarer

    ans['play'] = format_play(bridge_hand.play)
    ans['made'] = bridge_hand.made
    ans['claimed'] = bridge_hand.claimed

    print(ans)

    return ans

if __name__ == "__main__":
    main()