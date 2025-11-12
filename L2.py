import csv
import xml.etree.ElementTree as ET
from collections import Counter

# Пути к файлам
CSV_FILE = "../books-en.csv"   
XML_FILE = "../currency.xml"
RESULT_FILE = "result.txt"


# === 1. Разбор XML: извлекаем CharCode и Value ===
def parse_currency_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    char_codes = [elem.text for elem in root.iter("CharCode")]
    values = [elem.text for elem in root.iter("Value")]
    return char_codes, values


# === 2. Подсчёт книг с названием длиннее 30 символов ===
def titles_longer_than_30():
    count = 0
    with open(CSV_FILE, 'r', encoding='windows-1251') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if len(row['Book-Title']) > 30:
                count += 1
    return count


# === 3. Поиск книг по автору ===
def find_books_by_author(author):
    found_books = []
    with open(CSV_FILE, 'r', encoding='windows-1251') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Book-Author'].lower() == author.lower():
                found_books.append(row)
    return found_books


# === 4. Генератор библиографических ссылок ===
def generate_bibliography(n=20):
    bibliography = []
    with open(CSV_FILE, 'r', encoding='windows-1251') as f:
        reader = csv.DictReader(f, delimiter=';')
        for i, row in enumerate(reader):
            if i >= n:
                break
            bibliography.append(f"{row['Book-Author']}. {row['Book-Title']} - {row['Year-Of-Publication']}")
    # сохраняем в файл
    with open(RESULT_FILE, 'w', encoding='utf-8') as out:
        for i, ref in enumerate(bibliography, 1):
            out.write(f"{i}. {ref}\n")
    return bibliography


# === 5. Список всех издательств без повторений ===
def list_publishers():
    publishers = set()
    with open(CSV_FILE, 'r', encoding='windows-1251') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            publishers.add(row['Publisher'])
    return sorted(publishers)


# === 6. ТОП-20 самых популярных книг ===
def top_20_books():
    titles = []
    with open(CSV_FILE, 'r', encoding='windows-1251') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            titles.append(row['Book-Title'])
    top_books = Counter(titles).most_common(20)
    return top_books


# === Основная программа ===
if __name__ == "__main__":
    # 1. Парсим XML
    char_codes, values = parse_currency_xml(XML_FILE)
    print(f"CharCodes: {char_codes}")
    print(f"Values: {values}")

    # 2. Подсчёт длинных названий
    long_titles_count = titles_longer_than_30()
    print(f"\nКоличество книг с названием > 30 символов: {long_titles_count}")

    # 3. Поиск книг по автору
    author = input("\nВведите автора: ")
    books = find_books_by_author(author)
    if books:
        print(f"\nКниги автора {author}:")
        for book in books:
            print(f"- {book['Book-Title']} ({book['Year-Of-Publication']})")
    else:
        print(f"\nКниги автора {author} не найдены.")

    # 4. Генерация библиографических ссылок
    bib = generate_bibliography()
    print(f"\nСписок из 20 библиографических ссылок сохранён в {RESULT_FILE}")

    # 5. Уникальные издательства
    publishers = list_publishers()
    print(f"\nКоличество уникальных издательств: {len(publishers)}")

    # 6. ТОП-20 популярных книг
    print("\nТОП-20 популярных книг:")
    for i, (title, count) in enumerate(top_20_books(), 1):
        print(f"{i}. {title} — встречается {count} раз")
