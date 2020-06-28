# PassMaker

Wordlist creator with bias for words and dates.
-
```
usage: passbiaser.py [-h] [-u] [--leet] [--leetat] [-c] [--compress-md] [--compress-y] [-w WORDSFILE] [-d DATESFILE] [-o OUTPUTFILE] minLen maxLen

Simple tool for generating password wordlists biased for certain words and dates.

positional arguments:
  minLen                minimum length for the passwords
  maxLen                maximum length for the passwords

optional arguments:
  -h, --help            show this help message and exit
  -u, --upper           uppercase mutagen
  --leet                l33t mutagen
  --leetat              l33t mutagen with aA -> @
  -c, --capitalize      capitalize mutagen
  --compress-md         compress months and days starting with 0 mutagen, e.g 02 -> 2
  --compress-y          compress years from 4 digits to 2 mutagen, e.g 1978 -> 78
  -w WORDSFILE, --wordsfile WORDSFILE
                        file containing the words to be used.
  -d DATESFILE, --datesfile DATESFILE
                        file containing the dates to be used, each line should be in DD-MM-YYYY format, e.g: 16-04-1994; xx-04-1995; 16-xx-xxxx; etc
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        output file to write wordlist.
```

Repository with example files `words.test` and `dates.test` for usage example: `python passbiaser.py 8 12 -w words.test -d dates.test -c -o temp.txt`

The script doesn't use the same string with and without mutagen in the same password. So, for example, if you have the words `zé` and `maria` with the `-c` mutagen, you may get `Zémaria, zémaria, zéMaria...` but  not `zéZé, mariaMaria`.


This project is for educational purpuses only. Use at your own discretion and do not attempt to access anything for which you don't have proper authorization. The contributors should not be held responsible for any illegal activities performed with this software.
