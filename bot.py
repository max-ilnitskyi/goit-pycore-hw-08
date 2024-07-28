from book import AddressBook, Record, ValidationError


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return str(e)
        except ValueError:
            return "Enter the argument for the command"
        except KeyError:
            return "Not found"
        except IndexError:
            return "List index out of range"

    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    try:
        existing_record = book.find(name)
        existing_record.add_phone(phone)
        return "Phone added to contact."
    except Exception:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phones(args, book: AddressBook):
    (name,) = args
    record = book.find(name)
    return ", ".join([phone.value for phone in record.phones])


@input_error
def show_all(book: AddressBook):
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added to contact."


@input_error
def show_birthday(args, book: AddressBook):
    (name,) = args
    record = book.find(name)
    birthday = record.birthday
    if birthday:
        return birthday.value
    else:
        return "Unknown birthday."


@input_error
def show_birthdays(book: AddressBook):
    birthdays = book.get_upcoming_birthdays()
    response = ""
    for date, records in birthdays.items():
        response += (response and "\n") + "Congratulation date " + date + ":"
        for record in records:
            response += (
                "\n" + record.name.value + f"(actual date {record.birthday.value})"
            )

    return response or "No upcoming birthdays"


@input_error
def parse_input(raw_input: str):
    cmd, *args = raw_input.strip().split()
    cmd = cmd.strip().casefold()
    return cmd, *args


EXIT_COMMANDS = {"exit", "close"}


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command == "hello":
            print("How can I help you?")
            continue

        if command == "add":
            print(add_contact(args, book))
            continue

        if command == "change":
            print(change_contact(args, book))
            continue

        if command == "phone":
            print(show_phones(args, book))
            continue

        if command == "all":
            print(show_all(book))
            continue

        if command == "add-birthday":
            print(add_birthday(args, book))
            continue

        if command == "show-birthday":
            print(show_birthday(args, book))
            continue

        if command == "birthdays":
            print(show_birthdays(book))
            continue

        if command in EXIT_COMMANDS:
            print("Good bye!")
            break

        print("Invalid command.")


if __name__ == "__main__":
    main()
