def func(test_str, i):
    if i == len(test_str):
        return
    print(test_str[i])
    func(test_str, i + 1)

if __name__ == '__main__':
    print(func("chicken", 0))