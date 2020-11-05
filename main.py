import requests
from bs4 import BeautifulSoup
from time import time


def print_duration():
    end_time = time()
    duration = end_time - start_time
    print("Done! Process took", str(duration) + "s")


def parse_urls(urls, first_index, loop=False):
    out_urls = []
    for item in urls:
        if loop:  # for iterating numeric values in url later on
            item = item.replace("1.html", "{}.html")
        end_index = item.index('">')
        new_item = item[first_index: end_index]
        new_item = "https://www.computerworld.pl" + new_item
        print(new_item)
        out_urls.append(new_item)
    return out_urls


def get_urls(urls):
    with open("urls.txt", "w") as output_file:
        for url in urls:
            for n in range(1, 1000):
                ready_url = url.format(str(n))
                print(ready_url)
                page_response = requests.get(ready_url)
                if page_response.status_code == 404:
                    break
                soup1 = BeautifulSoup(page_response.text, "html.parser")
                terminy = soup1.select("#termin")
                # print(terminy)
                base_termin_urls = str(terminy).split("\n")[1:-1]
                definition_urls = parse_urls(base_termin_urls, 13)
                print(definition_urls)
                for definition_url in definition_urls:
                    print(definition_url, file=output_file)
    print_duration()


def main_get_urls():
    root_url = "https://www.computerworld.pl/slownik/angielski/A/1.html"
    response = requests.get(root_url)
    soup = BeautifulSoup(response.text, "html.parser")
    letters = soup.select("#litera")
    base_urls = str(letters).split("\n")[3:-1]
    work_urls = parse_urls(base_urls, 9, True)
    get_urls(work_urls)


def main_get_definitions():
    with open("urls.txt") as url_file, open("slownik.txt", "w") as output_file:
        for url in url_file:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find("h1").text
            print(title)
            translation = soup.find("p").text
            for item in [title, translation, ""]:
                print(item, file=output_file)
    print_duration()


start_time = time()
main_get_definitions()
