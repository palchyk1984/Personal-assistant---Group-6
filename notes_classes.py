from datetime import datetime

# Classes
class Field:                        # reused
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):                  # reused
    pass

class Tag(Field):                   # new - from Phone
    def __init__(self, value):
        if not value.isdigit() or len(value) > 10:
            raise ValueError("Tag should be max 10 digits")
        super().__init__(value)

class Timestamp():                  # new
    def __init__(self):
        self.ts = datetime.now()

    def __str__(self):
        return str(self.ts)

class Note(Field):                   # new
    def __init__(self, value):
        if len(value) > 255:
            raise ValueError("Note should be max 255 digits")
        super().__init__(value)

class NoteRecord:
    def __init__(self, note: Note):
        self.timestamp = Timestamp()
        self.tags = []
        self.note = note

    def __str__(self):
            return f"Note from: {self.timestamp}\n Text: {self.note}\n Tags: {self.tags}\n"
    
'''    
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
'''
    


class NoteBook:
    def __init__(self):
        self.data = {}

    def add_record(self, note_record):
        self.data[note_record.timestamp.ts] = note_record

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


first_notebook = NoteBook()

firts_note = Note('That was a difficult day')

first_note_record = NoteRecord(firts_note)

first_notebook.add_record(first_note_record)

first_notebook.show_all_notes()

second_note = Note('But tomorrow will be more difficult day')

second_note_record = NoteRecord(second_note)

first_notebook.add_record(second_note_record)

first_notebook.show_all_notes()

