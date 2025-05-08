#!/usr/bin/python3

import datetime
import random
import time

class MultiplicationType:
  def __init__(self):
    pass
  def operation(self, x, y):
    return x * y
  def symbol(self):
    return "x"
  def word(self):
    return "multiplication"

class AdditionType:
  def __init__(self):
    pass
  def operation(self, x, y):
    return x + y
  def symbol(self):
    return "+"
  def word(self):
    return "addition"
  
type = MultiplicationType()

n = int(input(f"How many {type.word()} problems do you want? You will be timed.\n"))
X = int(input(f"Enter a number to focus on (or 0 to practice all numbers)?\n"))

print("Get ready!")
for i in range(3):
  print(f"{3-i}")
  time.sleep(0.1)
print("Go!")
time.sleep(1)

t = time.time()
n_wrong_total = 0

for i in range(n):
  x = random.randint(0, 10) if X == 0 else X
  y = random.randint(0, 10)
  z = type.operation(x, y)
  
  a, n_wrong = -1, 0
  while a != z:
    a = input(f"{x} {type.symbol()} {y} = ")
    try:
      a = int(a)
    except:
      print("You did not enter a valid number.")
      continue
    if a != z:
      n_wrong_total += 1
      n_wrong += 1
      if isinstance(type, MultiplicationType) and n_wrong == 1:
        def rc_str(rc):
          s = f"{rc + 1}"
          while len(s) < 3:
            s = " " + s
          return s
        print("\n   ", end="")
        for c in range(y):
          print(rc_str(c), end="")
        print()
        for r in range(x):
          print(rc_str(r), end="")
          for c in range(y):
            print("  *", end="")
          print()
        print("\nTry again, counting the stars above if that helps.\n")
      else:
        print(f"{x} {type.symbol()} {y} = {z}!!! Type that to show you are learning:")

dt = time.time() - t
pct = 100 * (1 - n_wrong_total / n)
now = datetime.datetime.now().strftime("%m/%d %H:%M")

print("You finished {:d} {} problems in {:.1f} seconds!".format(n, type.word(), dt))
print("That's {:.1f} seconds per problem!!".format(dt/n))
print(f"You got {n_wrong_total} wrong out of {n}.")
print("That's an accuracy of {:.1f}%!".format(pct))

with open("summaries.txt", "a") as f:
  print("{}: {:.1f} / {} = {:.1f} sec/prob, at {:.1f}% (#: {})".format(now, dt, n, dt/n, pct, X), file=f)
