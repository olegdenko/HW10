phonebook = {}


def adding(x, y):
    return x + y


def multiplying(x, y):
    return x * y


def substraction(x, y):
    return x - y


OPERATIONS = {
    adding: ("+", "плюс", "додай", "add"),
    multiplying: ("*",),
    substraction: ("-",),
}


def main():
    x = 10
    y = 5
    while True:
        user_input = input("Waiting... ")

        if not user_input:
            break
        for func, opertions in OPERATIONS.items():
            if user_input in opertions:
                print(func(x, y))


if __name__ == "__main__":
    main()
