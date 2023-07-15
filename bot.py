import os
from clases_bot import AddressBook, Record, Name, Phone

new_phonebook = AddressBook()


def load_phonebook(phonebook):
    try:
        with open("phonebook.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                n, p = line.strip().split(":")
                name = Name(n)
                phones = [Phone(phone.strip()) for phone in p.split(",")]

                contact = Record(name, phones)
                phonebook.add_record(contact)
    except FileNotFoundError:
        pass
    return phonebook


def save_phonebook(phonebook):
    with open("phonebook.txt", "w") as file:
        for name, record in phonebook.data.items():
            if isinstance(record, Record):
                phones = [
                    phone.value if isinstance(phone, Phone) else phone
                    for phone in record.phones
                ]
                phones_str = ", ".join(phones)
                file.write(f"{name}:{phones_str}\n")
            else:
                file.write(f"{name}:{record}\n")


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
def add_contact(name, phone=None):
    if phone:
        phones = [Phone(p.strip()) for p in phone.split(",")]
        phonebook.add_record(Record(Name(name), phones))
        return f"Contact {name} with phone {phone} added"
    else:
        phonebook.add_record(Record(Name(name)))
        return f"Contact {name} added"


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
        phones = [Phone(p) for p in phone.split(",")]
        record = Record(Name(name), phones)
        phonebook.add_record(record)
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

    contacts = "\n".join(
        f"{name}: {', '.join([phone.value if isinstance(phone, Phone) else Phone(phone).value for phone in record.phones])}"
        for name, record in phonebook.items()
        if isinstance(record, Record)
    )
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
        "get",
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
