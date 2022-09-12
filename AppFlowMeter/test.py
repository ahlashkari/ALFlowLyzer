#!/usr/bin/env python3


import threading

def print_cube(num):

    j = 0
    for i in range(100000000):
        j += 1
    print("Cube: {}" .format(num * num * num))


def print_square(num):
    j = 0
    for i in range(5000000):
        j += 1
    print("Square: {}" .format(num * num))

def print_me(num, name):
    if name == "square":
        print_square(num)
    else:
        print_cube(num)

if __name__ =="__main__":
    t1 = threading.Thread(target=print_me, args=(10,"square",))
    t2 = threading.Thread(target=print_me, args=(10,"cube",))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Done!")
