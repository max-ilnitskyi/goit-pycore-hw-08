from collections import UserDict
from datetime import datetime, timedelta, date


class ValidationError(ValueError):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if value.isdecimal() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValidationError("Wrong phone")


BIRTHDAY_FORMAT = "%d.%m.%Y"


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, BIRTHDAY_FORMAT)
            super().__init__(value)
        except ValueError:
            raise ValidationError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, record_phone):
        self.phones = [phone for phone in self.phones if phone.value != record_phone]

    def edit_phone(self, old_record_phone, new_record_phone):
        if not old_record_phone in [phone.value for phone in self.phones]:
            raise KeyError
        self.phones = [
            Phone(new_record_phone) if phone.value == old_record_phone else phone
            for phone in self.phones
        ]

    def find_phone(self, record_phone):
        for phone in self.phones:
            if phone.value == record_phone:
                return phone

        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, record_name):
        return self.data[record_name]

    def delete(self, record_name):
        del self.data[record_name]

    def get_upcoming_birthdays(self):
        current_date = date.today()
        users_to_congratulate = {}

        for record in self.data.values():
            birthday = record.birthday

            if not birthday:
                continue

            birthday_date = datetime.strptime(birthday.value, BIRTHDAY_FORMAT).date()
            birthday_this_year = date(
                current_date.year, birthday_date.month, birthday_date.day
            )
            birthday_next_year = date(
                current_date.year + 1, birthday_date.month, birthday_date.day
            )

            next_birthday = (
                birthday_next_year
                if birthday_this_year < current_date
                else birthday_this_year
            )

            days_to_birthday = (next_birthday - current_date).days

            if days_to_birthday > 7:
                continue

            days_from_birthday_to_congratulation_date = (
                0 if next_birthday.weekday() < 5 else (6 - next_birthday.weekday()) + 1
            )

            congratulation_date = (
                next_birthday
                + timedelta(days=days_from_birthday_to_congratulation_date)
                if days_from_birthday_to_congratulation_date
                else next_birthday
            )

            congratulation_date_str = congratulation_date.strftime(BIRTHDAY_FORMAT)

            same_congratulation_date_users = users_to_congratulate.get(
                congratulation_date_str
            )

            if same_congratulation_date_users:
                same_congratulation_date_users.append(record)
            else:
                users_to_congratulate[congratulation_date_str] = [record]

        return users_to_congratulate
