from __future__ import print_function
from random import randint, choice
from sys import argv, platform
from os import path

""" python3 password.py [dictionary]

    Creates a password of specified length as described in xkcd.com/936/, eg.
    ManipularUseeBrockEruca, using OSX's builtin dictionary (should work on linux too
    pointing to a correct dictionary)
"""

def paste(text):
    from os import system
    pastecmd = {"darwin": "pbcopy", "win32": "clip"}
    if platform in pastecmd:
        system('echo "{}" | {}'.format(text, pastecmd[platform]))
    else:
        raise "PlatformError"
        

if platform == "win32" and len(argv) == 1:
    input("Windows requires a dictionary file to be located in the first argument!\nPress any key to continue...")
    quit()
try:
    dictionary = open(argv[1], "r") if len(argv) > 1 else open(path.join("/", "usr", "share", "dict", "words"), "r")
    dictionary = dictionary.read().split("\n")
except FileNotFoundError:
    input("Dictionary file not found, try specifying one in arguments or check arguments are correct...")
    quit()

length, maxchars = 0, 0
additions = [chr(x) for x in range(33, 65)]
errors = ("No", "Bad", "Incorrect", "Rude", "Wrong", "Silly", "Spurious", ":/")

while (True):
    try:
        length = int(input("How many words? "))
        extras = int(input("How many extra characters would you like to add? "))
        maxchars = int(input("Maximum password length? (minumum {}) ".format((length * 4) + extras)))
        if length < 1 or 1 < maxchars < length * 4 + extras:
            print("Length must be 4 * words + extra characters i.e. 4 words, 17 characters")
            continue
        else:
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
        print(chr(27) + "[39m", end="")
        try:
            paste("".join(password))
            print("Password copied to clipboard...")
        except:
            pass
        break
