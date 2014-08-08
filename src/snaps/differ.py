
from difflib import ndiff, restore

class DiffContent:

    def __init__(self):pass

    @classmethod
    def get_diff(cls, c_o, c_n):

        if c_o is not None and c_n is not None:
            diff = ndiff(c_o, c_n)
        else:
            diff = []

        return diff

    @classmethod
    def get_original(cls, diff):

        return ''.join(restore(diff, 1))


    @classmethod
    def get_revised(cls, diff):

        return ''.join(restore(diff, 2))

