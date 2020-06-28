import numpy as np
import random

words = np.genfromtxt('words.txt', dtype='U')
MaxInt = words.size
string = ''

for i in range(20):
    if i % 10 == 9:
        string += '\n'
    string += words[random.randint(0, MaxInt)]+' '

print(string)
