DEBUG = 1

def Lerp(norm, min, max):
    return (max - min) * norm + min


def dPrint(str):
    if DEBUG == 1:
        print(str)