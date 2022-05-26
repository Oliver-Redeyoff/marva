import os
import pickle

# Creates a given folder
def create_dir(path):
    exists = os.path.exists(path)
    if not exists:
        os.makedirs(path)

# Store data in given file
def store(data, path):
    with open(path, 'wb') as outp:
        if (type(data) == list):
            for item in data:
                pickle.dump(item, outp, pickle.HIGHEST_PROTOCOL)
        else:
            pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)

# Retrieve data from given file
def retrieve(path):
    object_list = []
    with (open(path, "rb")) as openfile:
        while True:
            try:
                object_list.append(pickle.load(openfile))
            except EOFError:
                break
    if (len(object_list) == 1):
        return object_list[0]
    else:
        return object_list