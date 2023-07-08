import os
import re
from collections import UserDict

# import clases_bot
from clases_bot import AddressBook, Record, Name, Phone

new_phonebook = AddressBook()


def load_phonebook(phonebook):
    try:
        with open("phonebook.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                n, p = line.strip().split(":")
                name = Name(n)
                phone = Phone(p.split(","))

                contact = Record(name, phone)
                phonebook.add_record(contact)
    except FileNotFoundError:
        pass
    return phonebook


def save_phonebook(phonebook):
    patern = rf"[\[\]]"
    with open("phonebook.txt", "w") as file:
        for name, value in phonebook.data.items():
            i = re.sub(patern, "", str(value))
            file.write(f"{name}:{i}\n")


phonebook = load_phonebook(new_phonebook)


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Invalid command"
        except TypeError:
            return "Please provide the necessary parameters"

    return wrapper


@input_error
def hello(name=None):
    if name is None:
        name = os.environ.get("USERNAME")
    return f"How can I help you, {name}?"


@input_error
def add_contact(name=None, phone=None):
    if name is None or phone is None:
        return "Please provide a name and phone number"

    phonebook[name] = phone
    return f"Contact {name} with phone {phone} added"


@input_error
def del_contact(name=None):
    if name is None:
        return "Please provide a name"

    if (
        name in phonebook
        and "yes" == input(f"Are you sure delete {name}: Yes/No :").lower()
    ):
        del phonebook[name]
        return f"Contact {name} deleted"
    else:
        return f"Contact {name} does not exist in the phonebook"


@input_error
def change_phone(name=None, phone=None):
    if name is None or phone is None:
        return "Please provide a name and phone number"

    if name in phonebook:
        phonebook[name] = phone
        return f"Phone number for contact {name} changed to {phone}"
    else:
        return f"Contact {name} does not exist in the phonebook"


@input_error
def get_phone(name=None):
    if name is None:
        return "Please provide a name"

    return phonebook[name]


@input_error
def show_all(phonebook):
    if not phonebook:
        return "Phonebook is empty"

    contacts = "\n".join(f"{name}: {phone}" for name, phone in phonebook.items())
    return contacts


OPERATIONS = {
    hello: ("hello",),
    add_contact: (
        "+",
        "плюс",
        "додай",
        "add",
    ),
    del_contact: (
        "del",
        "delete",
        "remove",
        "видалити",
    ),
    change_phone: (
        "change",
        "змінити",
    ),
    get_phone: (
        "phone",
        "номер",
    ),
    show_all: (
        "show all",
        "все",
    ),
}


def handler(user_input):
    for func, operations in OPERATIONS.items():
        for operation in operations:
            if user_input.startswith(operation):
                if operation == "hello":
                    return func()
                elif operation in ("show all", "все"):
                    return func(phonebook)
                else:
                    params = user_input[len(operation) + 1 :].split(" ", 1)
                    return func(*params)
    return "Invalid command"


def main():
    while True:
        user_input = input("Waiting... ").lower()

        if user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            save_phonebook(phonebook)
            break
        result = handler(user_input)
        print(result)


if __name__ == "__main__":
    main()
