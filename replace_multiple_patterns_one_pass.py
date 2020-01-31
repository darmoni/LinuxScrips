#!/usr/bin/env python3

try: dict
except: from UserDict import UserDict as dict

import re, sys

'''
# the simplest, lambda-based implementation
def multiple_replace(adict, text):
  # Create a regular expression from all of the dictionary keys
  regex = re.compile("|".join(map(re.escape, adict.keys(  ))))

  # For each match, look up the corresponding value in the dictionary
  return regex.sub(lambda match: adict[match.group(0)], text)
'''

def get_words_from_file(file):
    words = []
    for line in file.readline():
        if '#' == line[0]:
            continue
        words += ( line.split())
    return words

class Xlator(dict):
    """ All-in-one multiple-string-substitution class """
    def _make_regex(self):
        """ Build re object based on the keys of the current dictionary """
        return re.compile("|".join(map(re.escape, self.keys(  ))))

    def __call__(self, match):
        """ Handler invoked for each regex match """
        return self[match.group(0)]

    def xlat(self, text):
        """ Translate text, returns the modified text. """
        return self._make_regex(  ).sub(self, text)

class WordXlator(Xlator):
    """ An Xlator version to substitute only entire words """
    def _make_regex(self):
        return re.compile(
          r'\b'+r'\b|\b'.join(map(re.escape, self.keys(  )))+r'\b')

#sql_reserved_words = 'select while and update insert limit by from left join when where'.split()
if __name__ == "__main__":
    keywords = []

    sql_reserved_words_file = open('mysql_key_words.doc')
    keywords += get_words_from_file(sql_reserved_words_file)

    sql_reserved_words = " ".join(keywords).replace('ACCOUNT','').lower()

    #print(sql_reserved_words.upper())
    index = 0
    if len(sys.argv) > 1:
        index = 1
    #print (sys.argv[index])
    file_name = sys.argv[index];
    file = open(file_name)
    text = file.read().strip()
    adict = {
        "while" : "WHILE",
        #text = "`Larry'.'Wall` is the `creator` of `Perl`"
        #adict = {
        "Larry Wall" : "Guido van Rossum",
        "Wall" : "van Rossum",
        "Larry" : "Guido",
        "creator" : "Benevolent Dictator for Life",
        "Perl" : "Python",
        }
    #print(sql_reserved_words)
    for w in sql_reserved_words.split():
        adict.update({w.lower() : w.upper()})
    #print(adict)
    xlat = WordXlator(adict)
    print (xlat.xlat(text))
