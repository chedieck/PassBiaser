import argparse
import string
import itertools

LEET_MAP = str.maketrans('oOaAiIeE', '00441133') # does not include sS -> 5
LEETAT_MAP = str.maketrans('oOaAiIeE', '00@@1133')

def init_argparser():
    parser = argparse.ArgumentParser(description="Simple tool for generating password wordlists biased for certain words and dates.")
    parser.add_argument('minLen', type=int, help='minimum length for the passwords')
    parser.add_argument('maxLen', type=int, help='maximum length for the passwords')
    parser.add_argument('-u', '--upper', action='store_true', help='uppercase mutagen')
    parser.add_argument('-l', '--leet', action='store_true', help='l33t mutagen')
    parser.add_argument('--leetat', action='store_true', help='l33t mutagen with aA -> @')
    parser.add_argument('--mix-leet', action='store_true', help="should be used with leet xor leetat. Makes, for example, 'l3et' possible")
    parser.add_argument('-c', '--capitalize', action='store_true', help='capitalize mutagen')
    parser.add_argument('--compress-md', action='store_true', help='compress months and days starting with 0 mutagen, e.g 02 -> 2')
    parser.add_argument('--compress-y', action='store_true', help='compress years from 4 digits to 2 mutagen, e.g 1978 -> 78')
    parser.add_argument('-w', '--wordsfile', help='file containing the words to be used.') 
    parser.add_argument('-d', '--datesfile', help='file containing the dates to be used, each line should be in DD-MM-YYYY\n'
            'format, e.g: 16-04-1994; xx-04-1995; 16-xx-xxxx; etc')
    parser.add_argument('-o', '--outputfile', help='output file to write wordlist.')

    args = parser.parse_args()
    return args


# auxiliary functions
def _parse_dates (opened_file):
    dates = opened_file.read().splitlines()
    numbers = [i for j in dates for i in j.split('-')]
    # remove the xx and xxxx
    numbers = [x for x in numbers if x.lower() != 'xx' and x.lower() != 'xxxx']

    return numbers

def _combination_len(combination_set):
    return sum([len(x) for x  in combination_set])

def _mixed_leets(string, leetmap, k=0, all_mixed_leets=None):
    # Cant set default param value of all_mixed_leets to [],
    # Or function will save the variable state and accumulate
    # the return value.
    if not all_mixed_leets:
        all_mixed_leets = []
    for i in range(k, len(string)):
        char = string[i]
        if char in 'oOaAiIeE':
            new_string_list = [*string]
            new_string_list[i] = char.translate(leetmap)
            new_string = ''.join(new_string_list)
            all_mixed_leets.append(new_string)
            all_mixed_leets = _mixed_leets(new_string, leetmap, k=i, all_mixed_leets = all_mixed_leets)
    return all_mixed_leets

def _add_leets(S, leetmap, mix=False):
    if not mix:
        return S | set([s.translate(leetmap) for s in S])

    list_string_lists = []
    for s in S:
        list_string_lists.append(_mixed_leets(s, leetmap))

    return  S | set([s for mixed in list_string_lists for s in mixed])

#####



def combinations(args, S, curr_comb=set(), ret=[]):
    """This is a very verbose funcion. The first part parses the mutagens,
    while only the second actually calculates the combinations. 
    """
    minL = args.minLen
    maxL = args.maxLen
    for raw_s in S: 
        #####this section parses dates####
        s_mutations = {raw_s}
        if raw_s.isdigit() and (args.compress_md or args.compress_y):
            if len(raw_s) == 4 and args.compress_y: # 4-sized digit string will be interpreted as a year
                s_mutations.add(raw_s[-2:])
            if len(raw_s) == 2 and raw_s[0] == '0' and args.compress_md:
                # 2-sized digit string starting with 0 will be interpreted as a month or day
                s_mutations.add(raw_s[1])
        if (not raw_s.isdigit()) and (args.leet or args.leetat or args.upper or args.capitalize):
            if args.upper:
                s_mutations = s_mutations | set([i.upper() for i in s_mutations])
            if args.capitalize:
                s_mutations = s_mutations | set([i.capitalize() for i in s_mutations])
            if args.leet:
                s_mutations = _add_leets(s_mutations, LEET_MAP, args.mix_leet)
            if args.leetat:
                s_mutations = _add_leets(s_mutations, LEETAT_MAP, args.mix_leet)
        ######
        for s in s_mutations:
            new_comb = curr_comb.union({s})
            newS = S.difference(curr_comb.union({raw_s}))

            auxL = _combination_len(new_comb)
            if minL <= auxL <= maxL:
                ret.append(new_comb)
                ret = combinations(args, newS, new_comb, ret=ret)
            elif auxL < minL:
                ret = combinations(args, newS, new_comb, ret=ret)
    return ret


def arranjos(combinations):
    arranjos = []
    uniq = set(frozenset(i) for i in combinations)
    for c in uniq:
        arranjos.extend([''.join(i) for i in itertools.permutations(c)])
    return arranjos


def main(args):
    #first part deals with misuse of the software
    assert not (args.leet and args.leetat), "--leet and --leetat should not be used together."
    fullset = []
    if args.wordsfile:
        with open(args.wordsfile, 'r') as f:
            words = f.read().splitlines()
            fullset += words
            assert len(max(words, key=len)) <= args.maxLen, "Wordsfile incompatible with maxLen."
    if args.datesfile:
        with open(args.datesfile, 'r') as f:
            dates = _parse_dates(f)
            fullset += dates
            assert len(max(dates, key=len)) <= args.maxLen, "Datesfile incompatible with maxLen."
    fullset = set(fullset)
    try:
        fullset.remove('')
    except KeyError:
        pass

    A = arranjos(combinations(args, fullset))
    if args.outputfile:
        with open(args.outputfile, 'w') as f:
            f.write('\n'.join(A))

if __name__ == '__main__':
    pass
    main(init_argparser())
