import requests
import chardet

areas = dict()

# Определим кодировку файла (если не уверены, что utf-8)
with open("ScienceList_rus.txt", "rb") as file:
    raw_data = file.read()
    encoding = chardet.detect(raw_data)['encoding']

# Открытие с корректной кодировкой
with open("ScienceList_rus.txt", "r", encoding=encoding) as file:
    for line in file:
        if ":" not in line:
            continue  # Пропустить строки без ":"
        first, second = line.split(":", 1)
        first, second = first.strip(), second.strip()
        areas.setdefault(first, []).append(second)

url = "http://localhost:8000/article-service/area/create"

for first, seconds in areas.items():
    res1 = requests.post(url, json={
        "name": first,
        "layer": "first",
    })
    print(f"Posted: {first} (status: {res1.status_code})")

    for second in seconds:
        res2 = requests.post(url, json={
            "name": second,
            "layer": "second",
        })
        print(f"  └─ Posted: {second} (status: {res2.status_code})")
