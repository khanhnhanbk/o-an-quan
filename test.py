import time
data = [10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5]


def moved(index, direc):
    current = index + direc
    while data[index]:
        data[index] -= 1
        data[current] += 1
        current += direc
        current %= 12
        print(data)
        time.sleep(0.1)
    if data[current] == 0:
        res = 0
        while data[current] == 0:
            current += direc
            current %= 12
            if data[current]:
                res += data[current]
                data[current] = 0
                current += direc
                current %= 12
            else:
                return res
        return res
    elif current in (0, 6):
        return 0
    else:
        return moved(index=current, direc= direc)

print(data)

print(moved(3, -1))

print(data)


print(moved(11, -1))

print(data)


# print(moved(2, -1))

# print(data)
