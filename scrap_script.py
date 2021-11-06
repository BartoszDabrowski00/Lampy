import json

import requests
from bs4 import BeautifulSoup


def get_categories(lamps, baseurl, categories_links):
    req = requests.get(f'{baseurl}/lampy-sufitowe-c-760.html')
    soup = BeautifulSoup(req.content, 'lxml')
    categories = soup.find_all('li', class_='OknoRwd')

    for category in categories:
        link = category.find_all('a', href=True)[0]['href']
        name = category.find('span').get_text(strip=True)
        lamps[name] = {}
        categories_links.append(link)


def findSpec(itemsoup, specToFind):
    specifications = itemsoup.find(class_='DaneLista KolorLista')
    if specifications:
        correctTag = specifications.find(text=specToFind)
        if correctTag:
            return correctTag.findNext('strong').get_text(strip=True)
    return ''


def get_products(baseurl, lamps, categories_links):
    productlinks = []
    keys_list = list(lamps.keys())
    for i in range(len(categories_links)):
        print(keys_list[i])
        req = requests.get(categories_links[i])
        soup = BeautifulSoup(req.content, 'lxml')
        productlist = soup.find_all('div', class_='Okno OknoRwd')
        category_products = []

        for item in productlist:
            link = item.find_all('a', href=True)[0]
            productlinks.append(link['href'])
            itemreq = requests.get(link['href'])
            itemsoup = BeautifulSoup(itemreq.content, 'lxml')

            if not itemsoup:
                break

            name = itemsoup.find('h1', itemprop='name').get_text(strip=True)
            catalognumber = itemsoup.find('strong', itemprop='mpn').get_text(strip=True)
            price = itemsoup.find('span', itemprop='price')['content']
            inInventory = int(itemsoup.find('p', id="StanMagazynowy").find('img')['src'][46]) * 2
            picture = baseurl + '/' + itemsoup.find('img', itemprop='image')['src']
            description = itemsoup.find('div', itemprop='description').get_text(strip=True)
            description.replace(u'\xa0', u' ')

            lamp = {
                'name': name,
                'catalognumber': catalognumber,
                'price': price,
                'inInventory': inInventory,
                'picture': picture,
                'description': description,
                'specs': [{'Wysokość': findSpec(itemsoup, 'Wysokość:')},
                          {'Szerokość': findSpec(itemsoup, 'Szerokość:')},
                          {'Materiał': findSpec(itemsoup, 'Materiał:')},
                          {'Kolor': findSpec(itemsoup, 'Kolor podstawowy:')},
                          {'Trzonek': findSpec(itemsoup, 'Trzonek:')},
                          {'Moc żarówki': findSpec(itemsoup, 'Moc żarówki:')},
                          {'Napięcie zasilania': findSpec(itemsoup, 'Napięcie zasilania:')},
                          {'Ilość żarówek': findSpec(itemsoup, 'Ilość żarówek:')},
                          {'Kompatybilna z LED': findSpec(itemsoup, 'Kompatybilna z LED:')},
                          {'Źródło światła w komplecie': findSpec(itemsoup, 'Źródło światła w komplecie:')},
                          {'Klasa szczelności': findSpec(itemsoup, 'Klasa szczelności:')}]
            }
            category_products.append(lamp)
        lamps[keys_list[i]] = category_products


def save_lamps(lamps):
    with open('scrap_data.json', 'w') as file:
        json.dump(lamps, file)


def scrap():
    baseurl = "https://polskielampy.pl"
    lamps = {}
    categories_links = []
    get_categories(lamps, baseurl, categories_links)
    get_products(baseurl, lamps, categories_links)
    save_lamps(lamps)


if __name__ == '__main__':
    scrap()
