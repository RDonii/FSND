import random

all = [1, 2, 3, 4, 5]
previous = [1, 5]

def random_choice(all_items, previous_items):
    restart = True
    while restart:
        get_random = random.choice(all_items)
        for i in previous_items:
          if get_random == i:
            restart = True
            break
          else:
            restart = False
    return get_random

outer = random_choice(all, previous)
print(outer)