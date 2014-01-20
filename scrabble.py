#!/usr/bin/python
# See usage().  Aaron Fabbri 2011

import os
import sys
import sets

def usage() :
	print "Usage:  give it a string, and it will find all words that can"
	print "\tbe made from permutations of those characters."
	print ""
	print "%s <string>" % sys.argv[0]
	sys.exit()

class StringPermuter :
	min_str_len = 3
	max_str_len = 0
	# On ubuntu, I `apt-get install wamerican` to get this file
	dictionary_file = "/usr/share/dict/words"
	word_list = []

	def __init__(s, chars) : 
		s.chars = chars
		f = file(s.dictionary_file)
		print "Reading dictionary into memory"
		s.word_list = f.readlines()
		s.word_list = map(lambda s: s.strip().lower(), s.word_list)
		print "..done (%d words in dictionary)" % (len(s.word_list))
		s.word_set = sets.Set(s.word_list) 

	def is_word_in_dict(s, word) :
		word = word.lower()
		return ( word in s.word_set )

	# For each character c in 'chars', append "c" + prefix to 'output' set.
	# Also, recursively do stuff to visit all permutations of 'chars'
	def append_w_prefix(s, prefix, chars, output) :
		for c in chars : 
			word = prefix + c
			if len(word) >= s.min_str_len :
				output.add(word)
			remaining_chars = chars.replace(c, "", 1)
			s.append_w_prefix(word, remaining_chars, output)

	def output_words(s) :
		perms = set()
		print "Finding permutations..."
		s.append_w_prefix("", s.chars, perms)
		print "Testing words..."
		for w in perms :
			if s.is_word_in_dict(w) :
				print w
		print "Done."
	
def main():
	global max_str_len
	if len(sys.argv) != 2:
		usage()
	chars = sys.argv[1]	
	p = StringPermuter(chars)
	p.output_words()

if __name__ == "__main__":
	main()



