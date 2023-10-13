import json
import re
import requests

from bs4 import BeautifulSoup as BS

# from .utils import slugify_uri

HOST = 'https://jut.su/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'


def slugify_uri(uri: str) -> str:
    return re.sub(r'[./]', '-', uri).strip('-')


class BaseParse:

    def create_request(self):
        raise NotImplemented('create_request not implemented')


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
        self.req = requests.get(self.link, headers={'User-agent': USER_AGENT})

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
        self.slug = slugify_uri(uri)
        self.file_name = self.slug
        self.req = None
        self.image = None
        self.name = None
        self.description = None
        self.genres = []
        self.links = []
        self.soup: BS = None
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
        return HOST + self.__uri

    def create_request(self):
        self.req = requests.get(self.url, headers={'User-Agent': USER_AGENT})

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
        loaded_links = self.get_loaded()
        is_updated = False

        for attr in self.__dir__():
            if attr.startswith('parse'):
                method = getattr(self, attr)
                if callable(method):
                    method()

        for link in self.links:
            link_slug = slugify_uri(link)
            if link_slug not in loaded_links:
                loaded_links.append(slugify_uri(link_slug))
                is_updated = True

        if is_updated:
            self.update_loaded(loaded_links)

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

    def parse_genres(self):
        additional = self.soup.select_one('.under_video_additional').text
        genres = [i.replace('Аниме', '').strip() for i in
                  re.split(r',|\sи\s', additional.split('.')[0].replace('Жанры:', ''))]
        print(genres)


if __name__ == '__main__':
    pss = ParseSeasonSeries('full-metal-alchemist/')
    pss.start()
    print(pss.image)
    print(pss.name)
    print(pss.genres)
    print(pss.description)
