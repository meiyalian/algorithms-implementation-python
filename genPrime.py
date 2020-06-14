import random
import sys

def generate_randomPrime(k):
    if k == 1:
        return 1

    while True:
        random_num = random.randint(2 ** (k - 1), (2 ** k) - 1)

        result = miller_rabin_test(random_num)

        if result == "Probably_Prime" or result == "Proven_Prime":
            break
    return random_num




def miller_rabin_test(num):
    """
        Implementation of mille rabin test
        Parameter: integer number
        Return: String "Proven_Prime" or "Composite" or "Probably_Prime"

        Time Complexity: O(log(n)) where n is the input number
        Space complexity: O(log(n)) ( the value of s )
    """
    if num == 1 or num==2:
        return "Proven_Prime"

    if num %2 ==0:
        return "Composite"
    s = 0
    t = num-1

    while t%2 == 0:
        s +=1
        t = t//2

    k = 50  # set up level of accuracy
    if num < k:
        k = num - 1

    for i in range(k):

        a =random.randint(2, num-1)

        base = modular_exponentiation(a, t, num)
        results = [base] # an array storing s values
        for i in range(s):
            result = (results[-1]**2 ) % num
            results.append(result)
        if results[-1] != 1:
            return "Composite"
        for i in range(len(results)-1,0,-1):
            if results[i] == 1 and (results[i-1] != 1 and results[i-1] -num != -1 ):
                return "Composite"
    return "Probably_Prime"


def modular_exponentiation(a,b,n):
    """
        Iimplementation of repeating squaring
        Parameter: a: base value , b: power, n: mod value
        Return: result of a^b mod n
        Time Complexity: O(Nlog(x)) where n is the length of the binary string of b and x is the decimal value of b
        Space Complexity: O(1)

    """
    binary = str(bin(b))[2:]
    result = 1
    val = a % n
    for i in range(len(binary)-1, -1, -1):
        if binary[i] == "1":
            result = (result*val) % n
        val = (val * val) % n

    return result


def main(argv):
    if len(argv) != 1:
        print("genPrime.py <k>")
        sys.exit()
    else:
        try:
            num = int(argv[0])
        except ValueError:
            print("genPrime.py <k>")
            sys.exit()

        prime = generate_randomPrime(num)
        print(prime)


if __name__ =="__main__":
    main(sys.argv[1:])
