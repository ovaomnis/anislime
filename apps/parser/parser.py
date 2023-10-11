import json
import re
import requests

from bs4 import BeautifulSoup as BS


class BaseParse:
    HOST = 'https://jut.su/'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'

    def create_request(self):
        raise NotImplemented('create_request not implemented')

    @staticmethod
    def slugify_uri(uri: str) -> str:
        return re.sub(r'[./]', '-', uri).strip('-')


class ParseSeries(BaseParse):
    def __init__(self, season: str, link: str, name: str):
        self.season = season
        self.link = link
        self.series = link.split('/')[-1][:-5]
        self.name = name
        self.req = None
        self.create_request()

    def __str__(self):
        return json.dumps({
            'season': self.season,
            'series': self.series,
            'name': self.name,
            'link': self.link
        }, indent=2, ensure_ascii=False)

    def create_request(self):
        # print(self.link)
        self.req = requests.get(self.link, headers={'User-agent': self.USER_AGENT})

    def get_soup(self):
        return BS(self.req.content, 'lxml')

    def parse(self):
        soup = self.get_soup()
        print(soup.find('video').find('source', attrs={'label': '1080p'}))


class ParseSeasonSeries(BaseParse):
    series_parser = ParseSeries
    __uri = None

    def __init__(self, uri: str):
        self.uri = uri
        self.slug = self.slugify_uri(uri)
        self.file_name = self.slug
        self.req = None
        self.image = None
        self.name = None
        self.age_rating = None
        self.years = []
        self.status = None
        self.orig_name = None
        self.genres = []
        self.links = []
        self.soup: BS = None
        self.__additional = []
        self.create_request()
        self.set_up_soup()

    @property
    def uri(self):
        return self.__uri

    @uri.setter
    def uri(self, value: str):
        if value.startswith('https:') or value.startswith('http:'):
            raise ValueError(f'uri starts with host')

        self.__uri = value

    @property
    def url(self):
        return self.HOST + self.__uri

    def create_request(self):
        self.req = requests.get(self.url, headers={'User-Agent': self.USER_AGENT})

    def get_loaded(self):
        try:
            with open(f'loaded/{self.file_name}.json', 'r+') as file:
                content = file.read()
                if not content:
                    return []
                return json.loads(content)
        except FileNotFoundError:
            with open(f'loaded/{self.file_name}.json', 'w+') as file:
                file.write(json.dumps([]))
                file.seek(0)
                return json.load(file)

    def update_loaded(self, links: list):
        with open(f'loaded/{self.file_name}.json', 'w+') as file:
            file.write(json.dumps(links))

    def set_up_soup(self):
        self.soup = BS(self.req.content, 'lxml')

    def start(self):
        # soup = self.get_soup()
        # links = soup.select('.short-btn')
        # loaded_links = self.get_loaded()
        # is_updated = False
        #
        # for link in links:
        #     href = re.sub(r'[./]', '-', link.get('href'))[1:]
        #     if href not in loaded_links:
        #         is_updated = True
        #         print(href)
        #         loaded_links.append(href)
        #
        # if is_updated:
        #     self.update_loaded(loaded_links)
        for attr in self.__dir__():
            if attr.startswith('parse'):
                method = getattr(self, attr)
                if callable(method):
                    method()

    def parse_links(self):
        for i in self.soup.select('.short-btn'):
            self.links.append(i.get('href'))

    def parse_name(self):
        self.name = self.soup.select_one('.header_video').text

    def parse_image(self):
        style = self.soup.select_one('div .all_anime_title').get('style')
        url_pattern = r"url\(['\"](https?://[^\)]+)['\"]\)"
        match = re.search(url_pattern, style)
        if match:
            self.image = match.group(1)
        else:
            print('Image not found')

    def parse_additional(self):
        self.__additional = self.soup.select_one('.under_video_additional')
        print(re.split(r'\sЖанры:\s', str(self.__additional)))


    # def parse_genres(self):
    #     for i in re.split(r"\bи\b|,", self.__additional[0].split(':')[1]):
    #         self.genres.append(i.replace('Аниме', '').strip())
    #
    # def parse_years(self):
    #     for i in re.split(r"\bи\b|,", self.__additional[1].split(':')[1]):
    #         self.years.append(i.replace('Аниме', '').strip())
    #
    # def parse_orig_name(self):
    #     print(self.__additional[2])


if __name__ == '__main__':
    pss = ParseSeasonSeries('dekiru-neko-wa-kyou/')
    pss.start()
