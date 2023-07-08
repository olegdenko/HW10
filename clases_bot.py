from collections import UserDict


class Field:
    def __init__(self, value=None) -> None:
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name: Name, phones: Phone = None) -> None:
        self.name = name
        self.phones = []
        if type(phones.value) == list:
            self.phones.extend(phones.value)

        elif phones:
            self.phones.append(phones)

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def __repr__(self) -> str:
        return str(self.phones)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        # print(record.__dict__)


# s = Record("Bill", 123454567)
# t = Record("Jimm", 1234578798)
# # print(s.name)
# # print(s.phones)
# d = AddressBook()
# print(d.data)
# d.add_record(s)
# print(d.data)
# d.add_record(t)
# print(d.data)
# print(d.data["Jimm"].phones[0])


# print(s.get_name())
# s.set_name("Dill")
# print(s.get_name())
