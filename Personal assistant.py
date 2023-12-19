# Chagelog for bot version 0.6:
# - added functions for 
# - - add-birthday - add birthday to an existing contact
# - - show-birthday - show birthday of a contact
# - - birthdays - show upcoming birthdays

import re
from datetime import datetime, timedelta
from collections import defaultdict
from rich.console import Console
from rich.table import Table

console = Console()

# Classes
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number format should be max 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        if not re.match(r'\d{2}\.\d{2}\.\d{4}', value):
            raise ValueError("Birthday should be in DD.MM.YYYY format.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name}, phones: {', '.join(map(str, self.phones))}, birthday: {self.birthday}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

# Розділення введеного рядка на команду та аргументи
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

# Декоратор для обробки помилок введення користувача
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format."

    return inner

# Завантаження контактів з текстового файлу
@input_error
def load_contacts(address_book, filename="contacts.txt"):
    try:
        with open(filename, "r") as file:
            for line in file:
                name, phones_str, birthday_str = line.strip().split(":")
                phones = phones_str.split(";")
                record = Record(name)
                for phone in phones:
                    record.add_phone(phone)
                if birthday_str:
                    record.add_birthday(birthday_str)
                address_book.add_record(record)
    except FileNotFoundError:
        pass

# Виведення усіх контактів
@input_error
def list_contacts(address_book):
    if not address_book.data:
        console.print("Contacts not found.")
    else:
        table = Table(title="All Contacts")
        table.add_column("Name 👤", style="cyan", justify="left")
        table.add_column("Phones 📞 ", style="magenta", justify="center")
        table.add_column("Birthday 🎂", style="green", justify="center")

        for record in address_book.data.values():
            phone_str = ', '.join([f"[cyan]{phone}[/cyan]" for phone in record.phones])
            birthday_str = str(record.birthday) if record.birthday else ""
            table.add_row(record.name.value, phone_str, birthday_str)

        console.print(table)

    return ""

# Додавання контакту
@input_error
def add_contact(args, address_book):
    if len(args) == 2:
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
        return "Contact added."
    else:
        raise ValueError("Give me name and phone please. Use add <name> <phone number>")

# Зміна номера телефону
@input_error
def change_contact(args, address_book):
    if len(args) == 2:
        name, new_phone = args
        record = address_book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, new_phone)
            return f"Phone number for {name} changed to {new_phone}."
        else:
            raise KeyError
    else:
        raise ValueError("Give me name and new phone please.")

# Пошук контактів 
def find_contact(args, address_book):
    if len(args) == 1:
        name = args[0]
        record = address_book.find(name)
        if record:
            return f"Phone number(s) for {name}: {', '.join(map(str, record.phones))}, birthday: {record.birthday}."
        else:
            return f"Contact '{name}' not found."
    else:
        raise ValueError("Give me a name to find.")

# Видалення контактів
@input_error
def delete_contact(args, address_book):
    if len(args) == 1:
        name = args[0]
        address_book.delete(name)
        return f"Contact {name} deleted."
    else:
        raise ValueError("Give me a name to delete.")

# Додавання номера для існуючого контакту
@input_error
def add_phone_to_contact(args, address_book):
    if len(args) == 2:
        name, new_phone = args
        record = address_book.find(name)
        if record:
            record.add_phone(new_phone)
            return f"Phone number {new_phone} added to {name}."
        else:
            raise KeyError
    else:
        raise ValueError("Give me name and new phone please.")

# Видалення номера для існуючого контакту
@input_error
def remove_phone_from_contact(args, address_book):
    if len(args) == 2:
        name, old_phone = args
        record = address_book.find(name)
        if record:
            record.remove_phone(old_phone)
            return f"Phone number {old_phone} removed from {name}."
        else:
            raise KeyError
    else:
        raise ValueError("Give me name and phone to remove please.")

# Редагування номера телефону для існуючого контакту
@input_error
def edit_phone_for_contact(args, address_book):
    if len(args) == 3:
        name, old_phone, new_phone = args
        record = address_book.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return f"Phone number {old_phone} for {name} edited to {new_phone}."
        else:
            raise KeyError
    else:
        raise ValueError("Give me name, old phone, and new phone please.")

# Пошук контактів за номером телефона
def find_by_phone(args, address_book):
    if len(args) == 1:
        phone = args[0]
        found_contacts = []
        for record in address_book.data.values():
            if record.find_phone(phone):
                found_contacts.append(record.name.value)
        if found_contacts:
            return f"Contacts with phone number {phone}: {', '.join(found_contacts)}."
        else:
            return f"No contacts found with phone number {phone}."
    else:
        raise ValueError("Give me a phone number to find.")
    
#Додавання дня народження
@input_error
def add_birthday_to_contact(args, address_book):
    if len(args) == 2:
        name, birthday = args
        record = address_book.find(name)
        if record:
            record.add_birthday(birthday)
            return f"Birthday {birthday} added to {name}."
        else:
            raise KeyError
    else:
        raise ValueError("Give me name and birthday (DD.MM.YYYY) please.")
    
# Показ дня народження контакту
@input_error
def show_birthday(args, address_book):
    if len(args) == 1:
        name = args[0]
        record = address_book.find(name)
        if record and record.birthday and record.birthday.value:
            return f"The birthday of {name} is on {record.birthday}."
        elif record:
            return f"{name} doesn't have a specified birthday."
        else:
            raise KeyError
    else:
        raise ValueError("Give me a name to show birthday.")

# Оголошення списку днів тижня
days_of_week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

# Дні народження на наступному тижні
def show_upcoming_birthdays(address_book):
    birthday_next_week = defaultdict(list)
    start_of_year = datetime(year=datetime.now().year, month=1, day=1)
    while start_of_year.weekday() != 0:
        start_of_year += timedelta(days=1)

    for record in address_book.data.values():
        if record.birthday and record.birthday.value:
            val = datetime.strptime(record.birthday.value, "%d.%m.%Y").replace(year=datetime.now().year)

            # Додавання днів, якщо день народження на вихідних
            if val.weekday() >= 5:  # 5 та 6 відповідають суботі та неділі
                val += timedelta(days=(7 - val.weekday()))

            birthday_number_of_week = (val - start_of_year).days // 7

            if birthday_number_of_week == (datetime.now() - start_of_year).days // 7 + 1:
                birthday_next_week[val.weekday()].append(record.name.value)

    print('\nNext week we will congratulate!:\n')

    for el in sorted(birthday_next_week.items(), key=lambda t: t[0]):
        names_to_congratulate = ', '.join(el[1])
        print(f'{days_of_week[el[0]]}: {names_to_congratulate}')


# Збереження контактів у текстовий файл  
@input_error
def save_contacts(address_book, filename="contacts.txt"):
    with open(filename, "w") as file:
        for record in address_book.data.values():
            birthday_str = str(record.birthday) if record.birthday else ""
            file.write(f"{record.name.value}:{';'.join(map(str, record.phones))}:{birthday_str}\n")

# Меню
def display_help():
    print('-' * 45 + '\nMain commands:\n'
                     'hello - greeting message\n'
                     'all - show all contacts\n'
                     'find - number search by name\n'
                     'findphone - search contacts by phone number\n'
                     'add - add new contact\\contact number\n'
                     'change - change contact number\n'
                     'add-phone - add phone number to an existing contact\n'
                     'remove-phone - remove phone number from an existing contact\n'
                     'editphone - edit phone number for an existing contact\n'
                     'add-birthday - add birthday to an existing contact\n'
                     'show-birthday - show birthday of a contact\n'
                     'birthdays - show upcoming birthdays\n'
                     'del - delete contact\\number\n'
                     'help - display all comands  from menu\n' + '-' * 45)


# Команди бота
def main():
    address_book = AddressBook()
    load_contacts(address_book)  # Додайте цей рядок
    print("Greeting you, my young padawan!")
    display_help()
    
    while True:
        user_input = input("Enter command: ")

        # Перевірка на пустий рядок перед викликом parse_input
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_contacts(address_book)
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "all":
            print(list_contacts(address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "find":
            print(find_contact(args, address_book))
        elif command == "del":
            print(delete_contact(args, address_book))
        elif command == "add-phone":
            print(add_phone_to_contact(args, address_book))
        elif command == "remove-phone":
            print(remove_phone_from_contact(args, address_book))
        elif command == "edit-phone":
            print(edit_phone_for_contact(args, address_book))
        elif command == "findphone":
            print(find_by_phone(args, address_book))
        elif command == "add-birthday":
            print(add_birthday_to_contact(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            show_upcoming_birthdays(address_book)
        elif command == 'help':
            display_help()
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

