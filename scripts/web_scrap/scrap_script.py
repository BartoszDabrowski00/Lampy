import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle

LOAD = False


def get_categories(category_list, baseurl, categories_links, endpoint, index, home):
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
        category_list.append([index, 1, name, home, 0, name])
        categories_links.append(link)
    return index


def findSpec(itemsoup, specToFind):
    specifications = itemsoup.find(class_='DaneLista KolorLista')
    if specifications:
        correctTag = specifications.find(text=specToFind)
        if correctTag:
            return correctTag.findNext('strong').get_text(strip=True)
    return ''


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
    category_list = []
    endpoints = [('/lampy-sufitowe-c-760.html', 'Lampy sufitowe'), ('/lampy-wiszace-c-134.html', 'Lampy wiszące')]
    index = 0
    for endpoint, home in endpoints:
        index = get_categories(category_list, baseurl, categories_links, endpoint, index, home)
    get_products(baseurl, lamps, category_list, categories_links)
    save(lamps, category_list)


if __name__ == '__main__':
    if not LOAD:
        scrap()
    else:
        lamps, categories = load()
        save(lamps, categories)
