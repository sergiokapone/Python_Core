import re

# ================================= Decorator ================================#


def input_error(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"<{args[0]}> does not appear in list"
        except ValueError:
            return "Give me a name and phone, please"

    return wrapper


# ================================== handlers ================================#


def hello(*args):
    return "How can I help you?"


def good_bye(*args):
    return "Good bye!"


def undefined(*args):
    return "What do you mean?"


def show_all(*args):
    return "show all"


@input_error
def get_phone(*args):
    return contacts[args[0]]


@input_error
def add_contact(*args):
    if args[0] and args[1]:
        if not contacts.get(args[0]):
            contacts[args[0]] = args[1]
            return f"I add contact for <{args[0]}> with phone <{args[1]}>"
        return f"Contact <{args[0]}> already in list."
    else:
        raise ValueError


@input_error
def change_contact(*args):
    if args[0] and args[1]:
        if contacts.get(args[0]):
            contacts[args[0]] = args[1]
            return f"I changed contact for <{args[0]}> to value <{args[1]}>"
        return f"Contact <{args[0]}> does not exist."
    else:
        raise ValueError


# =============================== handler loader =============================#


def get_handler(*args):
    COMMANDS = {
        "hello": hello,
        "add": add_contact,
        "change": change_contact,
        "phone": get_phone,
        "show all": show_all,
        "good bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
    }
    return COMMANDS.get(args[0], undefined)


# ================================ main function =============================#


def main():

    pattern = re.compile(
        r"\b(\.|hello|add|change|phone|show all|good bye|close|exit)\b(?:\s+([a-zA-Z]+))?\b(?:\s+(\d{10}$))?",
        re.IGNORECASE,
    )

    while True:

        # waiting for nonempty input
        while True:
            inp = input(">>> ").strip()
            if inp == "":
                continue
            break

        text = pattern.search(inp)

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
        handler = get_handler(*params)
        response = handler(*params[1:])
        if inp.strip() == ".":
            return
        if response == "show all":
            for k, v in contacts.items():
                print(f"{k}: {v}")
            response = f"--------------------\nList contain <{len(contacts)}> contact(s)"
        print(response)
        if response == "Good bye!":
            return


contacts = {}  # Global variable for storing contacts


# ================================ main programm =============================#

if __name__ == "__main__":

    main()
