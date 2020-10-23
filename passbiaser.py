import argparse
import itertools

# global variables
LEET_MAP = str.maketrans('oOaAiIeE', '00441133')  # does not include sS -> 5
LEETAT_MAP = str.maketrans('oOaAiIeE', '00@@1133')


def init_argparser():
    """Parse args sent by command line.

    Returns
    -------
    args : args.Namespace
        Namespace containing the arguments.
    """

    parser = argparse.ArgumentParser(description="Simple tool for generating"
                                     "password wordlists biased for certain"
                                     "words and dates.")
    parser.add_argument('minLen', type=int,
                        help='minimum length for the passwords')
    parser.add_argument('maxLen', type=int,
                        help='maximum length for the passwords')
    parser.add_argument('-u', '--upper', action='store_true',
                        help='uppercase mutagen')
    parser.add_argument('-l', '--leet', action='store_true',
                        help='l33t mutagen')
    parser.add_argument('--leetat', action='store_true',
                        help='l33t mutagen with aA -> @')
    parser.add_argument('--mix-leet', action='store_true',
                        help='should be used with leet xor leetat.'
                        'Makes, for example, "l3et" possible')
    parser.add_argument('-c', '--capitalize', action='store_true',
                        help='capitalize mutagen')
    parser.add_argument('--compress-md', action='store_true',
                        help='compress months and days starting'
                        'with 0 mutagen, e.g 02 -> 2')
    parser.add_argument('--compress-y', action='store_true',
                        help='compress years from 4 digits'
                        'to 2 mutagen, e.g 1978 -> 78')
    parser.add_argument('-w', '--wordsfile',
                        help='file containing the words to be used.')
    parser.add_argument('-d', '--datesfile',
                        help='file containing the dates to be used,'
                        'each line should be in DD-MM-YYYY\n'
                        'format, e.g: 16-04-1994; xx-04-1995; 16-xx-xxxx; etc')
    parser.add_argument('-o', '--outputfile',
                        help='output file to write wordlist.')

    args = parser.parse_args()
    return args


# auxiliary functions
def _parse_dates(opened_file):
    dates = opened_file.read().splitlines()
    numbers = [i for j in dates for i in j.split('-')]
    # remove the xx and xxxx
    numbers = [x for x in numbers if x.lower() != 'xx' and x.lower() != 'xxxx']

    return numbers


def _combination_len(combination_set):
    return sum([len(x) for x in combination_set])


def _mixed_leets(string, leetmap, k=0, all_mixed_leets=None):
    """Return a list containing all mixed leets possiblities for a string.

    Parameters
    ----------

    string : str, required
        String to be parsed.
    leetmap : dict, requiered
        Dictionary mapping chars to numbers.
    k : int
        Index to save the state of recursive function.
    all_mixed_leets : list
        List to be returned, passed to save the state of recursive function.
    """
    # Case where it has just started. This is needed, if we set
    # all_mixed_leets to [] by default the function will save state
    # when it's not expected to do so.
    if not all_mixed_leets:
        all_mixed_leets = []
    for i in range(k, len(string)):
        char = string[i]
        if char in 'oOaAiIeE':
            new_string_list = [*string]
            new_string_list[i] = char.translate(leetmap)
            new_string = ''.join(new_string_list)
            all_mixed_leets.append(new_string)
            all_mixed_leets = _mixed_leets(new_string,
                                           leetmap,
                                           k=i,
                                           all_mixed_leets=all_mixed_leets)
    return all_mixed_leets


def _add_leets(string_set, leetmap, mix=False):
    """Return initial set united with set of leets.

    Parameters
    ----------

    string_set : set{str}
        Set containing strings to be transformed.
    leetmap : dict
        Dict mapping chars to ints.
    mix : bool
        Either to have mixed leets or not.
    """

    if not mix:
        return string_set | set([s.translate(leetmap) for s in string_set])

    list_string_lists = [_mixed_leets(s, leetmap) for s in string_set]
    return string_set | set([s for mixed in list_string_lists for s in mixed])


def combinations(args, string_set, curr_comb=set(), ret=None):
    """Return all combinations of words on string_set according to
    the passed mutagens.

    Parameters
    ----------

    string_set : set{str} or list[str], required
        Set or list containing the strings to be mutaded and combined
    curr_comb : set
        Combination being parsed, saving state of recursive function
    ret : list
        List to be returned, saving state of recursive function

    Returns
    -------

    ret : list[set]
        List of sets, it set a combination of mutaded words
    """

    minL = args.minLen
    maxL = args.maxLen

    # Case where it has just started. This is needed, if we set
    # ret to [] by default the function will save state
    # when it's not expected to do so.
    if not ret:
        ret = []

    for raw_string in string_set:
        mutations_set = {raw_string}
        # parse dates
        if raw_string.isdigit() and (args.compress_md or args.compress_y):
            # 4 digit string will be interpreted as a year
            if len(raw_string) == 4 and args.compress_y:
                mutations_set.add(raw_string[-2:])
            # 2 digit string starting with 0 will be interpreted as a
            # compressible month or day.
            if len(raw_string) == 2 and raw_string[0] == '0' and args.compress_md:
                mutations_set.add(raw_string[1])
        # add mutagens to mutations_set
        if (not raw_string.isdigit()) and (args.leet or args.leetat or args.upper or args.capitalize):
            if args.upper:
                mutations_set = mutations_set | set([i.upper() for i in mutations_set])
            if args.capitalize:
                mutations_set = mutations_set | set([i.capitalize() for i in mutations_set])
            if args.leet:
                mutations_set = _add_leets(mutations_set, LEET_MAP, args.mix_leet)
            if args.leetat:
                mutations_set = _add_leets(mutations_set, LEETAT_MAP, args.mix_leet)

        # remove parsed strings from string set
        new_string_set = string_set.difference(curr_comb.union({raw_string}))
        for string in mutations_set:
            new_comb = curr_comb.union({string})
            auxL = _combination_len(new_comb)
            if minL <= auxL <= maxL:
                ret.append(new_comb)
                ret = combinations(args,
                                   new_string_set,
                                   new_comb,
                                   ret=ret)
            elif auxL < minL:  # try again if minimum length not achieved.
                ret = combinations(args,
                                   new_string_set,
                                   new_comb,
                                   ret=ret)
    return ret


def arranjos(combinations):
    """Return all permutations, concatenated to string, of combinations.
    Parameters
    ----------

    combinations : list[set]
        List of sets, each set a combination of words.

    Returns
    -------

    arranjos : list[str]
        List of concatenated permutations of words in combinations.
    """

    arranjos = []
    uniq = set(frozenset(i) for i in combinations)
    for c in uniq:
        arranjos.extend([''.join(i) for i in itertools.permutations(c)])
    return arranjos


def main(args):
    """Calculate wordlist and write it to file
    """

    # Script misuse handling.
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

    wordlist = arranjos(combinations(args, fullset))
    if args.outputfile:
        with open(args.outputfile, 'w') as f:
            f.write('\n'.join(wordlist))


if __name__ == '__main__':
    pass
    main(init_argparser())
