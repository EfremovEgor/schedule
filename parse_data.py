from bs4 import BeautifulSoup
import requests
import validators
import os


class PageDoesNotResponseException(Exception):
    pass


class FilesNotFoundException(Exception):
    pass


class InvalidUrlException(Exception):
    pass


def download_schedule(
    base_url: str = "https://esystem.rudn.ru",
    schedule_url: str = "https://esystem.rudn.ru/faculty/ia/raspisanie-dnevnoi-formy-obucheniya",
    folder_path="downloads\\",
    downloaded_file_name="new_schedule",
):
    base_url = "https://esystem.rudn.ru"
    if not validators.url(base_url):
        raise InvalidUrlException
    response = requests.get(schedule_url)
    if response.status_code != 200:
        raise PageDoesNotResponseException
    html = response.text
    html_objects = BeautifulSoup(html, "html.parser")
    files = html_objects.find_all("p", class_="o-file")
    if not os.path.exists(os.path.join(os.getcwd(), folder_path)):
        os.mkdir(os.path.join(os.getcwd(), folder_path))
    if not files:
        raise FilesNotFoundException
    for file in files:
        if "транспорт" in file.text.lower():
            response = requests.get(base_url + file["href"])
            with open(f"{folder_path}\\{downloaded_file_name}.xlsx", "wb") as schedule:
                schedule.write(response.content)
            break
