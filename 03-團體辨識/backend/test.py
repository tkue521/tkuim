import pickle
from pprint import pprint
objects = []
with (open("encodings.pickle", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break
pprint(objects[0].get('names'))