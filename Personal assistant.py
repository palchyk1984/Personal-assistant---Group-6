import re
from datetime import datetime, timedelta
from collections import defaultdict
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

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

# Додано класс для Email
class Email(Field):
    def __init__(self, value):
        if not is_valid_email(value):
            print("Invalid email format.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        if not re.match(r'\d{2}\.\d{2}\.\d{4}', value):
            raise ValueError("Birthday should be in DD.MM.YYYY format.")
        super().__init__(value)

class Address(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = []
        self.birthday = None

    #Методи для Phone
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


    #Методи для Email
    def add_email(self, email):
        new_email = Email(email)
        self.emails.append(new_email)

    def remove_email(self, email):
        self.emails = [e for e in self.emails if str(e) != email]

    def edit_email(self, old_email, new_email):
        self.remove_email(old_email)
        self.add_email(new_email)

    def find_email(self, email):
        for e in self.emails:
            if str(e) == email:
                return e
        return None
    
    #Методи для Birthday
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


    def edit_birthday(self, new_birthday):
        self.birthday = Birthday(new_birthday)

    #Методи для Adsress
    def add_address(self, address):
        new_address = Address(address)
        self.addresses.append(new_address)

     #Метод remove_address
    def remove_address(self, address):
        self.addresses = [a for a in self.addresses if str(a) != address]

    # Метод edit_address
    def edit_address(self, old_address, new_address):
        self.remove_address(old_address)
        self.add_address(new_address)


    def __str__(self):
        phones_str = ', '.join(map(str, self.phones))
        emails_str = ', '.join(map(str, self.emails))
        birthday_str = str(self.birthday) if self.birthday else ""
        return f"Contact name: {self.name}, phones: {', '.join(map(str, self.phones))}, " \
               f"emails: {', '.join(map(str, self.emails))}, addresses: {', '.join(map(str, self.addresses))}, " \
               f"birthday: {self.birthday}"
        #return f"Contact name: {self.name}, phones: {phones_str}, emails: {emails_str}, birthday: {birthday_str}"



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

# Notes specific Classes

class Tag(Field):                   
    def __init__(self, value):
        if not value.isdigit() or len(value) > 10:
            raise ValueError("Tag should be max 10 digits")
        super().__init__(value)

class Notename(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) > 20:
            raise ValueError("Note name should be max 20 digits")
        super().__init__(value)


class Timestamp():                 
    def __init__(self, ID = 0, ts = datetime.now()):
        self.ts = ts
        self.ID = ID

    def ID(self):
        self.ID += 1
    

    def __str__(self):
        return f'{self.ts} ID: {self.ID}'

class Note(Field):                   
    def __init__(self, value):
        if len(value) > 255:
            raise ValueError("Note should be max 255 digits")
        super().__init__(value)

class NoteRecord:
    def __init__(self, note: Note):
        self.timestamp = Timestamp()
        self.tags = ['no']
        self.note = note

    def __str__(self):
            return f"Note from: {self.timestamp}\n Text: {self.note}\n Tags: {self.tags}\n"
    
class NoteBook:
    def __init__(self):
        self.data = {}

    def add_record_notebook(self, note_record):
        self.data[note_record.timestamp] = note_record

    def show_all_notes(self):
        for note_record in self.data.values():
            print(note_record)
    
    def find_note_day(self, day):
        notes_list_day = []
        for timesnap in self.data:
            if timesnap.ts.day == day:
                notes_list_day = notes_list_day.append(self.data.get(timesnap)) 
        return notes_list_day

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
            return "Contact not found." #Traceback !
        except IndexError:
            return "Invalid command format." #Traceback !

    return inner

# Завантаження контактів з текстового файлу
@input_error
def load_contacts(address_book, filename="contacts.txt"):
    try:
        with open(filename, "r") as file:
            for line in file:
                print(f"Processing line: {line}")
                name, phones_str, emails_str, addresses_str, birthday_str = line.strip().split(":")
                phones = phones_str.split(";")
                emails = emails_str.split(";") if emails_str else []
                addresses = addresses_str.split(";") if addresses_str else []
                record = Record(name)
                for phone in phones:
                    record.add_phone(phone)
                for email in emails:
                    record.add_email(email)
                for address in addresses:
                    record.add_address(address)
                if birthday_str:
                    record.add_birthday(birthday_str)
                address_book.add_record(record)
    except FileNotFoundError:
        pass


# Завантаження ноутів з текстового файлу
@input_error
def load_notes(notebook, filename="notebook.txt"):
    try:
        with open(filename, "r") as file:
            for line in file:
                timestamp_ts_str, timestamp_ID_str, tags_str, note_str = line.strip().split("_")
                #tags = tags_str.split(";")
                note = Note(note_str)
                time_stamp = Timestamp(int(timestamp_ID_str), datetime.strptime(timestamp_ts_str, '%Y-%m-%d %H:%M:%S.%f'))
                note_record = NoteRecord(note)
                note_record.timestamp = time_stamp
                #note_record.tags = tags
                notebook.add_record_notebook(note_record)

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
        table.add_column("Phones 📞", style="magenta", justify="center")
        table.add_column("Emails 📧", style="yellow", justify="center")
        table.add_column("Addresses 🏠", style="blue", justify="center") 
        table.add_column("Birthday 🎂", style="green", justify="center")

        for record in address_book.data.values():
            phone_str = ', '.join([f"[cyan]{phone}[/cyan]" for phone in record.phones])
            email_str = ', '.join([f"[yellow]{email}[/yellow]" for email in record.emails])
            address_str = ', '.join([f"[blue]{address}[/blue]" for address in record.addresses]) 
            birthday_str = str(record.birthday) if record.birthday else ""
            table.add_row(record.name.value, phone_str, email_str, address_str, birthday_str)

        console.print(table)

    return ""


# CONTACT
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

# PHONE NUMBER
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
    
# EMAIL
# Email validation
def is_valid_email(email):
    return re.match(r'\S+@\S+\.\S+', email) is not None

# Add email
@input_error
def add_email_to_contact(args, address_book):
    if len(args) == 2:
        name, new_email = args
        record = address_book.find(name)
        if record:
            if is_valid_email(new_email):
                record.add_email(new_email)
                return f"Email {new_email} added to {name}."
            else:
                return "Invalid email format."
        else:
            raise KeyError 
            #return "Contact not found."
    else:
        raise ValueError ("Give me name and new email please.")
    return ""

#Remove Email
@input_error
def remove_email_from_contact(args, address_book):
    if len(args) == 2:
        name, old_email = args
        record = address_book.find(name)
        if record:
            record.remove_email(old_email)
            return f"Email {old_email} removed from {name}."
        else:
            raise KeyError 
    else:
        raise ValueError("Give me name and email to remove please.")

@input_error
def edit_email_for_contact(args, address_book):
    if len(args) == 3:
        name, old_email, new_email = args
        record = address_book.find(name)
        if record:
            record.edit_email(old_email, new_email)
            return f"Email {old_email} for {name} edited to {new_email}."
        else:
            raise KeyError
    else:
        raise ValueError("Give me name, old email, and new email please.")

# ADDRESS
# Add address
@input_error    
def add_address_to_contact(args, address_book):
    if len(args) == 2:
        name, new_address = args
        record = address_book.find(name)
        if record:
            try:
                record.add_address(new_address)
                return f"Address {new_address} added to {name}."
            except ValueError as e:
                print(str(e))
        else:
            raise KeyError 
    else:
        raise ValueError("Give me name and new address please.")
    return ""


# HAPPY BD
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

# Редагування дня народження контакту
@input_error
def edit_birthday_for_contact(args, address_book):
    if len(args) == 2:
        name, new_birthday = args
        record = address_book.find(name)
        if record:
            old_birthday = record.birthday.value if record.birthday else None
            record.edit_birthday(new_birthday)
            return f"Birthday for {name} edited. Old birthday {old_birthday} replaced by new birthday: {new_birthday}."
        else:
            raise KeyError
    else:
        raise ValueError("Give me name and new birthday (DD.MM.YYYY) please.")
    
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

# NOTES 
# processing user input funtions

def add_record_notebook(args, notebook):
    notebook.add_record_notebook(NoteRecord(' '.join(args)))
    
    return 'Note added to the notebook'


# DATABASE
# Збереження контактів у текстовий файл  
@input_error
def save_contacts(address_book, filename="contacts.txt"):
    with open(filename, "w") as file:
        for record in address_book.data.values():
            birthday_str = str(record.birthday) if record.birthday else ""
            phones_str = ';'.join(map(str, record.phones))
            emails_str = ';'.join(map(str, record.emails))
            addresses_str = ';'.join(map(str, record.addresses))  # Додайте це
            file.write(f"{record.name.value}:{phones_str}:{emails_str}:{addresses_str}:{birthday_str}\n")

def get_valid_commands():
    address_book = AddressBook()
    commands = [
        "close", "exit", "hello", "add", "all", "find",
        "del", "add-phone", "remove-phone", "edit-phone", "find-phone",
        "add-birthday", "show-birthday", "birthdays", "help", "add-email",

        "remove-email", "edit-email", "add-address"
    ]

    # Add dynamically generated commands based on the address book data
    commands += list(address_book.data.keys())

    return commands

def get_user_input():
    completer = WordCompleter(get_valid_commands(), ignore_case=True)
    return prompt("Enter command: ", completer=completer)

# Збереження ноутів у текстовий файл  
@input_error
def save_notes(notebook, filename="notebook.txt"):
    with open(filename, "w") as file:
        for noterecord in notebook.data.values():
            tags_str = ';'.join(map(str, noterecord.tags)) if noterecord.tags else ""
            file.write(f"{noterecord.timestamp.ts}_{noterecord.timestamp.ID}_{tags_str}_{noterecord.note}\n")

# POPUP
# Меню Help

# Опреділити стилі тексту
bold_underline = "bold underline"
yellow_text = "yellow"

# Опреділити стилі тексту
bold_underline = "bold underline"
green_text = "green"
white_text = "white"

# Опреділити стилі тексту
bold_underline = "bold underline"
green_text = "bold green"
white_text = "white"

def display_help():
    console = Console()

    # Виведення заголовка
    console.print("Help Menu", style=bold_underline)

    # Виведення категорій та команд для кожної категорії
    categories = {
        "Main commands": ["hello - greeting message", "help - display all commands from the menu", "close/exit - save added contacts/notes and finish work"],
        "Search": ["all - show all contacts", "find - number search by name", "find-phone - search contacts by phone number"],
        "Contact": ["add - add new contact", "del - delete contact/number"],
        "Phone": ["add-phone - add phone number to an existing contact", "remove-phone - remove phone number from an existing contact", "edit-phone - edit phone number for an existing contact"],
        "Email": ["add-email - add email to an existing contact", "remove-email - remove email from an existing contact", "edit-email - edit email for an existing contact"],
        "Birthday": ["add-birthday - add birthday to an existing contact", "edit-birthday - edit birthday of an existing contact", "show-birthday - show birthday of a contact", "birthdays - show upcoming birthdays"],
        "Address": ["add-address - add address for an existing contact"],
    }

    for category, commands in categories.items():
        console.print(f"\n{category}:", style=bold_underline)
        for command in commands:
            # Виведення рядка з різним кольором для кожного елемента
            console.print(f"[{green_text}]{command.split(' - ', 1)[0]}[/{green_text}] - {command.split(' - ', 1)[1]}", style=white_text)



# Команди бота
def main():
    address_book = AddressBook()
    notebook = NoteBook()
    load_contacts(address_book)
    load_notes(notebook)
    display_help() 
    
    #print("Greeting you, my young padawan!")
    baby_yoda_ascii_art = """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢀⣠⡴⠖⣛⣋⣭⣭⣭⣍⣙⡓⠶⢤⣀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⡴⢋⣥⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣍⡳⣦⡀⠀⠀⠀⠀
    ⠀⠀⢀⡴⢋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠻⣄⠀⠀⠀
    ⠀⠀⠞⣱⣿⣿⣿⣿⣿⣿⠿⠟⠛⢉⠙⠛⠻⢿⣿⣿⣿⣿⣿⣷⡘⣧⠀⠀
    ⠀⢲⣤⣤⣀⡉⠉⠙⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠛⠛⠓⠚⠓⡀
    ⢰⡇⠻⣿⣿⣿⣷⡀⠀⡠⣤⣀⠀⠀⠀ ⠀⡈⢬⣀⠀⢠⣶⣿⣿⣿⣿⢏⠀
    ⢸⡇⣷⣌⡛⠛⠻⠇⠈⠻⠿⠿⠂⠄⠄⠸⠿⠿⠛⠀⠸⠿⠿⠿⣛⡕⢹⠀
    ⠸⡇⣿⣿⣿⣿⣷⣶⣄⣀⣀⣀⣀⣀⣀⣀⣠⣄⣠⣤⣶⣶⣿⣿⣿⡇⣼⠀
    ⠀⢷⠸⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢻⡟⠁⢀⣻⣿⣿⢡⡇⠀
    ⠀⠈⢧⡹⣿⣿⣿⣷⡀⠀⠉⠿⡿⠛⠋⠁⠀ ⠀⣿⣷⣶⣾⣿⡿⢡⡟⠀⠀
    ⠀⠀⠈⠳⣌⠿⣿⣈⣙⠇⠀⠈⡁⠀⠀⠀⠀ ⠀⢻⣿⣿⣿⠟⣵⠏⠀⠀⠀
    ⠀⠀⠀⠀⠙⠳⣌⡛⢿⡀⠀⢀⠀⠀⠀⠀ ⠀⠀⣸⠿⢋⡵⠞⠁⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠈⠙⠲⠦⣭⣘⣒⣒⣒⣒⣨⡭⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """
    style = "bold green"
    console.print(baby_yoda_ascii_art, style=style)

    panel = Panel.fit("Greeting you, my young padawan!", title="My name is baby youda :)", border_style="green")
    console.print(panel)    
    
    
    while True:
        user_input = get_user_input()

        # Перевірка на пустий рядок перед викликом parse_input
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_contacts(address_book)
            save_notes(notebook)
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":                                      # Contact
            print(add_contact(args, address_book))
        elif command == "all":
            print(list_contacts(address_book))
        elif command == "find":
            print(find_contact(args, address_book))
        elif command == "del":
            print(delete_contact(args, address_book))
        elif command == "add-phone":                                # Phone
            print(add_phone_to_contact(args, address_book))
        elif command == "remove-phone":
            print(remove_phone_from_contact(args, address_book))
        elif command == "edit-phone":
            print(edit_phone_for_contact(args, address_book))
        elif command == "find-phone":
            print(find_by_phone(args, address_book))
        elif command == "add-birthday":                             # Happy BD
            print(add_birthday_to_contact(args, address_book))
        elif command == "edit-birthday":
            print(edit_birthday_for_contact(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            show_upcoming_birthdays(address_book)
        elif command == "add-email":                                # EMAIL
            print(add_email_to_contact(args, address_book))
        elif command == "remove-email":
            print(remove_email_from_contact(args, address_book))
        elif command == "edit-email":
            print(edit_email_for_contact(args, address_book))
        elif command == "add-address":                              # Address
            print(add_address_to_contact(args, address_book))
        elif command == 'help':
            display_help()
        elif command == "add-note":                           # NOTES specific command
            print(add_record_notebook(args, notebook))
        elif command == "all-notes":                         
            notebook.show_all_notes()                          # NOTES specific command
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()



