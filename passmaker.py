import argparse
import string

LEET_MAP = str.maketrans('oOaAiIeEsS', '0044113355')
LEETat_MAP = str.maketrans('oOaAiIeEsS', '00@@113355')

def init_argparser():
    parser = argparse.ArgumentParser(description="Simple tool for generating password wordlists biased for certain words and dates.")
    parser.add_argument('minLen', type=int, help='minimum length for the passwords')
    parser.add_argument('maxLen', type=int, help='maximum length for the passwords')
    parser.add_argument('-u', '--upper', action='store_true', help='uppercase mutagen')
    parser.add_argument('--l33t', action='store_true', help='leet mutagen')
    parser.add_argument('--l33t@', action='store_true', help='leet mutagen with aA -> @')
    parser.add_argument('-c', '--captalize', action='store_true', help='capitalize mutagen')
    parser.add_argument('--wordsfile', help='file containing the words to be used. A ! on the beggining of the word'
            'will make it mandatory, to avoid this, escape the exclamation sign.')
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

def combination(args, to_combine, curr_combination, all_combinations=set()):
    if not to_combine:
        return all_combinations()
    if L := _combination_len(curr_combination) > args.maxLen or L < args.minLen:
        return all_combinations()
    new_combination = curr_combination.add(to_combine)
    all_combination.add(new_comb)
    new_to_combine
    make_all_combinations(args, 


    

def combine (args, to_combine_set, combined_set=set()):
    
    



    


    
    

def main(args):
    if args.wordsfile:
        with open(args.wordsfile, 'r') as f:
            words = parse_words(f)
            assert len(max(words, key=len)) <= args.maxLen, "Wordsfile incompatible with maxLen."
    if args.datesfile:
        with open(args.datesfile, 'r') as f:
            dates = parse_dates(f)
            assert len(max(dates, key=len)) <= args.maxLen, "Datesfile incompatible with maxLen."
    wordlist = []
    for N in range(args.minLen, args.maxLen + 1):



if __name__ == '__main__':
    #main(init_argparser())
