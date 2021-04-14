from isAttainableThree.py import isAttainable

def nonRedundant(a, b, c, d):
    if not isAttainable(a, b, c, d) and not isAttainable(a, b, d, c) and not isAttainable(a, c, d, b) and not isAttainable(b, c, d, a):
        return True
