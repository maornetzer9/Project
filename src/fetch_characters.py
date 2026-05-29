"""
fetch_characters.py
שולף דמויות מה-Rick and Morty API:
  - Species: Human  |  Status: Alive  |  Origin: Earth
"""

import requests
import csv
import os

API_URL = "https://rickandmortyapi.com/api/character"
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "characters.csv")


def fetch_all_characters():
    """שולף את כל הדמויות מכל הדפים."""
    characters = []
    url = API_URL
    params = {"status": "alive", "species": "Human"}

    while url:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        characters.extend(data["results"])
        url = data["info"].get("next")  # None בדף האחרון → הלולאה נעצרת
        params = {}

    return characters


def filter_earth_characters(characters):
    """מסנן רק דמויות שמוצאן כדור הארץ."""
    return [
        c for c in characters
        if "Earth" in c.get("origin", {}).get("name", "")
    ]


def build_rows(characters):
    """בונה שורות לקובץ CSV."""
    return [
        {"Name": c["name"], "Location": c["location"]["name"], "Image": c["image"]}
        for c in characters
    ]


def write_csv(rows, filepath=OUTPUT_FILE):
    """כותב CSV."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Location", "Image"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ נכתבו {len(rows)} דמויות לקובץ: {filepath}")


def get_characters():
    """מחזירה רשימה מסוננת – משמשת גם את app.py."""
    return build_rows(filter_earth_characters(fetch_all_characters()))


if __name__ == "__main__":
    write_csv(get_characters())