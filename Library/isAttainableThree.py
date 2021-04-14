def isAttainable(a, b, c, val):
    for i in range(int(val/a)):
        for j in range(int(val/b)):
            for k in range(int(val/c)):
                if i*a + j*b + k*c == val:
                    return True
    return False
