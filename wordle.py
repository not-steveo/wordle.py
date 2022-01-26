from itertools import permutations
import enchant


print(" ______________________________________________________________________ ")
print("|  __    __    ___    ____    ___     _        ___        ____  __ __  |")
print("| |ww|__|ww|  /ooo\  |rrrr\  |ddd\   |l|      /e__]      |pppp\|yy|yy| |")
print("| |ww|ww|ww| |ooooo| |rrRrr) |dddd\  |l|     /ee[_       |ppPpp)yy|yy| |")
print("| |ww|ww|ww| |ooOoo| |rrrr/  |ddDdd| |l|    |eeee_]      |ppp_/|yy~yy| |")
print("| |ww`ww'ww| |ooooo| |rrrr\  |ddddd| |l|___ |eee[_   __  |pp|  |___,y| |")
print("|  \wwwwww/  |ooooo| |rr.rr\ |ddddd| |lllll||eeeee| |..| |pp|   ___|y| |")
print("|   \_/\_/    \___/  |__|\_| |_____| |_____||_____| |__| |__|  |____/  |")
print("|______________________________________________________________________|\n")

print("For best results, guess 1-2 times to get at least 2 known letters and")
print("eliminate some possible letters. You will then be asked to enter all ")
print("known letters, and then asked which letters you can eliminate from the")
print("possible alphabet. Finally, a list of possible words will be generated")
print("based on the information provided.\n")


known = "#####"
known_letters = []  # for letters that are known but not sure of position

# get known letters
while True:
  print("Letters known:", known, known_letters)
  response = input("Do you know any letters that aren't shown above? (Y/N) -> ")
  if response.upper() == "Y":
    letter = input("What is the letter? -> ")
    if len(letter) == 1 and letter.isalpha():
      position = input("What position is this letter? (-1=unknown, 0=first letter, 4=fifth letter) -> ")
      try:
        pos_int = int(position)
        if  0 <= pos_int and pos_int <= 4:
          new_str = known[:pos_int] + letter.upper() + known[pos_int + 1:]
          known = new_str
          print("String updated, new string is:", known, "and addt'l letters:", known_letters, "\n")
        elif pos_int == -1:
          known_letters.append(letter.upper())
          print("String updated, new string is:", known, "and addt'l letters:", known_letters, "\n")
        else:
          print("Invalid input. Please ensure you are entering a single digit between 0 and 4.\n")
      except:
        print("Invalid input. Please ensure you are entering a single digit between 0 and 4.\n")
    else:
      print("Invalid input. Please ensure you are entering a single, valid character.\n")
  else:
    if response.upper() == "EXIT":
      exit()
    else:
      print("All known letters input, next you will be able to eliminate letters that can't be in the answer.")
      break

print("")

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# get available letters
while True:
  print("Current available letters:", alphabet)
  response = input("Would you like to eliminate letters? (Y/N) -> ")
  if response.upper() == "Y":
    elim = input("Enter letters to eliminate, without spaces (ex: RSOTB...) -> ")
    if elim.isalpha():
      new_alpha = ""
      for letter in alphabet:
        if letter not in elim.upper():
          new_alpha += letter
      alphabet = new_alpha
    else:
      print("Invalid input. Please ensure you are only entering letters.\n")
  else:
    if response.upper() == "EXIT":
      exit()
    else:
      if len(alphabet) < 26:
        print("\nAlphabet shortened to:", len(alphabet), "- calculating permutations.")
      else:
        print("\nNo letters eliminated - calculating permutations.")
      break

# how many letters do we need to find?
spots = known.count("#")

avail_letters = []

for let in (alphabet * 3):  # to account for double letter words, and the off chance of a triple letter repeat
  avail_letters.append(let)

# all possible letter combos based on the available letters
permutations = ["".join(map(str, comb)) for comb in permutations(avail_letters, spots)]

word_checker = enchant.Dict("en_US")

possible_words = []
checked_perms = []

# create words by looping over permutations, check them using PyEnchant
for comb in permutations:
  if comb not in checked_perms:
    valid = False
    if len(known_letters) > 0:
      # check that all letters are in the current combination
      sub_check = [let for let in known_letters if let in comb]
      if len(known_letters) == len(sub_check):
        # valid combination, continue
        valid = True
    else:
      # if no known letters, we will try every permutation
      valid = True

    if valid:
      word = known
      for let in comb:
        word = word.replace("#", let, 1)
      if word not in possible_words:
        if word_checker.check(word):
          possible_words.append(word)
    checked_perms.append(comb)

print("\nFrom", len(permutations), "possible permutations,", len(possible_words), "words were generated.")

count = 0
print("\n----------WORDS GENERATED----------")
for ans in sorted(possible_words):
  count += 1
  print("{}. {}".format(count, ans))
print("-----------------------------------\n")
