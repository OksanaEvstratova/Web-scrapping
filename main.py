import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup
from fake_headers import Headers

def get_headers():
    return Headers(browser="firefox", os="win").generate()

def parse_article(vacancy_tag):
    link_tag = vacancy_tag.find("a", class_="bloko-link")
    if link_tag is None:
        return
    link = link_tag["href"]

    salary_tag = vacancy_tag.find(class_="bloko-header-section-2")
    if salary_tag is None:
        salary_tag_text = 0
    else:
        salary_tag_text = salary_tag.text.replace("\u202f", "")

    city_tag = vacancy_tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    company = vacancy_tag.find('a', class_='bloko-link bloko-link_kind-tertiary').text

    return {
        # "title": link_tag.find("span").text,
        "link": link,
        "salary": salary_tag_text,
        "company": company,
        "city": city_tag,
    }


def parse_page():
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    params = {
        'text': 'django, flask'
    }

    html = requests.get(url, headers=get_headers(), params=params).text
    soup = BeautifulSoup(html, features="html5lib")
    vacancies = soup.find_all(class_="vacancy-serp-item-body__main-info")
    vacancies_parsed = []
    for vacancy in vacancies:
        parsed = parse_article(vacancy)
        vacancies_parsed.append(parsed)
    return vacancies_parsed


if __name__ == "__main__":
    result = parse_page()
    with open('result.json', encoding='utf-8', mode='w') as f_json:
        json.dump(result, f_json, ensure_ascii=False, indent=4)

    pprint(result)