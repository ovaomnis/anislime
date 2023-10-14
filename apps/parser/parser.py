import json
import os.path
import re

import requests
from bs4 import BeautifulSoup as BS
from django.conf import settings

from apps.title.models import Title, Genre, Season, Series
from .utils import slugify_uri

HOST = 'https://jut.su/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
LOADED_PATH = settings.BASE_DIR / "apps/parser/loaded"
TITLE_POSTERS_URL = 'title_posters/'
TITLE_POSTERS_ROOT = settings.MEDIA_ROOT / TITLE_POSTERS_URL
TITLE_VIDEO_URL = 'videos/'
TITLE_VIDEO_ROOT = settings.MEDIA_ROOT / TITLE_VIDEO_URL


# def slugify_uri(uri: str) -> str:
#     return re.sub(r'[./]', '-', uri).strip('-')


class LoadedMixin:
    file_name = None

    def get_loaded(self):
        if not LOADED_PATH.exists():
            LOADED_PATH.mkdir(parents=True, exist_ok=True)

        try:
            with open(f'{LOADED_PATH}/{self.file_name}.json', 'r+') as file:
                content = file.read()
                if not content:
                    return []
                return json.loads(content)
        except FileNotFoundError:
            with open(f'{LOADED_PATH}/{self.file_name}.json', 'w+') as file:
                file.write(json.dumps([]))
                file.seek(0)
                return json.load(file)

    def update_loaded(self, links: list):
        with open(f'{LOADED_PATH}/{self.file_name}.json', 'w+') as file:
            file.write(json.dumps(links))


class BaseParse:
    req = None
    soup = None
    __uri = None

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
        raise NotImplemented('create_request not implemented')

    def set_up_soup(self):
        self.soup = BS(self.req.content, 'lxml')

    def start_parsing(self):
        for attr in self.__dir__():
            if attr.startswith('parse'):
                method = getattr(self, attr)
                if callable(method):
                    method()


class ParseSeries(BaseParse):
    def __init__(self, uri: str, title: Title):
        self.title = title
        self.video = None
        self.__season = None
        self.__season_number = None
        self.uri = uri
        self.series = uri.split('/')[-1][:-5]
        self.name = None
        self.slug = slugify_uri(uri.replace(HOST, ''))
        self.req = None
        self.number = int(self.series.split('-')[-1])
        self.create_request()
        self.set_up_soup()
        self.start()
        # print(self.series, self.slug)

    def start(self):
        self.start_parsing()
        Series.objects.create(**self.data)

    @property
    def data(self):
        return {
            'season': self.season,
            'number': self.number,
            'name': self.name,
            'video': self.video,
            'slug': self.slug,
            'title': self.title
        }

    @property
    def season(self):
        season_slug = self.__season if self.__season.startswith('season') else 'film'
        season = Season.objects.filter(slug=season_slug)
        if not season:
            return Season.objects.create(slug=season_slug, number=self.number, is_film=True)
        return season[0]

    def __str__(self):
        return self.data

    def create_request(self):
        # print(self.link)
        self.req = requests.get(HOST + self.uri, headers={'User-agent': USER_AGENT})

    def parse_season(self):
        season_match = re.search(r'/season-(\d+)/', self.uri)
        film_match = re.search(r'/film-(\d+)', self.uri)

        if season_match:
            self.__season = f'season-{season_match.group(1)}'
        elif film_match:
            self.__season = f'film-{str(film_match.group(1))}'
        else:
            self.__season = 'season-1'

        self.__season_number = int(self.__season.split('-')[-1])

    def parse_name(self):
        self.name = self.soup.select_one('.video_plate_title').text

    def parse_video(self):
        soup = self.soup
        video_src = soup.find('video').find('source', attrs={'label': '480p'}).get('src')
        video_url = f'{TITLE_VIDEO_URL + self.slug}.mp4'

        if not os.path.exists(TITLE_VIDEO_ROOT / self.slug):
            chunk_size = 258
            res = requests.get(video_src, headers={'User-Agent': USER_AGENT}, stream=True)
            with open(f'{TITLE_VIDEO_ROOT / self.slug}.mp4', 'wb') as file:
                for chunk in res.iter_content(chunk_size=chunk_size):
                    file.write(chunk)

        self.video = video_url


class ParseSeasonSeries(BaseParse, LoadedMixin):
    series_parser = ParseSeries
    __uri = None

    def __init__(self, uri: str, memorize: bool = False):
        self.memorize = memorize
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
        self.start()

    @property
    def data(self):
        return {
            'slug': self.slug,
            'poster': self.image,
            'name': self.name,
            'description': self.description,
            'age_rating': 12
        }

    def create_request(self):
        self.req = requests.get(self.url, headers={'User-Agent': USER_AGENT})

    def prepare_genres(self):
        for genre in self.genres:
            genre_obj, _ = Genre.objects.get_or_create(name=genre.capitalize())
            yield genre_obj

    def start(self):
        self.start_parsing()
        is_updated = False

        title_obj, _ = Title.objects.get_or_create(**self.data)
        title_obj.genres.add(*self.prepare_genres())

        if self.memorize:
            loaded_links = set(self.get_loaded())
        else:
            loaded_links = set([])

        for link in self.links:
            if link not in loaded_links:
                ParseSeries(uri=link, title=title_obj)
                loaded_links.add(link)
                is_updated = True

        if self.memorize and is_updated:
            self.update_loaded(list(loaded_links))

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
            if not TITLE_POSTERS_ROOT.exists():
                TITLE_POSTERS_ROOT.mkdir(parents=True, exist_ok=True)

            image_url = match.group(1)
            image_name = slugify_uri(image_url.replace('https://', '')) + '.jpg'
            with open(f'{TITLE_POSTERS_ROOT}/{image_name}', 'wb+') as file:
                file.write(requests.get(image_url, headers={'User-Agent': USER_AGENT}).content)
            self.image = TITLE_POSTERS_URL + image_name
        else:
            print('Image not found')

    def parse_description(self):
        self.description = self.soup.select_one('.under_video').text

    def parse_genres(self):
        additional = self.soup.select_one('.under_video_additional').text
        self.genres = [i.replace('Аниме', '').strip() for i in
                       re.split(r',|\sи\s', additional.split('.')[0].replace('Жанры:', ''))]
