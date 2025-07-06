import csv
import os

def read_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(file_path, new_row, fieldnames):
    file_exists = os.path.exists(file_path)
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)
