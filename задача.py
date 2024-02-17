def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args  # Змінено, щоб повертати список аргументів

from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10: #Реалізовано валідацію номера телефону
            raise ValueError("Phone number must contain 10 digits")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name) # Об'єкт типу Name зберігається в атрибуті name
        self.phones = [] # Список об'єктів типу Phone зберігається в атрибуті phones

    def add_phone(self, phone_number): # Додає новий номер телефону до списку
        self.phones.append(Phone(phone_number))
 
    def remove_phone(self, phone_number): # Видаляє номер телефону зі списку
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone, new_phone): # Ззмінює існуючий номер телефону на новий номер
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone_number): # шукає номер телефону в списку
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for record in self.data.values():
            if record.name.value == name:
                return record
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def main():
    contacts = AddressBook()  # Змінено на AddressBook, тепер contacts це адресна книга
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)  

        if command in ['exit', 'close']:
            print("Good bye!")
            break
        elif command == 'hello':
            print("How can I help you?")
        elif command == 'add':
            name, phone = args
            try:
                record = Record(name)
                record.add_phone(phone)
                contacts.add_record(record)
                print("Contact added.")
            except ValueError as e:
                print(e)
        elif command == 'change':
            name, new_phone = args
            record = contacts.find(name)
            if record:
                try:
                    record.edit_phone(record.phones[0].value, new_phone)
                    print("Contact updated.")
                except ValueError as e:
                    print(e)
            else:
                print("Contact not found.")
        elif command == 'phone':
            name, = args
            record = contacts.find(name)
            if record:
                print(f"\n{name}'s phone number: {record.phones[0].value}")
            else:
                print("Contact not found.")

        elif command == 'find':
            name, = args
            record = contacts.find(name)
            if record:
                 print(f"Found record: {record}")
            else:
                 print("Record not found.")

        elif command == 'delete':
            name, = args
            if name in contacts.data:
                contacts.delete(name)
                print(f"Record '{name}' deleted successfully.")
            else:
                print("Record not found.")
                 
        elif command == 'all':
            if contacts:
                result = "All contacts:"
                for name, record in contacts.data.items():
                    result += f"\n{name}: {record.phones[0].value}"
                print(result)
            else:
                print("Phonebook is empty.")
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()                                                                