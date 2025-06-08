import requests
import json
from bs4 import BeautifulSoup


class LLM_Tool:

    def __init__(self) -> None:
        pass

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def call(self, count: int = 1) -> str:
        pass


class World_Tool(LLM_Tool):

    def __init__(self) -> None:
        self.name = "random_world"
        self.description = "Инструмент для генерации случайных Миров"

    def call(self, count: int = 1) -> str:
        r = requests.get(
            "https://donjon.bin.sh/fantasy/random/rpc-fantasy.fcgi?type=World&n=10"
        )
        res = json.loads(r.text)
        res = res[:count]
        return "## Набор случайных описаний Миров:" + "\n".join(res)


class Locations_Tool(LLM_Tool):

    def __init__(self) -> None:
        self.name = "random_location"
        self.description = "Инструмент для генерации случайных Локаций"

    def call(self, count: int = 1) -> str:
        r = requests.get(
            "https://donjon.bin.sh/fantasy/random/rpc-fantasy.fcgi?type=Location&loc_type=&n=10"
        )
        res = json.loads(r.text)
        res = res[:count]
        return "## Набор случайных описаний Локаций:" + "\n".join(res)


class Character_Tool(LLM_Tool):

    def __init__(self) -> None:
        self.name = "random_character"
        self.description = "Инструмент для генерации случайных Персонажей"

    def call(self, count: int = 1) -> str:
        r = requests.get(
            "https://donjon.bin.sh/fantasy/random/rpc-fantasy.fcgi?type=NPC&race=&gender=&order=&culture=&n=10"
        )
        res = json.loads(r.text)
        res = res[:count]
        return "## Набор случайных описаний Персонажей:" + "\n".join(res)


class Town_Tool(LLM_Tool):

    def __init__(self) -> None:
        self.name = "random_town"
        self.description = "Инструмент для генерации случайных Городов"

    def call(self, count: int = 1) -> str:
        r = requests.get(
            "https://donjon.bin.sh/fantasy/random/rpc-fantasy.fcgi?type=Town&size=&race=&culture=&n=10"
        )
        res = json.loads(r.text)
        res = res[:count]
        return "## Набор случайных описаний Городов:" + "\n".join(res)


class Adventure_Tool(LLM_Tool):

    def __init__(self) -> None:
        self.name = "random_adventure"
        self.description = "Инструмент для генерации случайных Приключений"

    def get_adv(self):
        r = requests.get("https://donjon.bin.sh/fantasy/adventure/")
        soup = BeautifulSoup(r.text, "html.parser")
        adventure_data = {}
        table = soup.find("table", id="adventure")
        rows = table.find_all("tr", class_="section")
        for row in rows:
            section_title = row.find("td", class_="section_title").get_text(strip=True)
            value_cell = row.find("td").find_next_sibling("td")
            value = (
                value_cell.find("b").get_text(strip=True)
                if value_cell.find("b")
                else value_cell.get_text(strip=True)
            )
            next_row = row.find_next_sibling("tr")
            description = next_row.find("td").get_text(strip=True) if next_row else ""
            adventure_data[section_title] = {"value": value, "description": description}
            return json.dumps(adventure_data)

    def call(self, count: int = 1) -> str:
        res = []
        for i in range(count):
            res.append(self.get_adv())
        return "## Случайное приключение" + "\n".join(res)
