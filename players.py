"""
Created on Sun Oct  31 15:01:50 2020
@author: Viswanathan A
@Descirpion : Player Class with CLass Methods

"""

class Players:
    """A sample Player class"""

    def __init__(self, first, last, HighScore=0):
        self.first = first.upper()
        self.last = last.upper()
        self.HighScore = HighScore

    @property
    def HighestScore(self):
        print('{} {} High Score is {}'.format(self.first, self.last,self.HighScore))

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "Employee('{}', '{}', {}, {})".format(self.first, self.last, self.HighScore)