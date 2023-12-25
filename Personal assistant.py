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

## Classes

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

    # Phone
        
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

    # Email

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
    
    # Birthday

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def edit_birthday(self, new_birthday):
        self.birthday = Birthday(new_birthday)

    # Adsress
        
    def add_address(self, address):
        new_address = Address(address)
        self.addresses.append(new_address)

    def remove_address(self, address):
        self.addresses = [a for a in self.addresses if str(a) != address]

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
        if len(value) > 10:
            raise ValueError("Tag should be max 10 characters")
        super().__init__(value)


    def __str__(self):
        return str(self.value)
    
noteID = 0

class Timestamp():                 
    def __init__(self, noteID, ts):
        self.ts = ts
        self.noteID = noteID

    def increment_ID(self):
        self.noteID += 1
    
    def __eq__(self, other):
        return self.ts == other.ts

    def __ne__(self, other):
        return self.ts != other.ts

    def __lt__(self, other):
        return self.ts < other.ts

    def __gt__(self, other):
        return self.ts > other.ts

    def __le__(self, other):
        return self.ts <= other.ts

    def __ge__(self, other):
        return self.ts >= other.ts
    
    def __str__(self):
        return f'{self.ts} ID: {self.noteID}'
    
class Note(Field):                   
    def __init__(self, value):
        if len(value) > 255:
            raise ValueError("Note should be max 255 symbols")
        super().__init__(value)

class NoteRecord():
    
    def __init__(self, note: Note, note_name=""):
        global noteID
        #super().__init__(noteID)
        
        noteID = noteID + 1
        self.timestamp = Timestamp(noteID, datetime.now())
        self.tags = ['no']
        self.note = note
        self.note_name = note_name

    def __str__(self):
        tags_str = ', '.join(map(str, self.tags))
        return f"Note from: {self.timestamp}\n Name: {self.note_name}\n Text: {self.note}\n Tags: {tags_str}\n"
    
class NoteBook:
    def __init__(self):
        self.data = {}

    def add_record_notebook(self, note_record):
        self.data[note_record.timestamp.ts] = note_record

    #def show_all_notes(self):
        #for note_record in self.data.values():
            #print(note_record)
    
    def find_note_day(self, day):
        notes_list_day = []
        for timesnap in self.data:
            if timesnap.ts.day == day:
                notes_list_day = notes_list_day.append(self.data.get(timesnap)) 
        return notes_list_day

    def delete(self, searchID):
        for ts, note_record in self.data.items():
            
            if note_record.timestamp.noteID == searchID:
                ts_to_delete = ts

        return self.data.pop(ts_to_delete)

    def get_maxID(self):
        return self.data[-1].noteID
    
    def find_ID(self, searchID):
        for ts, note_record in self.data.items():
            
            if note_record.timestamp.noteID == searchID:
                return note_record
            
    def find_date_slot(self, start_date = datetime.now() - timedelta(days = 1), end_date = datetime.now()):
        date_slot_list = []
        for ts, note_record in self.data.items():
            if note_record.timestamp.ts >= start_date and note_record.timestamp.ts <= end_date:
                date_slot_list.append(note_record)
        return date_slot_list
    
    def find_name(self, name):
        name_note_list = []
        for ts, note_record in self.data.items():
            if note_record.note_name == name:
                name_note_list.append(note_record)
        return name_note_list
        
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
                timestamp_ts_str, timestamp_ID_str, tags_str, note_str, note_name = line.strip().split("_")
                tags = tags_str.split(", ")
                note = Note(note_str)
                time_stamp = Timestamp(int(timestamp_ID_str), datetime.strptime(timestamp_ts_str, '%Y-%m-%d %H:%M:%S.%f'))
                note_record = NoteRecord(note)
                note_record.timestamp = time_stamp
                note_record.tags = tags
                note_record.note_name = note_name
                notebook.add_record_notebook(note_record)

    except FileNotFoundError:
        pass

## VIEW All Contacts
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

@input_error
def show_all_notes(notebook):
    console = Console()

    if not notebook.data:
        console.print("No notes found.")
    else:
        # Create a table with appropriate columns
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Timestamp", justify="left")
        table.add_column("Note Name", justify="left")
        table.add_column("Note Text", justify="left")
        table.add_column("Tags", justify="left")
        

        # Populate the table with notes
        for timestamp, note_record in notebook.data.items():
            tags_str = ', '.join([str(tag) for tag in note_record.tags])
            table.add_row(
                str(note_record.timestamp.noteID),
                str(note_record.timestamp.ts),
                str(note_record.note_name),
                tags_str,
                str(note_record.note)
            )

        # Print the table to the console
        console.print(table)

## CONTACT
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

## PHONE NUMBER
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
    
## EMAIL
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

# Remove Email
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

## ADDRESS
    
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

# Edit address

@input_error
def edit_address_for_contact(args, address_book):
    if len(args) == 3:
        name, old_address, new_address = args
        record = address_book.find(name)
        if record:
            record.edit_address(old_address, new_address)
            return f"Address {old_address} for {name} edited to {new_address}."
        else:
            raise KeyError
    else:
        raise ValueError("Give me name, old address, and new address please.")

# Edit address
    
@input_error
def remove_address_from_contact(args, address_book):
    if len(args) == 2:
        name, address = args
        record = address_book.find(name)
        if record:
            record.remove_address(address)
            return f"Address {address} removed from {name}."
        else:
            raise KeyError 
    else:
        raise ValueError("Give me name and address to remove please.")


## HAPPY BD
    
#Додавання дня народження
    
@input_error
def add_birthday_to_contact(args, address_book):
    if len(args) == 2:
        name, birthday = args
        # Перевірка чи не знаходиться день народження в майбутньому
        if datetime.strptime(birthday, "%d.%m.%Y") > datetime.now():
            raise ValueError("New birthday cannot come from the future. Use realistic date.")
        else:   
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
        # Перевірка чи не знаходиться новий день народження в майбутньому
        if datetime.strptime(new_birthday, "%d.%m.%Y") > datetime.now():
            raise ValueError("New birthday cannot come from the future. Use realistic date.")
        else:
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

# Дні народження через задану кількість днів
def show_upcoming_birthdays_in_days(args, address_book):
    if len(args) == 1:
        days = int(args[0])
        birthdays_soon = defaultdict(list)
        current_date = datetime.now().date()
        future_date = current_date + timedelta(days)
        for record in address_book.data.values():
            if record.birthday and record.birthday.value:
                #birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").replace(year=current_date.year).date()
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()                
                if birthday_date.month == future_date.month and birthday_date.day == future_date.day:
                    # birthdays_soon[birthday_date.weekday()].append(record.name.value)
                    birthdays_soon[str(birthday_date)].append(record.name.value)

        print(f'\nUpcoming birthdays in the next {days} days:\n')

        for bd, names_to_list in sorted(birthdays_soon.items()):
            names_to_list_str = ', '.join(names_to_list)
            print(f'{bd}: {names_to_list_str}')

    else:
        raise ValueError("Give me the number of days starting from today in which you want to see the birthdays.")


## NOTES 
# processing user input funtions
@input_error
def add_record_notebook(args, notebook):
        # Запит ім'я нотатки
    note_name = input("Enter Note name: ")
    
    # Запит тексту нотатки
    note_text = input("Enter Note text: ")
    
    # Запит тегів
    tags_input = input("Enter tags (comma-separated, press Enter to skip): ")
    tags = [Tag(tag.strip()) for tag in tags_input.split(",") if tag.strip()]  # Розділити теги та видалити порожні

    note = Note(note_text)
    note_record = NoteRecord(note, note_name=note_name)
    note_record.tags = tags
    
    notebook.add_record_notebook(note_record)
    
    return f'Note with ID: {noteID} added to the notebook'
@input_error
def find_note_ID(args, notebook):
    # Запит ID нотатки
    note_ID = int(input("Enter Note ID: "))
    
    return notebook.find_ID(note_ID)
# Edit note
@input_error
def get_note_id_for_edit():
    return int(input("Give me note ID to edit, please: "))

# Edit note
@input_error
def edit_note(args, notebook):
    note_id = get_note_id_for_edit()
    note_record = notebook.find_ID(note_id)

    if note_record:
        # Display the note
        print(f"Editing Note ID {note_id}:")
        print(f"Name: {note_record.note_name}")
        print(f"Text: {note_record.note}")
        print(f"Tags: {', '.join(map(str, note_record.tags))}")

        # Ask for changes
        new_name = input("Enter new name (press Enter to skip): ")
        new_text = input("Enter new text (press Enter to skip): ")
        new_tags_input = input("Enter new tags (comma-separated, press Enter to skip): ")
        new_tags = [Tag(tag.strip()) for tag in new_tags_input.split(",") if tag.strip()]

        # Update the note if changes are provided
        if new_name:
            note_record.note_name = new_name
        if new_text:
            note_record.note = new_text
        if new_tags:
            note_record.tags = new_tags

        return f"Note ID {note_id} edited successfully."
    else:
        raise ValueError(f"No note found with ID {note_id}.")
    
@input_error
def note_delete(args, notebook):
    # Запит ID нотатки
    note_ID = int(input("Enter Note ID: "))
    print(f'Note deleted:\n {notebook.delete(note_ID)}')

@input_error
def find_note_date(args, notebook):
    # Запит ітервалу дат створення нотаток
    start = input("Enter start date: ")
    end = input("Enter end date: ")
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    print(f'Notes created from {start_date} to {end_date}:\n')
    for note in notebook.find_date_slot(start_date, end_date):
        print(note)
        
@input_error
def find_note_name(args, notebook):
    # Запит назви нотатоки
    search_name = input("Enter searched name: ")
    print(f'Notes with name {search_name}:\n')
    for note in notebook.find_name(search_name):
        print(note)

## DATABASE
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

## Baby youda
def get_valid_commands():
    address_book = AddressBook()
    commands = [
        "close", "exit", "hello", "help", 
        "add", "del",
        "all", "find",
        "add-phone", "remove-phone", "edit-phone", "find-phone",
        "add-birthday", "edit-birthday", "show-birthday", "birthdays",
        "add-email","remove-email", "edit-email", 
        "add-address", "edit-address" ,"remove-address",
        "add-note", "all-notes", "edit-note", "find-note-ID","find-note-name", "find-note-date", "note-del"
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
            tags_str = ', '.join(map(str, noterecord.tags)) if noterecord.tags else ""
            file.write(f"{noterecord.timestamp.ts}_{noterecord.timestamp.noteID}_{tags_str}_{noterecord.note}_{noterecord.note_name}\n")

## POPUP
# Меню Help

# Mune styles
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
        "Birthday": ["add-birthday - add birthday to an existing contact", "edit-birthday - edit birthday of an existing contact", "show-birthday - show birthday of a contact", 'show-birthdays-in-days - show contacts with birthdays in a number of days specified', "birthdays - show upcoming birthdays"],
        "Address": ["add-address - add address for an existing contact","edit-address - edit address for an existing contact","remove-address - remove address for an existing contact" ],
        "Notes": ["add-note - adding note", "edit-note - editing note", "find-note-ID - find note by given ID", "find-note-name - find notes for a given name", "find-note-date - find notes for a given date slot (format of input: start date 2023-12-21 end date 2023-12-22)", "all-notes - display all notes", "note-del - delete note for a given note ID"],
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
    noteID = notebook.get_maxID
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
        elif command == "show-birthdays-in-days":
            print(show_upcoming_birthdays_in_days(args, address_book))
        elif command == "add-email":                                # EMAIL
            print(add_email_to_contact(args, address_book))
        elif command == "remove-email":
            print(remove_email_from_contact(args, address_book))
        elif command == "edit-email":
            print(edit_email_for_contact(args, address_book))
        elif command == "add-address":                              # Address
            print(add_address_to_contact(args, address_book))
        elif command == "edit-address":
            print(edit_address_for_contact(args, address_book))
        elif command == "remove-address":
            print(remove_address_from_contact(args, address_book))
        elif command == 'help':
            display_help()
        elif command == "add-note":                           # NOTES 
            print(add_record_notebook(args, notebook))
        elif command == "all-notes":                         
            show_all_notes(notebook)                          
        elif command == "find-note-id":                         
            print(find_note_ID(args, notebook))                  
        elif command == "edit-note":
            print(edit_note(args, notebook))
        elif command == "note-del":                           
            note_delete(args, notebook)
        elif command == "find-note-date":                           
            find_note_date(args, notebook)
        elif command == "find-note-name":                           
            find_note_name(args, notebook)                 
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()



