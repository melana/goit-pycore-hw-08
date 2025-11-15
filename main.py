from book import AddressBook, Record, Phone
from datetime import datetime, timedelta, date
from storage import load_data, save_data

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct arguments please."
        except KeyError:
            return "Key does not exist, try again please."
        except IndexError:
            return "Index is out of range try again please."
        except Exception as e: # обробляє всі інші exeptions
            return (f"Error: {e}")

    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    phone_number = Phone(phone).value # для додаткової валідаціїфвв 
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone_number)
    return message

@input_error
def change_contact(args, book: AddressBook): # функція, яка обробляє команду change
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book: AddressBook): # функція, яка обробляє команду phone
    (name,) = args
    record = book.find(name)
    return ", ".join([phone.value for phone in record.phones])

@input_error
def show_all(book: AddressBook): # функція, яка обробляє команду all
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book: AddressBook): # функція, яка обробляє команду add-birthday
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added to contact."

@input_error
def show_birthday(args, book: AddressBook):# функція, яка обробляє команду show-birthday
    (name,) = args
    record = book.find(name)
    birthday = record.birthday
    if birthday:
        return birthday.value
    else:
        return "Unknown birthday."


@input_error
def birthdays(book: AddressBook): # функція, яка обробляє команду birthdays
    birthdays_list = book.get_upcoming_birthdays()
    if not birthdays_list:
        return "No upcoming birthdays"

    response = ""
    for item in birthdays_list:
        response += (
            f"Congratulation date {item['congratulation_date']}: "
            f"{item['name']}\n"
        )
    return response.strip()

def main():
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]: # обробляє команди close, exit
            print("Good bye!")
            break
        elif command == "hello": # обробляє команду hello
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

    save_data(book)       


if __name__ == "__main__":
    main()
