import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle

LOAD = False


# category_list contains:
# [0] root category id, [1] main category name, [2] category name
def get_main_categories(endpoints, category_list):
    for endpoint in endpoints:
        category_list.append([0, 'Strona główna', endpoint[2]])


def get_categories(category_list, baseurl, categories_links, endpoint, main_index, index):
    subcategories_limit = 8
    req = requests.get(f'{baseurl}{endpoint}')
    soup = BeautifulSoup(req.content, 'lxml')
    categories = soup.find_all('li', class_='OknoRwd')
    for category in categories:
        subcategories_limit -= 1
        if subcategories_limit == 0:
            break
        index += 1
        link = category.find_all('a', href=True)[0]['href']
        name = category.find('span').get_text(strip=True)
        category_list.append([0, category_list[main_index][2], name])
        categories_links.append(link)
    return index


def add_attribute(attribute_list, id, quantity):
    if quantity > 0:
        row = {
            'id': id,
            'attribute': 'Rodzaj wtyczki:select:1',
            'value': 'Europejska:1',
            'impact on weight': 0,
            'quantity': int(quantity/2)
        }
        attribute_list.append(row)
        row2 = {
            'id': id,
            'attribute': 'Rodzaj wtyczki:select:1',
            'value': 'Amerykańska:1',
            'impact on weight': 0,
            'quantity': int(quantity/2)
        }
        attribute_list.append(row2)

def findSpec(itemsoup, specToFind):
    specifications = itemsoup.find(class_='DaneLista KolorLista')
    if specifications:
        correctTag = specifications.find(text=specToFind)
        if correctTag:
            return correctTag.findNext('strong').get_text(strip=True)
    return ''


def textToPrice(priceText):
    priceFloat = 0
    for letter in priceText:
        if letter >= '0' and letter <= '9':
            priceFloat += int(letter)
            priceFloat *= 10
    priceFloat /= 1000
    return priceFloat

def get_attributes(itemsoup):
    text = ''
    attributes = {
        'Wysokość': findSpec(itemsoup, 'Wysokość:'),
        'Szerokość': findSpec(itemsoup, 'Szerokość:'),
        'Materiał': findSpec(itemsoup, 'Materiał:'),
        'Kolor': findSpec(itemsoup, 'Kolor podstawowy:'),
        'Trzonek': findSpec(itemsoup, 'Trzonek:'),
        'Moc żarówki': findSpec(itemsoup, 'Moc żarówki:'),
        'Napięcie zasilania': findSpec(itemsoup, 'Napięcie zasilania:'),
        'Ilość żarówek': findSpec(itemsoup, 'Ilość żarówek:'),
        'Kompatybilna z LED': findSpec(itemsoup, 'Kompatybilna z LED:'),
        'Źródło światła w komplecie': findSpec(itemsoup, 'Źródło światła w komplecie:'),
        'Klasa szczelności': findSpec(itemsoup, 'Klasa szczelności:')
    }
    for attribute in attributes:
        text += attribute + ':' + attributes[attribute] + ','
    text = text[0:-1]
    return text


def get_products(baseurl, lamps, category_list, categories_links, attribute_list):
    productlinks = []
    productIndex = 100
    for i in range(len(categories_links)):
        req = requests.get(categories_links[i])
        soup = BeautifulSoup(req.content, 'lxml')
        productlist1 = soup.find_all('div', class_='Okno OknoRwd')
        productlist = []
        productlist.append(productlist1[0])
        productlist.append(productlist1[1])
        productlist.append(productlist1[2])
        productlist.append(productlist1[3])

        for item in productlist:
            link = item.find_all('a', href=True)[0]
            productlinks.append(link['href'])
            itemreq = requests.get(link['href'])
            itemsoup = BeautifulSoup(itemreq.content, 'lxml')

            if not itemsoup:
                break

            name = itemsoup.find('h1', itemprop='name').get_text(strip=True)
            catalognumber = itemsoup.find('strong', itemprop='mpn').get_text(strip=True)
            inInventory = int(itemsoup.find('p', id="StanMagazynowy").find('img')['src'][46]) * 2
            picture = baseurl + '/' + itemsoup.find('img', itemprop='image')['src']
            description = itemsoup.find('div', itemprop='description').get_text(strip=True)
            description.replace(u'\xa0', u' ')
            try:
                price = textToPrice(itemsoup.find('id', itemprop='CenaPoprzednia').find('strong'))
                break
            except AttributeError:
                price = float(itemsoup.find('span', itemprop='price')['content'])

            add_attribute(attribute_list, productIndex, inInventory)
            lamp = {
                'ID': productIndex,
                'name': name,
                'catalognumber': catalognumber,
                #'cena netto': price / 1.23,
                'cena brutto': price,
                'ID regula podatkowa': 1,
                'ID kategorii': category_list[i][2],
                'inInventory': inInventory,
                'picture': picture,
                'description': description,
                #'category': category_list[i][2],
                'attributes': get_attributes(itemsoup)
            }
            lamps.append(lamp)
            productIndex += 1
            print(lamp)
            print(attribute_list)


def save(lamps, categories, attributes):
    with open('categories.pickle', 'wb') as handle:
        pickle.dump(categories, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('attributes.pickle', 'wb') as handle:
        pickle.dump(attributes, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('lamps.pickle', 'wb') as handle:
        pickle.dump(lamps, handle, protocol=pickle.HIGHEST_PROTOCOL)
    pd.DataFrame(categories).to_csv('categories.csv', sep=';', encoding='utf-8', index=False)
    pd.DataFrame(attributes).to_csv('attributes.csv', sep=';', encoding='utf-8', index=False)
    pd.DataFrame(lamps).to_csv('lamps.csv', sep=';', encoding='utf-8', index=False)


def load():
    with open('lamps.pickle', 'rb') as handle:
        lamps = pickle.load(handle)
    with open('categories.pickle', 'rb') as handle:
        categories = pickle.load(handle)
    return lamps, categories


def scrap():
    baseurl = "https://polskielampy.pl"
    lamps = []
    categories_links = []
    category_list = []
    attribute_list = []
    endpoints = [(1, '/lampy-sufitowe-c-760.html', 'Lampy sufitowe'), (2, '/lampy-wiszace-c-134.html', 'Lampy wiszące')]
    index = 0
    get_main_categories(endpoints, category_list)
    for main_index, endpoint, home in endpoints:
        index = get_categories(category_list, baseurl, categories_links, endpoint, main_index, index)
    print(category_list)
    print(attribute_list)
    get_products(baseurl, lamps, category_list, categories_links, attribute_list)
    save(lamps, category_list, attribute_list)


if __name__ == '__main__':
    if not LOAD:
        scrap()
    else:
        lamps, categories = load()
