
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


n = int(input("Enter the value of n: "))


prime_sum = 0
primes = []
for i in range(1, n + 1):
    if is_prime(i):
        prime_sum += i
        primes.append(i)


print(primes)
print(f"The sum of all prime numbers between 1 and {n} is: {prime_sum}")
