import pytest
from solution import BeastsParser, BeastsParserError

class DummyResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code

@pytest.fixture
def html_page() -> str:
    # Минимальный HTML с двумя буквами
    return '''<div class="mw-category-group"><h3>А</h3><ul><li>Антилопа</li><li>Акула</li></ul></div>
    <div class="mw-category-group"><h3>Б</h3><ul><li>Бобр</li></ul></div>'''

@pytest.fixture
def monkeypatch_requests(monkeypatch, html_page):
    class DummySession:
        def __init__(self):
            self.calls = 0
        def get(self, url):
            self.calls += 1
            if self.calls == 1:
                return DummyResponse(html_page)
            return DummyResponse('', 200)
    monkeypatch.setattr("requests.Session", DummySession)


def test_get_animals_count_by_letter(monkeypatch_requests):
    parser = BeastsParser()
    data = parser.get_animals_count_by_letter()
    assert data == {"А": 2, "Б": 1}


def test_save_to_csv(tmp_path):
    parser = BeastsParser()
    data = {"А": 2, "Б": 1}
    file_path = tmp_path / "beasts.csv"
    parser.save_to_csv(data, str(file_path))
    content = file_path.read_text(encoding="utf-8")
    assert "А,2" in content and "Б,1" in content


def test_error(monkeypatch):
    class DummySession:
        def get(self, url):
            raise Exception("network error")
    monkeypatch.setattr("requests.Session", DummySession)
    parser = BeastsParser()
    with pytest.raises(BeastsParserError):
        parser.get_animals_count_by_letter() 