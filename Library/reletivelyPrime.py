def relativelyPrime(a, b, c, d):
    lst = [a, b, c, d]
    bol = False
    for i in lst:
        for j in lst:
            if i != j and relPrimePair(i, j):
                bol = True
    return bol
  
def relPrimePair(a, b):
    if a < b:
        minn = a
    else:
        minn = b
    gcf = 1
    for val in range(2, minn):
        if a%val == 0 and b%val == 0:
            gcf = val
    if val == 1:
        return True
    return False
