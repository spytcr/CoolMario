import csv
from properties import saves_path


def save_data(data):
    with open(saves_path, 'w', newline='', encoding='utf8') as f:
        writer = csv.DictWriter(f, fieldnames=list(data.keys()), delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerow(data)


def load_data():
    with open(saves_path, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f, delimiter=';', quotechar='"')
        data = {k: int(v) for k, v in next(reader).items()}
        return data
