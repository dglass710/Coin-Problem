def apery(a, b, c, d):
    'Takes a quad as input and returns the Apery set assuming were working mod the minimum element'
    workingMod = min(a,b,c,d)
    intList = [0 for _ in range(workingMod)]
    p = 0
    while any(x == 0 for x in intList[1:]): # while at least one element of the apery set has not been found
        if isAttainable4(a, b, c, d, p): # if p is attainable by <a,b,c,d>
            eqClass = p % workingMod
            for val in range(1, workingMod): # val will take on every integer value from 1 to workingMod - 1
                if eqClass == val and intList[val] == 0: # if the attainable is in val eq class and is the first one found
                    intList [val] = p # we alter its index in intList and that effectively marks it when revisited by the above line
        p += 1
    return tuple(sorted(intList))
