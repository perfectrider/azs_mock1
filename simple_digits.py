def find_sdigits(n):
    sdigits = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            sdigits.append(num)
    return sdigits

print(find_sdigits(1000))
