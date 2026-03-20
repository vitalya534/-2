import json
import os

DATA_FILE = "books.json"


def load_books():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def add_book(books):
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    year = input("Год издания: ").strip()
    genre = input("Жанр: ").strip()
    description = input("Краткое описание: ").strip()
    books.append({
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "description": description,
        "read": False,
        "favorite": False
    })
    save_books(books)
    print(f'Книга "{title}" добавлена.')


def list_books(books):
    if not books:
        print("Библиотека пуста.")
        return
    print("\nСортировка: 1-по названию  2-по автору  3-по году  (Enter-без сортировки)")
    sort_choice = input("> ").strip()
    sort_map = {"1": "title", "2": "author", "3": "year"}
    sorted_books = sorted(books, key=lambda b: b[sort_map[sort_choice]]) if sort_choice in sort_map else books

    print("\nФильтр по жанру (Enter-все): ", end="")
    genre_filter = input().strip().lower()
    print("Фильтр по статусу: 1-прочитана  2-не прочитана  (Enter-все): ", end="")
    status_filter = input().strip()

    result = []
    for b in sorted_books:
        if genre_filter and b["genre"].lower() != genre_filter:
            continue
        if status_filter == "1" and not b["read"]:
            continue
        if status_filter == "2" and b["read"]:
            continue
        result.append(b)

    if not result:
        print("Книги не найдены.")
        return
    _print_books(result, books)


def _print_books(result, books):
    for b in result:
        idx = books.index(b) + 1
        status = "✓ прочитана" if b["read"] else "○ не прочитана"
        fav = " ★" if b["favorite"] else ""
        print(f'[{idx}] "{b["title"]}" — {b["author"]}, {b["year"]}, {b["genre"]}{fav} [{status}]')


def toggle_favorite(books):
    _print_books(books, books)
    try:
        idx = int(input("Номер книги: ")) - 1
        books[idx]["favorite"] = not books[idx]["favorite"]
        state = "добавлена в избранное" if books[idx]["favorite"] else "удалена из избранного"
        save_books(books)
        print(f'Книга "{books[idx]["title"]}" {state}.')
    except (ValueError, IndexError):
        print("Неверный номер.")


def change_status(books):
    _print_books(books, books)
    try:
        idx = int(input("Номер книги: ")) - 1
        books[idx]["read"] = not books[idx]["read"]
        state = "прочитана" if books[idx]["read"] else "не прочитана"
        save_books(books)
        print(f'Статус книги "{books[idx]["title"]}" изменён на "{state}".')
    except (ValueError, IndexError):
        print("Неверный номер.")


def show_favorites(books):
    favs = [b for b in books if b["favorite"]]
    if not favs:
        print("Избранных книг нет.")
    else:
        _print_books(favs, books)


def delete_book(books):
    _print_books(books, books)
    try:
        idx = int(input("Номер книги для удаления: ")) - 1
        removed = books.pop(idx)
        save_books(books)
        print(f'Книга "{removed["title"]}" удалена.')
    except (ValueError, IndexError):
        print("Неверный номер.")


def search_books(books):
    query = input("Поисковый запрос: ").strip().lower()
    result = [b for b in books if
              query in b["title"].lower() or
              query in b["author"].lower() or
              query in b["description"].lower()]
    if not result:
        print("Ничего не найдено.")
    else:
        _print_books(result, books)


def recommendations(books):
    read = [b for b in books if b["read"]]
    if not read:
        print("Нет прочитанных книг для рекомендаций.")
        return
    genres = {}
    for b in read:
        genres[b["genre"]] = genres.get(b["genre"], 0) + 1
    top_genre = max(genres, key=genres.get)
    recs = [b for b in books if b["genre"] == top_genre and not b["read"]]
    if not recs:
        print(f'Все книги жанра "{top_genre}" уже прочитаны.')
    else:
        print(f'Рекомендации на основе жанра "{top_genre}":')
        _print_books(recs, books)


MENU = """
=== Т-Библиотека ===
1. Добавить книгу
2. Просмотр книг
3. Добавить/убрать из избранного
4. Изменить статус книги
5. Избранные книги
6. Удалить книгу
7. Поиск книги
8. Рекомендации
0. Выход
"""


def main():
    books = load_books()
    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        actions = {
            "1": lambda: add_book(books),
            "2": lambda: list_books(books),
            "3": lambda: toggle_favorite(books),
            "4": lambda: change_status(books),
            "5": lambda: show_favorites(books),
            "6": lambda: delete_book(books),
            "7": lambda: search_books(books),
            "8": lambda: recommendations(books),
        }
        if choice == "0":
            print("До свидания!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()
