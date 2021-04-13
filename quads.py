import time
from HumanTime import TimeAutoShort

'''Usage:
    When creating a dadabase, simply call Frobenius(n) where n is the largest such d for <a,b,c,d>
    It will store one of four messages depending on 3 and 4 element reduction
    If gcd(a,b,c,d) != 1, it will say all four elements share a common factor (there is no Frobenius number in this case)
    If gcd(x,y,z) != 1 for and three x,y,z in {a,b,c,d} it will say three elements have a common factor and we know 
    <a.bn,cn.dn> has symmetry iff <a,b,c,d> does
    Otherwise, if <a,b,c,d> is symmetric it will say True and False if its not'''
class Frobenius(object):
    '''a Frobenius object used for research on Frobenius symmetry, specifically the symetry of attainables and unattainables 
    less than or equal to the Frobenius number it's main method allows for the checking of all sets of the form {a,b,c,d} where, 
    a, b, c, d < num with F.main(num) and num is some natural number such that F is a Frobeinius object
    The constructor calls the main method for convenience and can easily be adjusted for command line use'''

    def __init__(self, n, t = 1.5):
        '''constructor for the Frobenius object. mode = N for normal mode with sets obaying three way reletive primality 
        or mode = PW for piecewise reletively prime sets only'''
        self.fractions = []  # a list that will contain the ratio of attainables to total as floating point numbers
        self.fractionsDict = {} # a dictionary whos keys are the contents of self.fractions and whos values are strings representing their corrisponding sets
        self.itime = time.time(); self.progCounter = self.itime # two floats initialized to unix time in seconds for use in the progress method
        self.valsList = []
        self.data = dict()
        self.main(n, t)

    def main(self, n, t):
        num = n + 1 # makes the sets include all values up to and including num
        valsCovered = self.checkVals(n, t)
        b = open(f'{n}quad.txt', 'w')
        for key, value in self.data.items():
            #if value in [True, False]:
            b.write(f'{key[0]}\n{key[1]}\n{key[2]}\n{key[3]}\n{value}\n\n')
        b.close()

    def checkVals(self, n, inc = 1):
        '''checkVals acts as an iterator of sorts going though each value for a, b, c, and d between xmin and xmax for x in [a, b, c, d]'
        totalVals is calculated using the formula for the tetrahedral (or triangular pyramidal) numbers shifted two
        this is only accurate because a<b, b<c, and c<d 
        otherwise this will look at permutations of sets which is redundant'''
        totalVals = int((n - 5) * (n - 1) * (n)/6) ## this is the amount of iterations when a<b and b<c
        valsCovered = 0
        for a in range(3, n - 2):
            for b in range(a, n - 1):
                for c in range(b, n):
                    for d in range(c, n + 1):
                        if a < b and b < c and c < d:
                            tmp = self.Frob(a, b, c, d)
                            if tmp != None:
                                if self.validQuad(a, b, c, d):
                                    tmp1 = '{' + f'{a}, {b}, {c}' + '}'
                                    if tmp[0] == .5:
                                        self.data[(a, b, c, d)] = True
                                    else:
                                        self.data[(a, b, c, d)] = False
                                else:
                                    self.data[(a, b, c, d)] = 'Three elements share a common factor'
                            else:
                                self.data[(a, b, c, d)] = 'All elements share a common factor'
                    valsCovered += 1
                    self.progress(valsCovered, totalVals, inc)
        print(f'100 % {TimeAutoShort(time.time() - self.itime, 2)}')
        return valsCovered

    def validQuad(self, a, b, c, d):
        return self.gcd3(a, b, c) == 1 and self.gcd3(a, b, d) == 1 and self.gcd3(a, c, d) == 1 and self.gcd3(b, c, d) == 1

    def gcd3(self, x, y, z):
        'returns the greatest common denominator of x and y'
        smaller = min([x, y, z])
        for i in range(1, smaller+1):
            if((x % i == 0) and (y % i == 0) and (z % i ==0)):
                hcf = i 
        return hcf

    def Frob(self, a, b, c, d):
        'returns a string representing the valid sets as a string along with a float representing the ratio of attainable values to total values <= F'
        if self.relPrime(a, b, c, d):
            threeSmallest = []
            attainables = 0
            totalVals = 0
            inARow = 0
            for element in [a, b, c, d]:
                if element != max([a, b, c, d]):
                    threeSmallest.append(element)
            self.valsList = []
            for val in range(a*b*c):
                if self.isAttainable(val, a, b, c, d):
                    attainables += 1
                    inARow += 1
                    self.valsList.append(val)
                else:
                    inARow = 0
                totalVals += 1
                if inARow == min([a, b, c, d]):
                    totalVals -= inARow
                    attainables -= inARow
                    break
            if element == a*b*c*d-1:
                print(f'The for loop broke naturally for {{{a}, {b}, {c}}}')
            return float(attainables)/totalVals, totalVals - 1

    def isAttainable(self, val, a, b, c, d):
        'returns True if val can be attained by a linear combination of a, b, and c'
        if val == 0:
            return True
        if any(val - x in self.valsList for x in [a, b, c, d]):
                return True
        for i in range(int(val/a) + 1):
            for j in range(int(val/b) + 1):
                for k in range(int(val/c) + 1):
                    for l in range(int(val/d) + 1):
                        if a * i + b * j + c * k + d * l == val:
                            self.valsList.append(val)
                            return True

    def relPrime(self, a, b, c, d):
        'returns true if a, b, and c are all relatively prime either pair wise for mode PW or for all three if mode is N'
        # if a not in [0, 1] and b not in [0, 1] and c not in [0, 1] and d not in [0, 1]:
        if not any((x in [0, 1] for x in [a, b, c, d])):
            return self.gcd4(a, b, c, d) == 1 
        return False

    def gcd4(self, i, j, k, l):
        'returns the greatest common denominator of x and y'
        smaller = min([i, j, k, l])
        for n in range(1, smaller+1):
            if i % n == 0 and j % n == 0 and k % n ==0 and l % n ==0:
                hcf = n 
        return hcf

    def reducedNotRedundant(self, a, b, c):
        tmp = self.gcd(a, b) 
        a = a//tmp
        b = b//tmp
        tmp = self.gcd(b, c) 
        b = b//tmp
        c = c//tmp
        tmp = self.gcd(a, c) 
        a = a//tmp
        c = c//tmp
        return self.notRedundant(a, b, c)

    def notRedundant(self, a, b, c):
        if self.isAttainableTwo(a, b, c) or self.isAttainableTwo(b, c, a) or self.isAttainableTwo(a, c, b):
            return False
        return True

    def isAttainableTwo(self, a, b, val):
        'returns True if val can be attained by a linear combination of a, b, and c'
        if val == 0:
            return True
        for i in range(int(val/a) + 1):
            for j in range(int(val/b) + 1):
                if a * i + b * j == val:
                    return True

    def isInt(self, b):
        intList = []
        if 2*b//3 == 2*b/float(3):
            intList.append(2*b/3)
        if 3*b//2 == 3*b/float(2):
            intList.append(3*b/2)
        return intList
       
    def isInt(self, a, b):
        intList = []
        for num1 in range(2, a-2):
            for num2 in range(3, a-2+1):
                if num1/float(num2) != num1//num2 and num2/float(num1) != num2//num1 and num1 + num2 <= a: # if a/b and b/a cannot be reduced to an integer
                    if num1*b//num2 == num1*b/float(num2):
                        if num1*b//num2 not in (a, b):
                            intList.append(num1*b/num2)
                    if num2*b//num1 == num2*b/float(num1):
                        if num2*b//num1 not in (a, b):
                            intList.append(num2*b/num1)
        return intList

    def FrobTwo(self, a, b):
        if self.gcd(a, b) == 1:
            twoSmallest = []
            attainables = 0
            totalVals = 0
            inARow = 0
            for element in [a, b]:
                if element != max([a, b]):
                    twoSmallest.append(element)
            for val in range(a*b-a-b+1):
                if self.isAttainableTwo(a, b, val):
                    attainables += 1
                    self.valsList.append(val)
                else:
                    inARow = 0
                totalVals += 1
            return attainables/float(totalVals), a * b - a - b

    def gcd(self, x, y):
        'returns the greatest common denominator of x and y'
        if x > y:
            smaller = y
        else:
            smaller = x
        for i in range(1, smaller+1):
            if((x % i == 0) and (y % i == 0)):
                hcf = i 
        return hcf

    def progress(self, valsCovered, totalVals, inc):
        'displays to the screen both the percentage of completion and the execution time formatted with TimeAutoShort from a module i created'
        if self.progCounter < time.time() - inc:
            self.progCounter = time.time()
            print(f'{valsCovered*100/float(totalVals):.4f} % {TimeAutoShort(time.time() - self.itime, 2)}')

R = Frobenius(180)
#for val in range(10, 110, 10):
#    Frobenius(val)
