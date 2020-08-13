# DESCRIPTION
# Creates all possible poetry of certain combinatronic parameters (15,249,024 poems), using the letters A, B, C, and D. The results may be translated to any of infinite possible poems by designating four different possible words to substitute for those letters. An example (and the first thought of) translation; "dog poetry:"
#    A = woof
#    B = woofus
#    C = woofy
#    D = yorp
# Pick any such poem from the database which this script creates, and translate and read them to your dogs. See how they like them. It is likely that results are better with humans. This was not actually tested on dogs before release. It's a leap of faith.

# DEPENDENCIES
# Python 3. Know-how for installing Python and/or invoking scripts with it.

# USAGE
# With Python installed and in your PATH, open a terminal to the directory with this script, and invoke it as a parameter to Python:
#    python generate_all_poetry.py
# It will print progress about poems it generates, and when complete (which could be a very long time), the results will be in the mysqlite3 database all_poetry.sqlite. See retrieve_and_decipher_poem.py for a retrieval example, but any code that interfaces with a mysqlite3 database (including terminal queries) will work.


# CODE
import os
db_file_exists_boolean = os.path.exists('all_poetry.sqlite')
if db_file_exists_boolean == False:
	import itertools
	import random
	import sqlite3

	# ORIGINAL DOG POETRY ORDER REFERENCE; DEPRECATED after I realized I can create more than just dog poems by translating letters:
	# one_word_permutations = ['woof', 'woofus', 'woofy', 'yorp']
	# create permutations of all these: 1, 2, 3 and 4-word groups:
	one_word_permutations = ['A', 'B', 'C', 'D']
	two_word_permutations = list(itertools.permutations(one_word_permutations, 2))
		# variant that includes repetition, but hangs the computer:
		# two_word_permutations = list(itertools.product(one_word_permutations, repeat=2))
	three_word_permutations = list(itertools.permutations(one_word_permutations, 3))
	four_word_permutations = list(itertools.permutations(one_word_permutations, 4))

	# create a list for all these permutations, and add all of them to it, in human-readable string format:
	all_one_to_four_permutations = list()

	for element in one_word_permutations:
		all_one_to_four_permutations.append(element)

	for element in two_word_permutations:
		tmp_str = element[0] + ' ' + element[1]
		all_one_to_four_permutations.append(tmp_str)

	for element in three_word_permutations:
		tmp_str = element[0] + ' ' + element[1] + ' ' + element[2]
		all_one_to_four_permutations.append(tmp_str)

	for element in four_word_permutations:
		tmp_str = element[0] + ' ' + element[1] + ' ' + element[2] + ' ' + element[3]
		all_one_to_four_permutations.append(tmp_str)

	# Create a list of all 4-permutations of all those. This is our collection of poetry. If this were combinations and not permutations, it would be impractically huge. I tried it. The task seemed to hang. Even what permutaitons narrows it down to is arguably impractical, but at least it's barely wieldy.
	all_poetry = list(itertools.permutations(all_one_to_four_permutations, 4))

	# Define a function that creates a poetry formatted string from any poem index in the collection. '/' is stanza or meter or newline separation in this.
	def format_poem_by_index(idx):
		poem = ''
		for line in all_poetry[idx]:
			poem += line + "/"
		return poem

	# Creates the database file and table if they don't already exist (which, re a previous check, they should not) :
	conn = sqlite3.connect('all_poetry.sqlite')
	cursor = conn.cursor()
	# NOTES to help me keep it straight:
	# - The database fields are poemID, poemText.
	# - The corresponding Python variables are hooman_counting_number, STRpoem.
	cursor.execute('''CREATE TABLE poems(poemID INTEGER, poemText TEXT)''')
	# Populate it with poems with IDs of incrementing numbers:
	idx = 0
	for data in all_poetry:
		STRpoem = format_poem_by_index(idx)
		# because I'm not going to have human-counterintuitive zero-based poem IDs:
		hooman_counting_number = idx + 1; idx += 1
		print('Format and insert poem ID', hooman_counting_number, ' . . .')
		# re: https://pythonprogramming.net/sqlite-part-2-dynamically-inserting-database-timestamps :
		cursor.execute("INSERT INTO poems (poemID, poemText) VALUES (?, ?)", (hooman_counting_number, STRpoem))
	conn.commit()
	conn.close()

	print("DONE. All possible poemes (in the constraints of this script) have been created: ", str(len(all_poetry)), ' poems.')
	print("To extract and translate poems by ID (which is any number from 1 to that maximum range), use retrieve_and_print_poem.py.")
else:
	print('Database file all_poetry.sqlite already exists; will not use.\nTo recreate it, delete it and run this script again.')