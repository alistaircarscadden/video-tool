from random import randint
from time import time


def generate_filename(extension=''):
    '''Generate a (very probably) unique filename with the given `extension`. Include the dot in the extension.'''
    x = int(time() * 1000)
    y = randint(0x0, 0xFFFF)
    return f'v_{x}_{y:04}{extension}'
