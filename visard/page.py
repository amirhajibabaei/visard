import urllib
from bs4 import BeautifulSoup


class Page:
    """
    wrapper around bs
    """

    def __init__(self, url):
        self.url = urllib.request.urlopen(url)
        self.content = self.url.read()
        self.soup = BeautifulSoup(self.content, "html.parser")


def example():
    self = Page('https://pubs.rsc.org/en/content/articlehtml/2017/ee/c6ee02697d')
    for tab in self.soup.find_all('div', {'class': lambda c: c and 'table' in c}):
        print(tab['class'])


if __name__ == '__main__':
    example()
