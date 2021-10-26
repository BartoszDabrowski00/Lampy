import requests
from bs4 import BeautifulSoup
import pandas as pd


#zwraca pole danej specyfikacji (wynika z budowy strony)
def findSpec(specToFind):
	specifications = itemsoup.find(class_='DaneLista KolorLista')
	correctTag = specifications.find(text=specToFind)
	if(correctTag):
		return correctTag.findNext('strong').get_text(strip=True)
	return ''



baseurl = "https://polskielampy.pl"

req = requests.get(baseurl + '/lampy-sufitowe-c-760.html/s=1')

soup = BeautifulSoup(req.content, 'lxml')
productlist = soup.find_all('div', class_='Okno OknoRwd')
productlinks = []
lamps = []

for item in productlist:
	link = item.find_all('a', href=True)[0]
	productlinks.append(link['href'])
	itemreq = requests.get(link['href'])
	itemsoup = BeautifulSoup(itemreq.content, 'lxml')

	name = itemsoup.find('h1', itemprop='name').get_text(strip=True)
	producent = itemsoup.find('div', itemprop='brand').get_text(strip=True)
	catalognumber = itemsoup.find('strong', itemprop='mpn').get_text(strip=True)
	price = itemsoup.find('span', itemprop='price')['content']
	inInventory = int(itemsoup.find('p', id="StanMagazynowy").find('img')['src'][46]) * 2
	picture = baseurl + '/' + itemsoup.find('img', itemprop='image')['src']
	description = itemsoup.find('div', itemprop='description').get_text(strip=True)
	description.replace(u'\xa0', u' ')

	lamp = {
		'name': name,
		'producent': producent,
		'catalognumber': catalognumber,
		'price': price,
		'inInventory': inInventory,
		'picture': picture,
		'description': description,
		'specs': 'Wysokość:' + findSpec('Wysokość:') + ',' +
		'Szerokość:' + findSpec('Szerokość:') + ',' +
		'Materiał:' + findSpec('Materiał:') + ',' +
		'Kolor:' + findSpec('Kolor podstawowy:') + ',' +
		'Trzonek:' + findSpec('Trzonek:') + ',' +
		'Moc żarówki:' + findSpec('Moc żarówki:') + ',' +
		'Napięcie zasilania:' + findSpec('Napięcie zasilania:') + ',' +
		'Ilość żarówek:' + findSpec('Ilość żarówek:') + ',' +
		'Kompatybilna z LED:' + findSpec('Kompatybilna z LED:') + ',' +
		'Źródło światła w komplecie:' + findSpec('Źródło światła w komplecie:') + ',' +
		'Klasa szczelności:' + findSpec('Klasa szczelności:')
	}
	print(lamp)
	lamps.append(lamp)

df = pd.DataFrame(lamps)
df.to_csv('scrapLamps.csv', sep=';', encoding='utf-8-sig')

print(lamps)