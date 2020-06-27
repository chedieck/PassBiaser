import argparse
import string
import itertools

LEET_MAP = str.maketrans('oOaAiIeE', '00441133') # does not include sS -> 5
LEETat_MAP = str.maketrans('oOaAiIeE', '00@@1133')

def init_argparser():
    parser = argparse.ArgumentParser(description="Simple tool for generating password wordlists biased for certain words and dates.")
    parser.add_argument('minLen', type=int, help='minimum length for the passwords')
    parser.add_argument('maxLen', type=int, help='maximum length for the passwords')
    parser.add_argument('-u', '--upper', action='store_true', help='uppercase mutagen')
    parser.add_argument('--leet', action='store_true', help='l33t mutagen')
    parser.add_argument('--leetat', action='store_true', help='l33t mutagen with aA -> @')
    parser.add_argument('-c', '--captalize', action='store_true', help='capitalize mutagen')
    parser.add_argument('-w', '--wordsfile', help='file containing the words to be used.') 
    parser.add_argument('-d', '--datesfile', help='file containing the dates to be used, each line should be in DD-MM-YYYY\n'
            'format, e.g: 16-04-1994; xx-04-1995; 16-xx-xxxx; etc')
    parser.add_argument('-o', '--outputfile', help='output file to write wordlist.')

    args = parser.parse_args()
    return args

#words = ['zezin', 'totó']
#dates = ['26-10-1995', '31-09-1800']



def gen_for_N(N, args, words, dates):
    mandatorywords = [w for w in words if w[0] == '!']
    words = [w if w[0] != '\\' else w for w in words]
    pass

def parse_words (args, opened_file):
    words = opened_file.read().splitlines()
    input_list = words.copy()
    for word in words :
        if args.captalize:
            input_list.append(word.capitalize())
    words = input_list.copy()
    for word in words :
        if args.upper:
            input_list.append(word.upper())
    words = input_list.copy()
    for word in words :
        if args.leet:
            input_list.append(w := word.translate(LEET_MAP))
    words = input_list.copy()
    for word in words :
        if args.leetat:
            input_list.append(word.translate(LEETat_MAP))

    return input_list

def parse_dates (opened_file):
    dates = opened_file.read().splitlines()
    numbers = [i for j in dates for i in j.split('-')]
    # remove the xx and xxxx
    numbers = [x for x in numbers if x.lower() != 'xx' and x.lower() != 'xxxx']

    return numbers

# short auxiliary function
def _combination_len(combination_set):
    return sum([len(x) for x  in combination_set])


#hard way, fuckit
def combinations(S, minL, maxL, curr_comb=set(), ret=[]):
    for s in S: 
        #####this#section#parses#dates####
        special = '' # string to specify if current s is day or year
        N = 1 #auxiliar counter
        if s.isdigit():     # digits will be treated in a special way
            if len(s) == 4: # 4-sized digit string will be interpreted as a year
                special = 'y' 
            if len(s) == 2 and s[0] == '0':
                # 2-sized digit string starting with 0 will be interpreted as a month or day
                special = 'd' 
            N = 2
        for i in range(N):
            real_s = s  
            if i == 1:     # second case where s is a year, month or day
                if special == 'y':
                    s = s[-2:] # get only last two digits to represent year.
                if special == 'd':
                    s = s[1] # get s without the initial zero
            ##################################

            new_comb = curr_comb.union({s})
            newS = S.difference(curr_comb.union({real_s}))

            auxL =_combination_len(curr_comb) + len(s) 
            if minL <= auxL <= maxL:
                ret.append(new_comb)
                ret = combinations(newS, minL, maxL, new_comb, ret=ret)
            elif auxL < minL:
                ret = combinations(newS, minL, maxL, new_comb, ret=ret)
    return ret


def arranjos(combinations):
    arranjos = []
    uniq = set(frozenset(i) for i in combinations)
    for c in uniq:
        arranjos.extend([''.join(i) for i in itertools.permutations(c)])
    return arranjos


def main(args):
    if args.wordsfile:
        with open(args.wordsfile, 'r') as f:
            words = parse_words(args, f)
            assert len(max(words, key=len)) <= args.maxLen, "Wordsfile incompatible with maxLen."
    if args.datesfile:
        with open(args.datesfile, 'r') as f:
            dates = parse_dates(f)
            assert len(max(dates, key=len)) <= args.maxLen, "Datesfile incompatible with maxLen."
    fullset = set(words + dates)
    fullset.remove('')

    if args.outputfile:
        with open(args.outputfile, 'w') as f:
            f.write('\n'.join(A))

if __name__ == '__main__':
    pass
    main(init_argparser())
