# PassMaker

Wordlist creator with bias for words and dates.
-
Usage:

```
Simple tool for generating password wordlists biased for certain words and dates.

positional arguments:
  minLen                minimum length for the passwords
  maxLen                maximum length for the passwords

optional arguments:
  -h, --help            show this help message and exit
  -u, --upper           uppercase mutagen
  --leet                l33t mutagen
  --leetat              l33t mutagen with aA -> @
  -c, --captalize       capitalize mutagen
  -w WORDSFILE, --wordsfile WORDSFILE
                        file containing the words to be used.
  -d DATESFILE, --datesfile DATESFILE
                        file containing the dates to be used, each line should be in DD-MM-YYYY format, e.g: 16-04-1994; xx-04-1995; 16-xx-xxxx; etc
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        output file to write wordlist.
```

Repository with example files `words.test` and `dates.test` for usage example: `python passbiaser.py 8 12 -w words.test -d dates.test -c -o temp.txt`

The script doesn't use the same string with and without mutagen in the same password. So, if you have the words `zé` and `maria` with the `-c` mutagen, you may get `Zémaria, zémaria, zéMaria...` but  not `zéZé, mariaMaria`.


This project is for educational purpuses only. Use at your own discretion, the contributors should not be hold responsible for any illegal activities performed with this software.
