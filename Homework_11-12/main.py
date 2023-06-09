import re
from pathlib import Path
from prettytable import PrettyTable
from botmodule import Name, Phone, Birthday, Record, AddressBook

# ============================ Tables decoration =============================#


def build_table(data):
    """Функція будує PrettyTable для заданного списка записів."""

    table = PrettyTable()
    table.field_names = ["Name", "Birthday", "Phones"]
    table.min_width.update({"Name": 20, "Birthday": 12, "Phones": 40})
    data = AddressBook(data)
    for key in data:
        record = data[key]
        name = record.name.value
        birthday = record.show_birthday()
        phones = record.show_phones()
        table.add_row([name, birthday, phones])
    return table


# ================================= Decorator ================================#


def input_error(func):
    def wrapper(*func_args, **func_kwargs):
        try:
            return func(*func_args, **func_kwargs)
        except KeyError as error:
            return "\033[1;31m{}\033[0m".format(str(error).strip("'"))
        except ValueError as error:
            return f"\033[1;31m{str(error)}\033[0m"
        except TypeError as error:
            return f"\033[1;31m{str(error)}\033[0m"
        except FileNotFoundError:
            return "\033[1;31mFile not found\033[0m"

    return wrapper


# ================================== handlers ================================#


def hello(*args):
    return "\033[32mHow can I help you?\033[0m"


def good_bye(*args):
    contacts.save_contacts("contacts")
    return "Good bye!"


def undefined(*args):
    return "\033[32mWhat do you mean?\033[0m"


@input_error
def save(*args):
    contacts.save_contacts(args[0])
    return f"File {args[0]} saved"


@input_error
def load(*args):
    file_path = Path(args[0])
    if file_path.exists():
        contacts.load_contacts(args[0])
        return f"File {args[0]} loaded"
    else:
        raise FileNotFoundError


@input_error
def set_birthday(*args):
    """Функція-handler додає день народження до контакту."""

    if not args[0] or args[0].isdigit():
        raise KeyError("Give me a name, please")
    if not args[1]:
        raise ValueError("Give me a date, please")

    name, birthday = Name(args[0]), Birthday(args[1])

    if name.value in contacts.data:
        record = contacts.data[name.value]
    else:
        record = Record(name)
        contacts.add_record(record)
    record.add_birthday(birthday)

    return f"I added a birthday {args[1]} to contact {args[0]}"


@input_error
def add(*args):
    """Добавляет телефонный номер в контакт по имени."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    if not args[1]:
        raise ValueError("Give me a phone, please")

    name, phone = Name(args[0]), Phone(args[1])

    if name.value in contacts.data:
        record = contacts.data[name.value]
    else:
        record = Record(name)
        contacts.add_record(record)
    record.add_phone(phone)

    return f"I added a phone {args[1]} to contact {args[0]}"


@input_error
def phones(*args):
    """Функція-handler показує телефонні номери відповідного контакту."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    if args[0] not in contacts.keys():
        raise ValueError("Contact does not in AddressBook")

    table = PrettyTable()
    table.field_names = ["Name", "Phones"]
    table.min_width.update({"Name": 20, "Phones": 55})

    phones = contacts.get(args[0]).show_phones() or "-"
    table.add_row([args[0], phones])

    return f"\033[0m{table}"


@input_error
def birthday(*args):
    """Функція-handler показує день народження та кількість днів до наступного."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    table = PrettyTable()
    table.field_names = ["Name", "Birthday", "Days to next Birthday"]
    table.min_width.update({"Name": 20, "Birthday": 12, "Days to next Birthday": 40})

    if args[0] not in contacts.keys():
        raise ValueError("Contact does not in AddressBook")

    days_to_next_birthday = contacts.data[args[0]].days_to_birthday() or "-"
    birthday = contacts.get(args[0]).show_birthday() or "-"

    table.add_row([args[0], birthday, days_to_next_birthday])

    return f"\033[0m{table}"


@input_error
def search(*args):

    if not args[0]:
        raise KeyError("Give me a some string, please")

    results = contacts.search(args[0])

    if results:
        return f"\033[0m{build_table(results)}"
    return "By your request found nothing"


@input_error
def remove(*args):
    """Функція-handler видаляє запис з книги."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    name = Name(args[0])

    del contacts[name.value]

    return f"Contact {name.value} was removed"


@input_error
def change(*args):
    """Функція-handler змінює телефон контакту."""

    if not args[0]:
        raise KeyError("Give me a name, please")

    if not args[1]:
        raise ValueError("Old phone number is required")

    if not args[2]:
        raise ValueError("New phone number is required")

    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])

    if name.value not in contacts:
        return f"Contact {name.value} not found"

    contact_list = contacts[name.value].phones
    for number in contact_list:
        if number == old_phone:
            idx = contact_list.index(number)
            contact_list[idx] = new_phone
            break
        return f"Phone {old_phone.value} not found for {name.value}"

    return f"Contact {name.value} with phone number {old_phone.value} was updated with new phone number {new_phone.value}"


@input_error
def export_to_csv(*args):
    if not args[0]:
        raise TypeError("Set file name, please")
    contacts.export_to_csv(args[0])
    return f"File {args[0]} exported to csv"


@input_error
def import_from_csv(*args):
    contacts.import_from_csv(args[0])
    return f"File {args[0]} imported from csv"


def show_all(*args):
    """Функция-handler показує книгу контактів."""

    number_of_entries = (
        int(args[0])
        if args[0] is not None and isinstance(args[0], str) and args[0].isdigit()
        else 100
    )
    for tab in contacts.iterator(number_of_entries):
        if tab == "continue":
            input("\033[1;32mPress <Enter> to continue...\033[0m")
        else:
            print(build_table(tab))

    return f"Address book contain {len(contacts)} contacts"


def help_commands(*args):
    """Функція показує перелік всіх команд."""

    table = PrettyTable()
    table.field_names = ["Command"]
    table.min_width.update({"Command": 20})

    for command in COMMANDS:
        table.add_row([command])

    return f"\nPlease type followed commands:\n\033[0m{table}"


def week_birthdays(*args):

    table = PrettyTable()
    table.field_names = ["Weekday", "Peoples"]
    table.min_width.update({"Weekday": 20, "Peoples": 55})
    birthdays = contacts.get_birthdays_per_week()

    for weekday, names in birthdays.items():
        table.add_row([weekday, ", ".join(names)])

    return f"\033[0m{table}"


# =============================== handler loader =============================#

COMMANDS = {
    "help": help_commands,
    "hello": hello,
    "set birthday": set_birthday,
    "birthday of": birthday,
    "add": add,
    "change": change,
    "phones of": phones,
    "show all": show_all,
    "remove": remove,
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    "save": save,
    "load": load,
    "search": search,
    "export": export_to_csv,
    "import": import_from_csv,
    "near birthdays": week_birthdays,
}

command_pattern = "|".join(COMMANDS.keys())
pattern = re.compile(
    r"\b(\.|" + command_pattern + r")\b"
    r"(?:\s+([a-zA-Z0-9\.]+))?"
    r"(?:\s+(\d{1,2}\.\d{1,2}\.\d{4}|\d{1,})?)?"
    r"(?:\s+(\d+)?)?",
    re.IGNORECASE,
)


def get_handler(*args):
    """Функція викликає відповідний handler."""

    return COMMANDS.get(args[0], undefined)


contacts = AddressBook()  # Global variable for storing contacts


def wait_for_input(prompt):
    while True:
        inp = input(prompt).strip()
        if inp == "":
            continue
        break
    return inp


def parse_command(command):
    text = pattern.search(command)

    params = (
        tuple(
            map(
                # Made a commands to be a uppercase
                lambda x: x.lower() if text.groups().index(x) == 0 else x,
                text.groups(),
            )
        )
        if text
        else (None, 0, 0)
    )

    return params


# ================================ main function ============================ #


def main():
    print("\033[1;32mHello, I'm an assistant. Type help if you need.\033[0m")
    load("contacts")
    while True:
        command = wait_for_input(">>> ")

        if command.strip() == ".":
            contacts.save_contacts("contacts")
            return
        params = parse_command(command)
        handler = get_handler(*params)
        response = handler(*params[1:])
        print(f"\033[1;32m{response}\033[0m")
        if response == "Good bye!":
            return


# ================================ main program ============================= #

if __name__ == "__main__":

    main()
