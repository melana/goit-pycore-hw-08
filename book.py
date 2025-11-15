from collections import UserDict
from datetime import datetime, timedelta, date

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
		pass


class Phone(Field):
    def __init__(self, value):
        if value.isdigit() and len(value) == 10: # перевірка коректності номера телефону
            super().__init__(value)
        else:
            raise ValueError("Номер має містити 10 цифр")


BIRTHDAY_FORMAT = "%d.%m.%Y" # формат дати для Дня народження


class Birthday(Field):
    def __init__(self, value):
        try: 
            datetime.strptime(value, BIRTHDAY_FORMAT)
            super().__init__(value)
        except ValueError: 
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone)) # додає новий номер телефону

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone] #видаляє телефон за значенням

    def edit_phone(self, old_phone, new_phone):
        try:
            for phone in self.phones: # редагує існуючий телефон
                if phone.value == old_phone:
                    phone.value = new_phone
        except Exception as e:
            pass

    def find_phone(self, phone_number):
        try:
            for phone in self.phones: # пошук об’єкта Phone за значенням
                if phone.value == phone_number:
                    return phone
            return None
        except Exception as e:
            print(f"Error: {e}")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
      
    def find(self, name):
        return self.data.get(name)
        
    def delete(self, name):
        del self.data[name]
        
    def get_upcoming_birthdays(self): 
        today = datetime.today().date()
        upcoming_birthdays = []
        for user in self.data.values():
            if user.birthday is None:
                continue
            user_birthday = datetime.strptime(user.birthday.value, "%d.%m.%Y")#
            birthday_this_year = user_birthday.replace(year = today.year).date()
            if birthday_this_year < today:# перевіряємо, чи вже минув день народження в цьому році
                continue
            elif (birthday_this_year - today).days <=6:
                if birthday_this_year.weekday() == 5:# якщо день народження в суботу
                    congratulation_date = birthday_this_year + timedelta(days=2)
                elif birthday_this_year.weekday() == 6:# якщо день народження в неділю
                    congratulation_date = birthday_this_year + timedelta(days=1)
                else:
                    congratulation_date = birthday_this_year

                upcoming_birthdays.append({"name": (user.name.value), "congratulation_date": datetime.strftime(congratulation_date, "%d.%m.%Y")})
        return upcoming_birthdays