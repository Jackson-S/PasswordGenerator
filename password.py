from random import randint, choice
from sys import argv
from os import system

""" python3 password.py [dictionary]

    Creates a password of specified length as described in xkcd.com/936/, eg.
    ManipularUseeBrockEruca, using OSX's builtin dictionary (should work on linux too
    pointing to a correct dictionary)
"""

dictionary = open(argv[1], "r") if len(argv) > 1 else open("/usr/share/dict/web2", "r").read().split("\n")
password, length, maxchars = "", 0, 0
additions = [chr(x) for x in range(33, 65)]
errors = ("No", "Bad", "Incorrect", "Rude", "Wrong", "Silly", "Spurious", ":/")

while (True):
    try:
        length = int(input("How many words? "))
        extras = int(input("How many extra characters would you like to add? "))
        maxchars = int(input("Maximum password length? (minumum {}) ".format(length * 4 + extras)))
        if length < 1 or maxchars < 1 or (maxchars < length * 4):
            print("Length must be 4 * words + 1 i.e. 4 words, 17 characters")
            continue
        break
    except (ValueError, NameError):
        print("{} horse battery staple, that's not a number!".format(choice(errors)))
        continue

print("Making password from {dictlength} words, containing {words} words, of length > {length}"\
      .format(dictlength=len(dictionary), words=length, length=maxchars))

while(True):
    password = []
    colour, cindex = [x for x in range(31, 37)], 0
    for _ in range(length):
        password.extend(choice(dictionary).title())
    for _ in range(extras):
        password.insert(randint(0, len(password)), choice(additions))
    if 0 <= len(password) <= maxchars:
        for letter in password:
            if letter.isupper():
                cindex = (cindex + 1) % len(colour)
            if letter.isalpha() is not True:
                print("{esc}[97m{l}{esc}[{prev}m".format(esc=chr(27), l=letter, prev=colour[cindex]), end="")
            else:
                print("{}{}".format(chr(27) + "[" + str(colour[cindex]) + "m", letter), end="")
        system("echo {} | pbcopy".format("".join(password)))
        print(chr(27) + "[39m\nPassword copied to clipboard.")
        break
