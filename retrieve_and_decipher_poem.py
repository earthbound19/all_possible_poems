# DESCRIPTION
# 994732 woof woofus/woofy yorp/woofus/woof yorp
# Connects to poetry cipher database all_poetry.sqlite and deciphers and prints poem sys.argv[1] (a poem ID number) using the ciphertext loaded from file name sys.argv[2] (for example ciphers/woof_woofus.txt). If no parameters to script are provided, defaults are used.

# USAGE
# Run this script through a Python interpreter with any of the optional parameters given by --help (all parameters are optional. If you pass no parameters, defaults are used). To see help, run this script this way:
#    python retrieve_and_decipher_poem.py --help

# USAGE EXAMPLES
# To load and decipher a random poemID from the database with the default cypher woof_woofus, run this script through a Python interpreter without any parameters:
#    python retrieve_and_decipher_poem.py
# To load a specific poem ID, pass a poem ID (valid values are 1 - 15249024) with the -i or --poem-id switch; for example:
#    python retrieve_and_decipher_poem.py -i 994732
# To load a specific poem ID and use a non-default cipher, also pass the file name of a cipher with the -c or --cipher switch; for example:
#    python retrieve_and_decipher_poem.py -i 15249024 -c ciphers/meow_mrow.txt
# To load a random poem ID and use a non-default cipher, just pass the cipher via -c (and use the default random poemID select, which you don't have to indicate)
#    python retrieve_and_decipher_poem.py -c ciphers/byor_byorf.txt
# To suppress print of the poemID with poem print (for example to capture the print and pass it to something else), use the -s or --suppress-poem-id-print switch:
#    python retrieve_and_decipher_poem.py -s


# DATABASE SCHEMA AND POETRY DESIGN
# The database has one table, named poems, with two fields: poemID and poemText. poemID is a number, which starts at 1. poemText is the actual text of poems. Meter or stanza separations (or newlines, or however you want to interpret them) are marked by forward slashes /.

# NOTES
# Some good poems:
# - 994732 (featured above)
# - 3124127
# - 999000
# - 13664121
# - 15249024
# - 7966749


# CODE
import sqlite3, sys, re, random, argparse

PARSER = argparse.ArgumentParser(description=
'Connects to poetry cipher database all_poetry.sqlite and deciphers \
and prints a poem.')

PARSER.add_argument('-i', '--poem-id', type=str, help=
'A poem ID (valid values are 1 - 15249024) to load from the database \
and print. If not provided, or provided as the keyword RANDOM, a \
random poem is selected.'
)

PARSER.add_argument('-c', '--cipher', type=str, help=
'File name of a cipher to use to interpret a poem. File format of \
cipher is four words or phrases on four lines (see example in \
ciphers/woof_woofus.txt). If not provided, the default hard-coded \
cipher woof_woofus (the same as what is provided in \
/ciphers/woof_woofus.txt) is used.'
)

PARSER.add_argument('-s', '--suppress-poem-id-print',
action='store_true',
help='Suppresses poemID print with print of poem.'
)

ARGS = PARSER.parse_args()

# SET GLOBALS based on parameters passed or not passed to script
# PoemID; set to what is passed to script if passed; otherwise pick a random one in range of poemIDs:
if ARGS.poem_id:
	poemIDtoRetrieve = ARGS.poem_id
else:
	poemIDtoRetrieve = random.randint(1, 15249024)
# cipher; dynamic cipher load from text file if provided by -c; otherwise use a hard-coded default cipher:
if ARGS.cipher:
	f = open(ARGS.cipher, "r")
	cipherRaw = list(f.read().splitlines())
	f.close()
	cipher_key = [('A',cipherRaw[0]), ('B',cipherRaw[1]), ('C',cipherRaw[2]), ('D',cipherRaw[3])]
else:
	cipher_key = [('A','woof'), ('B','woofus'), ('C','woofy'), ('D','yorp')]
	# print(cipher_key[0][0], cipher_key[0][1])		#A woof
	# print(cipher_key[1][0], cipher_key[1][1])		#B woofus

# optional flag to suppress poemID in print:
if ARGS.suppress_poem_id_print:
	suppressPoemIDinPrint = True
else:
	suppressPoemIDinPrint = False

# connect to the database and create a cursor to use it:
conn = sqlite3.connect('all_poetry.sqlite')
cursor = conn.cursor()

# Translates (actually decrypts or deciphers) a poem from cipher_key letters to words:
def decipher(ciphertext, cipher_key):
	deciphered_text = re.sub(cipher_key[0][0], cipher_key[0][1], ciphertext)
	deciphered_text = re.sub(cipher_key[1][0], cipher_key[1][1], deciphered_text)
	deciphered_text = re.sub(cipher_key[2][0], cipher_key[2][1], deciphered_text)
	deciphered_text = re.sub(cipher_key[3][0], cipher_key[3][1], deciphered_text)
	return deciphered_text 

# retrieve and print poemText by ID from the database:
query = "SELECT poemText FROM poems WHERE poemID = " + str(poemIDtoRetrieve)
cursor.execute(query)
result = cursor.fetchall()
ciphertext = result[0][0]
poem = decipher(ciphertext, cipher_key)
# Substitute forward slashes in poem with newlines for display:
poem = re.sub('/', '\n', poem)
# Suppress or do not suppress print of poemID with poem print, depending on set flag:
if suppressPoemIDinPrint == True:
	print(poem)
else:
	print(str(poemIDtoRetrieve) + " ~\n" + poem)