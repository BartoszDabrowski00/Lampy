import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle

LOAD = False


# main_category_list contains:
# [0] id, [1] category name
def get_main_categories(endpoints, main_category_list):
    i = 1
    for endpoint in endpoints:
        main_category_list.append([i, endpoint[2]])
        i += 1


# category_list contains:
# [0] id, [1] main category id, [2] category name
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
        category_list.append([index, main_index, name])
        categories_links.append(link)
    return index


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


def get_products(baseurl, lamps, category_list, categories_links):
    productlinks = []
    for i in range(len(categories_links)):
        print(category_list[i])
        req = requests.get(categories_links[i])
        soup = BeautifulSoup(req.content, 'lxml')
        productlist = soup.find_all('div', class_='Okno OknoRwd')

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

            lamp = {
                'ID': i + 100,
                'name': name,
                'catalognumber': catalognumber,
                'cena netto': price,
                'cena brutto': price / 1.23,
                'ID regula podatkowa': 1,
                'ID kategorii': category_list[i][0],
                'inInventory': inInventory,
                'picture': picture,
                'description': description,
                'category': category_list[i][2],
                'Wysokość': findSpec(itemsoup, 'Wysokość:'),
                'Szerokość': findSpec(itemsoup, 'Szerokość:'),
                'Specyfikacja':
                    'Materiał:' + findSpec(itemsoup, 'Materiał:') + '   ' +
                    'Kolor:' + findSpec(itemsoup, 'Kolor podstawowy:') + '   ' +
                    'Trzonek:' + findSpec(itemsoup, 'Trzonek:') + '   ' +
                    'Moc żarówkiL' + findSpec(itemsoup, 'Moc żarówki:') + '   ' +
                    'Napięcie zasilaniaL' + findSpec(itemsoup, 'Napięcie zasilania:') + '   ' +
                    'Ilość żarówekL' + findSpec(itemsoup, 'Ilość żarówek:') + ' ' +
                    'Kompatybilna z LEDL' + findSpec(itemsoup, 'Kompatybilna z LED:') + '   ' +
                    'Źródło światła w komplecieL' + findSpec(itemsoup, 'Źródło światła w komplecie:') + '   ' +
                    'Klasa szczelnościL' + findSpec(itemsoup, 'Klasa szczelności:')

            }
            lamps.append(lamp)


def save(lamps, categories):
    with open('categories.pickle', 'wb') as handle:
        pickle.dump(categories, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('lamps.pickle', 'wb') as handle:
        pickle.dump(lamps, handle, protocol=pickle.HIGHEST_PROTOCOL)
    pd.DataFrame(categories).to_csv('categories.csv', sep=',', encoding='utf-8', index=False)
    pd.DataFrame(lamps).to_csv('lamps.csv', sep=',', encoding='utf-8', index=False)


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
    main_category_list = []
    category_list = []
    endpoints = [(1, '/lampy-sufitowe-c-760.html', 'Lampy sufitowe'), (2, '/lampy-wiszace-c-134.html', 'Lampy wiszące')]
    index = 0
    get_main_categories(endpoints, main_category_list)
    for main_index, endpoint, home in endpoints:
        index = get_categories(category_list, baseurl, categories_links, endpoint, main_index, index)
    print(category_list)
    get_products(baseurl, lamps, category_list, categories_links)
    save(lamps, category_list)


if __name__ == '__main__':
    if not LOAD:
        scrap()
    else:
        lamps, categories = load()
        save(lamps, categories)
