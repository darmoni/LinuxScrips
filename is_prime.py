#!/usr/bin/env python3

import math

def atkin(nmax):
    """
    Returns a list of prime numbers below the number "nmax"
    """
    is_prime = dict([(i, False) for i in range(5, nmax+1)])
    for x in range(1, int(math.sqrt(nmax))+1):
        for y in range(1, int(math.sqrt(nmax))+1):
            n = 4*x**2 + y**2
            if (n <= nmax) and ((n % 12 == 1) or (n % 12 == 5)):
                is_prime[n] = not is_prime[n]
            n = 3*x**2 + y**2
            if (n <= nmax) and (n % 12 == 7):
                is_prime[n] = not is_prime[n]
            n = 3*x**2 - y**2
            if (x > y) and (n <= nmax) and (n % 12 == 11):
                is_prime[n] = not is_prime[n]
    for n in range(5, int(math.sqrt(nmax))+1):
        if is_prime[n]:
            ik = 1
            while (ik * n**2 <= nmax):
                is_prime[ik * n**2] = False
                ik += 1
    primes = []
    for i in range(nmax + 1):
        if i in [0, 1, 4]: pass
        elif i in [2,3] or is_prime[i]: primes.append(i)
        else: pass
    if nmax in primes:
           primes.remove(nmax)
    return primes

assert(atkin(30)==[2, 3, 5, 7, 11, 13, 17, 19, 23, 29])


# take input from the user
while True:
    num = int(input("Enter a number: "))

    if num < 0 :
        print ("Come back again soon... Good Bye!!")
        break
    elif 1 == num:
        print ("1 is a primary number. Duh!!!")
    else:
        primes= (atkin(num))
        limit = int(math.sqrt(num)+1)
        print ("will try to find a divider smaller than {}, {}*{}={}".format(limit, limit, limit , limit* limit))
        #for i in range(2,limit,2):
        for i in primes:
            #print ("i=",i);
            if num % i == 0:
                print ("Nope! {} divided by {} is {}".format(num,i,num//i))
                break
        else:
            print (num, "is a primary number")
