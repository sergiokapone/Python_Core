import csv
from datetime import datetime, timedelta

###############################################################################
#   Зчитуванні інформації про дати народження з csv-файлу та формування       #
#          на його основі списка словників users                              #
###############################################################################


filename = "birthdays.csv"

users = []

with open(filename, "r") as data:
    for line in csv.DictReader(data, delimiter=";"):
        line["Born"] = datetime.strptime(line["Born"], "%d.%m.%Y").date()
        users.append(line)

###############################################################################
#                            Реалізація функції                               #
###############################################################################


def get_birthdays_per_week(users):
    """Функція виводить сSписок колег, яких потрібно привітати з днем народження на тижні."""

    # Всі дні народження будуть виводитись,
    # починаючи з цього дня і далі до п'ятниці включно.
    # Якщо сьогодні субота, або неділя,
    # то забираємо ці дні і далі до п'ятниці включно.

    # today = datetime.today().date()
    today = datetime.strptime('11/02/2023', '%d/%m/%Y').date()

    def filtering(user):
        if today.weekday() == 5:
            return (
                0 <= (user["Born"].replace(year=today.year) - today).days <= 6
            )
        elif today.weekday() == 6:
            return -1 <= (
                 user["Born"].replace(year=today.year) - today
            ).days <= 5
        return (
            0
            <= (user["Born"].replace(year=today.year) - today).days
            <= 4 - today.weekday()
        )

    user_birthdays = map(
        lambda user: (
            user["Born"].replace(year=today.year),
            user["Name"],
        ),
        filter(filtering, users),
    )

    d = {}
    for k, v in user_birthdays:
        if k.strftime('%A') == "Saturday":
            k += timedelta(days=2)
        elif k.strftime('%A') == "Sunday":
            k += timedelta(days=1)
        d.setdefault(k, []).append(v)

    d = sorted(d.items())

    for k, v in d:
        print(k.strftime('%A'), end=": ")
        print(*v, sep=", ")


def get_next_saturday():
    current_time = datetime.now()
    next_saturday = (
        current_time.date()
        - timedelta(days=current_time.weekday())
        + timedelta(days=5, weeks=0)
    )
    return next_saturday


###############################################################################
#                            Головна програма                                 #
###############################################################################


if __name__ == "__main__":

    get_birthdays_per_week(users)
