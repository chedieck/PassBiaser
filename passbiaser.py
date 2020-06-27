import argparse
import string
import itertools

LEET_MAP = str.maketrans('oOaAiIeEsS', '0044113355')
LEETat_MAP = str.maketrans('oOaAiIeEsS', '00@@113355')

def init_argparser():
    parser = argparse.ArgumentParser(description="Simple tool for generating password wordlists biased for certain words and dates.")
    parser.add_argument('minLen', type=int, help='minimum length for the passwords')
    parser.add_argument('maxLen', type=int, help='maximum length for the passwords')
    parser.add_argument('-u', '--upper', action='store_true', help='uppercase mutagen')
    parser.add_argument('--leet', action='store_true', help='l33t mutagen')
    parser.add_argument('--leetat', action='store_true', help='l33t mutagen with aA -> @')
    parser.add_argument('-c', '--captalize', action='store_true', help='capitalize mutagen')
    parser.add_argument('--wordsfile', help='file containing the words to be used.') 
    parser.add_argument('--datesfile', help='file containing the dates to be used, each line should be in DD-MM-YYYY\n'
            'format, e.g: 16-04-1994; xx-04-1995; 16-xx-xxxx; etc')

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
    input_list = set(words)
    for word in words :
        if args.c:
            input_list.add(word.capitalize())
        if args.u:
            input_list.add(word.upper())

def parse_dates (opened_file):
    dates = opened_file.read().splitlines()
    days, months, years = dates.split()
    # remove the xx and sort
    days = [x for x in days if x.lower() != 'xx'].sort(key=len, reverse=1)
    months = [x for x in months if x.lower() != 'xx'].sort(key=len, reverse=1)
    years = [x for x in years if x.lower() != 'xx'].sort(key=len, reverse=1)


    dates = {'years': years, 'months': months, 'days': days}
    return dates

def _combination_len(combination_set):
    return sum([len(x) for x  in combination_set])


""" hard way, fuckit
def combinations(S, minL, maxL, curr_comb=set(), ret=[]):
    print(locals(), input())
    for s in S: 
        #####this#section#parses#dates####
        special = ''
        N = 1
        if s.isdigit():     # digits will be treated in a special way
            if len(s) == 4: # 4-sized digit string will be interpreted as a year
                special = 'y' 
            if len(s) == 2 and s[0] == '0':
                # 2-sized digit string starting with 0 will be interpreted as a month or day
                special = 'd' 
            N = 2
        for i in range(N):
            if i == 1:     # case where s is a year, month or day
                if special == 'y':
                    s = s[-2:] # get only last two digits to represent year.
                if special == 'd':
                    s = s[1] # get s without the initial zero
            ##################################

            new_comb = curr_comb.union({s})
            newS = S.difference(new_comb)
            auxL = _combination_len(curr_comb) + len(s)
            if minL <= auxL <= maxL:
                ret.append(new_comb)
            elif auxL < minL:
                ret = combinations(newS, minL, maxL, new_comb, ret=ret)
    return ret

"""

def arranjos(S, minL, maxL):
    auxcombinations = []
    for i in range(len(S)):
        auxcombinations.extend([c for c in itertools.combinations(S, i)])
    combinations = [c for c in auxcombinations if minL <= _combination_len(c) <= maxL]
    arranjos = []
    for c in combinations:
        arranjos.extend([''.join(i) for i in itertools.permutations(c)])
    return arranjos
    

    
    



    


    
    

def main(args):
    if args.wordsfile:
        with open(args.wordsfile, 'r') as f:
            words = parse_words(f)
            assert len(max(words, key=len)) <= args.maxLen, "Wordsfile incompatible with maxLen."
    if args.datesfile:
        with open(args.datesfile, 'r') as f:
            dates = parse_dates(f)
            assert len(max(dates, key=len)) <= args.maxLen, "Datesfile incompatible with maxLen."
    if args.capitalize:
        words = [i.capitalize() for i in words]

    if args.upper:
        words = [i.upper() for i in words]

    if args.leet:
        words = [i.translate(LEET_MAP) for i in words]

    if args.leetat:
        words = [i.translate(LEETAT_MAP) for i in words]

    # run the 


        


if __name__ == '__main__':
    pass
    #main(init_argparser())
