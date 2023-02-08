from bs4 import BeautifulSoup
import requests
import validators
import os


def download_schedule(
    base_url: str = "https://esystem.rudn.ru",
    schedule_url: str = "https://esystem.rudn.ru/faculty/ia/raspisanie",
    folder_path="downloads\\",
    downloaded_file_name="new_schedule",
):
    base_url = "https://esystem.rudn.ru"
    if not validators.url(base_url):
        raise Exception("Invalid url")
    response = requests.get("https://esystem.rudn.ru/faculty/ia/raspisanie")
    if response.status_code != 200:
        raise Exception("Page doesn't response")
    html = response.text
    html_objects = BeautifulSoup(html, "html.parser")
    files = html_objects.find_all("p", class_="o-file")
    if not os.path.exists(os.path.join(os.getcwd(), folder_path)):
        os.mkdir(os.path.join(os.getcwd(), folder_path))
    if not files:
        raise Exception("No files found")
    for file in files:
        if "транспорт" in file.text.lower():
            response = requests.get(base_url + file["href"])
            with open(f"{folder_path}\\{downloaded_file_name}.xlsx", "wb") as schedule:
                schedule.write(response.content)
            break
