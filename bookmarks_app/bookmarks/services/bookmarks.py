from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from django.core.files import File

from bookmarks.models import Bookmark


class BookmarkService(object):
    def get_url_type(self, soup):
        url_type = soup.find("meta", attrs={"property": "og:type"})
        if url_type:
            return url_type["content"]
        return "website"

    def get_title(self, soup):
        title = soup.find("meta", attrs={"property": "og:title"})
        if title:
            return title["content"]
        title = soup.find("title")
        if title:
            return title.text

    def get_description(self, soup):
        description = soup.find("meta", attrs={"property": "og:description"})
        if description:
            return description["content"]
        description = soup.find("meta", attrs={"name": "description"})
        if description:
            return description["content"]

    def get_image_url(self, soup):
        image_url = soup.find("meta", attrs={"property": "og:image"})
        if image_url:
            return image_url["content"]

    def upload_image(self, bookmark, image_url):
        image = NamedTemporaryFile(delete=True)
        image.write(urlopen(image_url).read())
        image.flush()
        bookmark.image.save("bookmark_image.jpg", File(image))
        return bookmark

    def get_attributes(self, url):
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            return None, None, None, None
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, features="lxml")
        url_type = self.get_url_type(soup)
        title = self.get_title(soup)
        description = self.get_description(soup)
        image_url = self.get_image_url(soup)
        return url_type, title, description, image_url

    def create(self, url, creator):
        url_type, title, description, image_url = self.get_attributes(url)
        new_bookmark = Bookmark(
            title=title,
            description=description,
            url=url,
            url_type=url_type,
            creator=creator,
        )
        if image_url:
            self.upload_image(new_bookmark, image_url)
        new_bookmark.save()
        return new_bookmark
