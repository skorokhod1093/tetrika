import requests
from bs4 import BeautifulSoup
import csv
import time

class BeastsParserError(Exception):
    """Исключение для ошибок парсера животных."""
    pass

class BeastsParser:
    WIKI_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"

    def __init__(self, delay: float = 0.5) -> None:
        self.delay = delay

    def get_animals_count_by_letter(self) -> dict[str, int]:
        result: dict[str, int] = {}
        session = requests.Session()
        url = self.WIKI_URL
        try:
            while url:
                resp = session.get(url)
                if resp.status_code != 200:
                    raise BeastsParserError(f"Ошибка запроса: {resp.status_code}")
                soup = BeautifulSoup(resp.text, "html.parser")
                for div in soup.find_all("div", class_="mw-category-group"):
                    letter = div.find("h3")
                    if letter:
                        letter_text = letter.text.strip().upper()
                        count = len(div.find_all("li"))
                        result[letter_text] = result.get(letter_text, 0) + count
                next_link = soup.find("a", string="Следующая страница")
                if next_link:
                    url = "https://ru.wikipedia.org" + next_link["href"]
                    time.sleep(self.delay)
                else:
                    url = None
        except Exception as e:
            raise BeastsParserError(f"Ошибка парсинга: {e}")
        return result

    def save_to_csv(self, data: dict[str, int], filename: str = "beasts.csv") -> None:
        try:
            with open(filename, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                for letter, count in sorted(data.items()):
                    writer.writerow([letter, count])
        except Exception as e:
            raise BeastsParserError(f"Ошибка записи в CSV: {e}")

# Пример использования
if __name__ == "__main__":
    parser = BeastsParser()
    data = parser.get_animals_count_by_letter()
    parser.save_to_csv(data) 