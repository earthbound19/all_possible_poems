# DESCRIPTION
# 994732 woof woofus/woofy yorp/woofus/woof yorp
# Connects to poetry cipher database all_poetry.sqlite and deciphers and prints poem sys.argv[1] (a poem ID number) using the ciphertext loaded from file name sys.argv[2] (for example ciphers/woof_woofus.txt). If no parameters to script are provided, defaults are used.

# USAGE
# Run this script through a Python interpreter with these parameters:
# - sys.argv[1] OPTIONAL. A poem ID (valid values are 1 - 15249024) to load from the database and print. If not provided, or provided as the keyword 'RANDOM' (with or without quotes), a random poem is selected.
# - sys.argv[2] OPTIONAL. File name of a cipher to use to interpret a poem. If not provided, the default hard-coded cipher woof_woofus (the same as what is provided in /ciphers/woof_woofus.txt) is used.
# For example, to load and decipher a random poem from the database with the default cypher woof_woofus, run this script through a Python interpreter without any parameters:
#    python retrieve_and_decipher_poem.py
# To load a specific poem ID, also pass a poem ID to the script; for example:
#    python retrieve_and_decipher_poem.py 994732
# To load a specific poem ID and use a non-default cipher, also pass the file name of a cipher; for example:
#    python retrieve_and_decipher_poem.py 15249024 ciphers/byor_byorf.txt
# To load a random poem ID and use a non-default cipher, run:
#    python retrieve_and_decipher_poem.py RANDOM ciphers/byor_byorf.txt
# Printouts of deciphered poems are preceded by the poemID (number) and a tilde.

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
import sqlite3, sys, re, random

if len(sys.argv) > 1 and sys.argv[1] != 'RANDOM':       # positional parameter 1; poem ID to retrieve (number)
	poemIDtoRetrieve = sys.argv[1]
# - if no sys.argv[1], OR if sys.argv[1] is out of range of available poemIDs, set it to a random number in range:
else:
	poemIDtoRetrieve = random.randint(1, 15249024)
# - dynamic cipher load from text file if sys.argv[2] provided; otherwise use a hard-coded default cipher:
if len(sys.argv) > 2:       # positional parameter 2; the file name of a text file cipher.
	cipherToLoad = sys.argv[2]
	f = open(cipherToLoad, "r")
	cipherRaw = list(f.read().splitlines())
	f.close()
	cipher = [('A',cipherRaw[0]), ('B',cipherRaw[1]), ('C',cipherRaw[2]), ('D',cipherRaw[3])]
else:
	cipher = [('A','woof'), ('B','woofus'), ('C','woofy'), ('D','yorp')]
	# print(cipher[0][0], cipher[0][1])		#A woof
	# print(cipher[1][0], cipher[1][1])		#B woofus

# connect to the database and create a cursor to use it:
conn = sqlite3.connect('all_poetry.sqlite')
cursor = conn.cursor()

# Translates (actually decrypts or deciphers) a poem from cipher letters to words:
def decipher(ciphertext, cipher):
	deciphered_text = re.sub(cipher[0][0], cipher[0][1], ciphertext)
	deciphered_text = re.sub(cipher[1][0], cipher[1][1], deciphered_text)
	deciphered_text = re.sub(cipher[2][0], cipher[2][1], deciphered_text)
	deciphered_text = re.sub(cipher[3][0], cipher[3][1], deciphered_text)
	return deciphered_text 

# retrieve and print poemText by ID from the database:
query = "SELECT poemText FROM poems WHERE poemID = " + str(poemIDtoRetrieve)
cursor.execute(query)
result = cursor.fetchall()
ciphertext = result[0][0]
poem = decipher(ciphertext, cipher)
# Substitute forward slashes in poem with newlines for display:
poem = re.sub('/', '\n', poem)
poemPrintSTR = str(poemIDtoRetrieve) + " ~\n" + poem
print(poemPrintSTR)


