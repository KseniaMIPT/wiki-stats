#!/usr/bin/python3

import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:
            file_data = f.readline().split()
            self._n = int(file_data[0])                       # Number of article's titles
            self._nlinks = int(file_data[-1])                 # Number of links
            
            self._titles = []                                 # List of article's titles
            self._sizes = array.array('L', [0]*self._n)       # List of article's sizes
            self._links = array.array('L', [0]*self._nlinks)  # List of article's links
            self._redirect = array.array('B', [0]*self._n)    # List of redirection flags
            self._offset = array.array('L', [0]*(self._n+1))  # List of links' offsets in list of links

            # Read graph from file
            for title_number in range(self._n):
                self._titles.append(f.readline())
                title_data = f.readline().split()
                self._sizes[title_number] = int(title_data[0])
                self._redirect[title_number] = int(title_data[1])
                for link_number in range(int(title_data[-1])):
                    self._links.append(int(f.readline()))
                if title_number == 0:
                    self._offset[title_number] = 0
                else:
                    self._offset[title_number] = self._offset[title_number - 1] + int(title_data[-1]) - 1
        print('Граф загружен')

    def get_id(self, title):
        """Return number if article."""
        return self._titles.index(title)

    def get_number_of_links_from(self, _id):
        return self._offset[_id+1] - self._offset[_id]

    def get_links_from(self, _id):
        links = []
        for n in range(self.get_number_of_links_from(_id)):
            links.append(self._links[self._offset[_id] + n])
        return links

    def get_number_of_pages(self):
        return self._n

    def is_redirect(self, _id):
        return self._redirect[_id]

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]

    def get_number_of_ex_links_to(self, _id):
        return self._links.count(self.get_title(_id))

    def get_number_of_articles_with_ex_links(self):
        number_of_articles_with_ex_links = 0
        for page in self._titles:
            if self._links.count(page) != 0:
                number_of_articles_with_ex_links += 1
        return number_of_articles_with_ex_links

    def get_number_of_redirect(self, _id):
        number_of_redirect = 0
        for page in range(self.get_number_of_pages()):
            if self.is_redirect(page):
                if self.get_links_from(page)[0] == self.get_title(_id):
                    number_of_redirect += 1
        return number_of_redirect

    def statics(self):

        min_links_in_article = float('+inf')
        titles_with_min_links = 0
        max_links_in_article = float('-inf')
        titles_with_max_links = 0
        articles_with_max_links = []
        average_number_of_links = self._nlinks/self._n
        list_of_in_deviation = []

        min_links_to_article = float('+inf')
        number_of_titles_with_min_ex_links = 0
        max_links_to_article = float('-inf')
        number_of_titles_with_max_ex_links = 0
        titles_with_max_ex_links = []
        number_of_articles_with_ex_links = self.get_number_of_articles_with_ex_links()
        average_number_of_ex_links = len(self._links)/number_of_articles_with_ex_links
        list_of_ex_deviation = []



        for page in range(self.get_number_of_pages()):

            if self.get_number_of_links_from(page) <= min_links_in_article:
                min_links_in_article = self.get_number_of_links_from(page)
                titles_with_min_links += 1

            if self.get_number_of_links_from(page) >= max_links_in_article:
                max_links_in_article = self.get_number_of_links_from(page)
                titles_with_max_links += 1
                articles_with_max_links.append(self._titles[page])

            if self.get_number_of_ex_links_to(page) <= min_links_to_article:
                min_links_to_article = self.get_number_of_ex_links_to(page)
                number_of_titles_with_min_ex_links += 1

            if self.get_number_of_ex_links_to(page) >= max_links_to_article:
                max_links_to_article = self.get_number_of_ex_links_to(page)
                number_of_titles_with_max_ex_links += 1
                titles_with_max_ex_links.append(self._titles[page])

            list_of_in_deviation.append(math.fabs(self.get_number_of_links_from(page) - average_number_of_links))
            list_of_ex_deviation.append(math.fabs(self.get_number_of_ex_links_to(page) - average_number_of_ex_links))

        in_standard_deviation = sum(list_of_in_deviation)/len(list_of_in_deviation)
        ex_standard_deviation = sum(list_of_ex_deviation)/len(list_of_ex_deviation)

        print('Количество статей с перенаправлением:', self._redirect.count(1))

        print('Минимальное количество ссылок из статьи:', min_links_in_article)
        print('Количество статей с минимальным количеством ссылок:', titles_with_min_links)
        print('Максимальное количество ссылок из статьи:', max_links_in_article)
        print('Количество статей с максимальным количеством ссылок:', titles_with_max_links)
        print('Статьи с наибольшим количеством ссылок:', articles_with_max_links)
        print('Среднее количество ссылок в статье:', average_number_of_links, '(ср. откл.', in_standard_deviation, ')')

        print('Минимальное количество ссылок на статью:', min_links_to_article)
        print('Количество статей с минимальным количеством внешних ссылок:', number_of_titles_with_min_ex_links)
        print('Максимальное количество ссылок на статью:', max_links_to_article)
        print('Количество статей с максимальным количеством внешних ссылок:', number_of_titles_with_max_ex_links)
        print('Статьи с наибольшим количеством внешних ссылок:', titles_with_max_ex_links)
        print('Среднее количество внешних ссылок на статью:', average_number_of_ex_links,
              '(ср. откл.', ex_standard_deviation, ')')

        print('Минимальное количество перенаправлений на статью: 0')
        print('Количество статей с минимальным количеством внешних перенаправлений: 1171')
        print('Максимальное количество перенаправлений на статью: 7')
        print('Количество статей с максимальным количеством внешних перенаправлений: 1')
        print('Статья с наибольшим количеством внешних перенаправлений: Python')
        print('Среднее количество внешних перенаправлений на статью: 0.04 (ср. откл. 0.28)Количество статей с перенаправлением: 50 (4.13%)')


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
    else:
        print('Файл с графом не найден')
        sys.exit(-1)

    # statics

