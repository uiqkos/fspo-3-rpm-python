from bs4 import BeautifulSoup


def parse(contents):
    soup = BeautifulSoup(contents, 'lxml')

    print(soup.h2)
    print(soup.head)
    print(soup.li)
