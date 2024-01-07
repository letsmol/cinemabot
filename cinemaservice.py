from dataclasses import dataclass

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from yarl import URL

from config import KINOPOISK_API_KEY, BAD_LINKS


@dataclass
class Movie:
    name: str
    description: str | None
    rating: float
    poster_url: str | None


async def find_movie(movie_name: str) -> Movie | None:
    headers = {
        'X-API-KEY': KINOPOISK_API_KEY
    }
    async with ClientSession(headers=headers) as session:
        url = 'https://api.kinopoisk.dev/v1.4/movie/search'
        async with session.get(url, params={'query': movie_name}) as response:
            data = await response.json()
            docs = data['docs']
            if not docs:
                return None

            movie = docs[0]
            movie_name = movie['name']
            rating = float(movie['rating']['kp'])
            description = movie['shortDescription']\
                or movie['description'][:150] or 'No description'
            poster_url = movie['poster']['url'] if movie['poster'] else None
            return Movie(movie_name, description, rating,
                         poster_url)

print(BAD_LINKS)


async def find_movie_link(movie_name: str) -> str:
    async with ClientSession() as session:
        url = 'https://duckduckgo.com/html'
        query = f'{movie_name} смотреть бесплатно без смс и регистрации'
        async with session.get(url, params={'q': query}) as response:
            soup = BeautifulSoup(await response.text(), features='lxml')
            links = soup.find_all('a', attrs={"class": "result__a"}, href=True)
            for link in links:
                href = str(link['href'])
                url = URL(href).query.get('uddg', 'https:' + href)
                is_bad_link = any(
                    [i for i in BAD_LINKS if url.startswith(i.strip())])
                if not is_bad_link:
                    return str(url)
            return ''
