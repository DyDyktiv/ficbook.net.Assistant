# import requests
import bs4


class FicSize:
    def __init__(self, s):
        self.planned = s['planned']
        self.pages = s['pages']
        self.parts = s['parts']
        self.specific = self.pages * 100 // self.parts

    def updata(self, s):
        self.planned = s.get('planned', self.planned)
        self.pages = s.get('pages', self.pages)
        self.parts = s.get('parts', self.parts)
        self.specific = self.pages * 100 // self.parts


def http2text(inurl):
    # text = requests.get(url).text
    with open('1544316663.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    soup = bs4.BeautifulSoup(text, 'html.parser')
    fics = soup.select('.fanfic-thumb-block')
    i = 1
    for item in fics:
        if 'fanfic-thumb-block-premium' in item.attrs['class']:
            continue
        link = item.find('a', {'class': 'visit-link'}).get('href')
        link = link[link.rfind('/') + 1:]
        name = item.find('a', {'class': 'visit-link'}).text
        count = int(item.find('sup', {'class': 'count'}).text)
        reward = int(item.find('sup', {'class': 'reward'}).text)
        fandoms, pairings, genres, raiting, warnings, status = 0, 0, 0, 0, 0, 0
        s = dict()
        for dt in item.findAll('dt'):
            title = dt.text
            if title == 'Фэндом:':
                fandoms = tuple(map(lambda fandom: fandom.text,
                                    dt.find_next_siblings('dd')[0].findAll('a')))
            elif title == 'Пэйринг и персонажи:':
                pairings = ', '.join(map(lambda pair: pair.text,
                                         dt.find_next_siblings('dd')[0].findAll('a')))
            elif title == 'Рейтинг:':
                raiting = dt.find_next_siblings('dd')[0].find('strong').text.strip()
            elif title == 'Жанры:':
                genres = tuple(map(lambda genre: genre.text.strip(),
                                   dt.find_next_siblings('dd')[0].findAll('a')))
            elif title == 'Предупреждения:':
                warnings = tuple(map(lambda warning: warning.text.strip(),
                                     dt.find_next_siblings('dd')[0].findAll('strong')))
            elif title == 'Размер:':
                r = dt.find_next_siblings('dd')[0].text.strip().split(',\n')
                s['planned'] = r[0]
                s['pages'] = int(r[1].split(' ')[0])
                s['parts'] = int(r[2].split(' ')[0])
                s = FicSize(s)
            elif title == 'Статус:':
                status = dt.find_next_siblings('dd')[0].text.strip()
            else:
                print(dt.text, False)
        note = item.find('div', {'class': 'wrap word-break urlize fanfic-description-text'}).text.strip()
        print(f'{i}: {name}(id{link}) +{count}({reward})\n\tФэндом: {", ".join(fandoms)}')
        if pairings:
            print('\tПэйринг и персонажи:', pairings)
        print('\tРейтинг:', raiting)
        if genres:
            print('\tЖанры:', ', '.join(genres))
        if warnings:
            print('\tПредупреждения:', ', '.join(warnings))
        print(f'\tРазмер: {s.planned}, {s.pages} pages, {s.parts} parts, {s.specific // 100} pages/part')
        print('\tСтатус:', status)
        input(note)
        i += 1
    return inurl + str(i)


with open('initial.txt', 'r', encoding='utf-8') as ini:
    for url in ini:
        http2text(url)
