# all_possible_poems
Creates and reads from a database of all possible poems that fit certain criteria.

The criteria:

- Composed of four possible words
- Four lines of poetry
- One to four words per line
- No word repeats more than once on a line, and words may be in any order (permutation)
- No line repeats (each line is unique vs. all other lines in the poem: permutations of lines, not combinations)

This produces 15,249,024 poems.

The Python script `generate_all_poetry.py` creates an sqlite3 database which contains all poems that meet these criteria. See the comments at the start of that script for detailed description and usage. The script `retrieve_and_decipher_poem.py` is some example code for retrieval and display of a poem.

An example poem:

    A B C D
    A B D
    D C B A
    A C D

If we consider this a shorthand or cipher to be expanded or translated into a poem that approximates any kind of sense or meaning, we can do things like this:

    A = woof
    B = woofus
    C = woofy
    D = yorp

With that translation key, the above becomes:

    woof woofus woofy yorp
    woof woofus yorp
    yorp woofy woofus woof
    woof woofy yorp

Now consider a different translation:

    A = byor
    B = byorf
    C = norf
    D = blor

The above becomes:

    byor byorf norf blor
    byor byorf blor
    blor norf byorf byor
    byor norf blor

Follows the original draft of the readme (or design), still applicable if the poems in this collection are translated to Dog.

## woof_woofus

### Poetry by and for dogs

We spoke with all dogs. Dogs have a surprising lot of things to say with their four basic utterances in combination: "woof," "woofus," "woofy," and "yorp." What they have to say is also surprisingly poetic. We collected all of those things. These are those things. All of them. These are all possible dog poems.