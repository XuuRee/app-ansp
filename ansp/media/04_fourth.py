from random import random, randint

def dice():
    return randint(1,6)


def turn():
    i = dice()
    total = i
    while (i % 2 == 0):
        i = dice()
        total += i
    return total


def dice_freq(count):    
    lst = []
    for i in range(count):
        lst.append(dice())
    for i in range(1,7):
        print(i, "padla", lst.count(i), "krat")


# 4.2.1 (drunkman simulator)
def leftOrRight():
    if (randint(0, 1)):
        return False
    return True


def printPaths(distance, middle):
    print("home", end=" ")
    for i in range(distance):
        if (i == middle):
            print("*", end=" ")
        else:
            print(".", end=" ")
    print("pub")


def homeOrPub(distance, position):
    if (position == 0):
        print("Ended at home!")
        return True
    if (position == distance - 1):
        print("Ended in the pub again!")
        return True
    return False


def drunkman_simulator(distance, steps):    # ... steps, output=False)
    if (distance < 3):
        print("Path too short!")
        return
    position = distance // 2
    printPaths(distance, position)
    for i in range(steps):
        if (leftOrRight()):
            position -= 1
        else:
            position += 1
        printPaths(distance, position)
        if (homeOrPub(distance, position)):
            return
    print("Fall a sleep!")


# 4.2.6 (random student)
    
