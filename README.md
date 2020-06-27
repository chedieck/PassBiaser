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


This project is for educational purpuses only. Use at your own discretion, the contributors should not be hold responsible for any illegal activities performed with this software.
