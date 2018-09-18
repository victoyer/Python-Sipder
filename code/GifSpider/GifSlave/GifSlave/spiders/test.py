def tests(num: int):
    if num == 1 or num == 0:
        return 1

    return num * tests(num - 1)


if __name__ == '__main__':
    print(tests(900))
