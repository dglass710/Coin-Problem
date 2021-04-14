def isAttainable4(a, b, c, d, val):
  'Determines is val is attainable by a combination of a, b, c, and d'
    for i in range(int(val/a) + 1):
        for j in range(int(val/b) + 1):
            for k in range(int(val/c) + 1):
                for l in range(int(val/d) + 1):
                    if i*a + j*b + k*c + l*d == val:
                        return True
    return False
