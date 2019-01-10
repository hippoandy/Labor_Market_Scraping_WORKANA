''' general purpose multi-threading web scraper

Author: Xin Jin
'''

import threading
import textwrap
import queue
import os

import requests

from utils import write_to_json

class Scraper():
    ''' multi-threading scraper '''
    def __init__(self, name='scrape', concurrent=500, base='./data', \
                 timeout=30, parse_func=lambda res: res.text):
        '''\
            name: job name, prefix for all data files
            url_lst: all urls to scrape
            res_tmp_lst: temporarily holds response object for urls in url_lst
            parse_func: parsing function, provided by user

            data_base: base directory for all data
            data_path: path for data
            scrape_err_path: path for scrape errors
            parse_err_path: path for parse errors

            job_queue: thread-safe synchronized queue
            cond: Lock for synchronized variable read/write
            concurrent: number of threads
            timeout: timeout for each request
            job_finished: tracking scraping progress

            data_lst: final data, after scraping, all data should be here
            scrape_err_lst: scrape errors, [{'url': <failed url>, 'err': <error msg>}]
            parse_err_lst: parsing errors, [{'url': <failed url>, 'err': <error msg>}]
        '''
        self.name = name
        self.url_lst = []
        self.res_tmp_lst = []
        self.parse_func = parse_func

        self.data_base = base
        self.data_path = os.path.join(self.data_base, f'{name}.json')
        self.scrape_err_path = os.path.join(self.data_base, f'{name}_scrape_err.json')
        self.parse_err_path = os.path.join(self.data_base, f'{name}_parse_err.json')

        self.job_queue = queue.Queue()
        self.cond = threading.Lock()
        self.concurrent = concurrent
        self.timeout = timeout
        self.job_finished = 0

        self.data_lst, self.scrape_err_lst, self.parse_err_lst = [], [], []

    def urls(self, url_lst_to_add):
        ''' consume url list passed by user '''
        if not self.url_lst:
            self.url_lst = url_lst_to_add
        elif self.url_lst:
            self.url_lst.extend(url_lst_to_add)
        return self

    def parse(self, parse_func):
        ''' comsume parsing function passed by user '''
        self.parse_func = parse_func
        return self

    def run_until_done(self):
        ''' run until no scrape_err_lst or parse_err_lst or stuck '''
        self._spawn_threads()
        pre_url_lst_sorted = None
        self.job_finished = 0
        while self.url_lst or self.scrape_err_lst or self.parse_err_lst:
            if self.scrape_err_lst:
                self.url_lst.extend(list(map(lambda x: x['url'], self.scrape_err_lst)))
            if self.parse_err_lst:
                self.url_lst.extend(list(map(lambda x: x['url'], self.parse_err_lst)))
            if pre_url_lst_sorted and sorted(self.url_lst) == pre_url_lst_sorted:
                self._save()
                print(textwrap.dedent(f'''\
                    stuck, please check scrape_err or parse_err
                    saved result:
                        len(data_lst): {len(self.data_lst)}
                        len(scrape_err_lst): {len(self.scrape_err_lst)}
                        len(parse_err_lst): {len(self.parse_err_lst)}
                '''))
                return
            pre_url_lst_sorted = sorted(self.url_lst)

            self.scrape_err_lst.clear()
            self.parse_err_lst.clear()
            print(f'loop started with len(url_lst): {len(self.url_lst)}')
            for url in self.url_lst:
                self.job_queue.put(url)
            self.job_queue.join()
            self.url_lst = []
            self._parse()
            self.res_tmp_lst = []
            self.job_finished = 0

        self._save()
        print(textwrap.dedent(f'''\
            finished
            saved result:
                len(data_lst): {len(self.data_lst)}
                len(scrape_err_lst): {len(self.scrape_err_lst)}
                len(parse_err_lst): {len(self.parse_err_lst)}
        '''))

    # def run(self):
    #     # TODO
    #     self._spawn_threads()
    #     # scrape
    #     for url in self.url_lst:
    #         self.job_queue.put(url)
    #     job_queue.join()
    #     # parse
    #     self._parse()
    #     self._ask_save()
    #
    # def _ask_save():
    #     # TODO
    #     print(f'len(res_tmp_lst): {len(res_tmp_lst)}')
    #     print(f'len(scrape_err_lst): {len(res_tmp_lst)}')
    #     usr_input = None
    #     while not (usr_input == 'discard' or usr_input == 'save'):
    #         usr_input = input('save this result? (discard/save)').strip()
    #         if usr_input == 'discard':
    #             break
    #         elif usr_input == 'save':
    #             write_to_json(f'{self.name}_data.json', self.data_lst)
    #             write_to_json(f'{self.name}_scrape_err.json', self.scrape_err_lst)
    #             write_to_json(f'{self.name}_parse_err.json', self.parse_err_lst)

    def _save(self):
        ''' save final data. data_lst, scrape_err_lst, parse_err_lst '''
        write_to_json(self.data_path, self.data_lst)
        write_to_json(self.scrape_err_path, self.scrape_err_lst)
        write_to_json(self.parse_err_path, self.parse_err_lst)

    def _job(self):
        ''' job for each thread '''
        while True:
            url = self.job_queue.get()
            try:
                res = requests.get(url, timeout=self.timeout)
                self.cond.acquire()
                self.res_tmp_lst.append(res)
            except Exception as err:
                self.cond.acquire()
                self.scrape_err_lst.append({'url': url, 'err': str(err)})
            finally:
                self.job_finished += 1
                print(f'process: {100 * self.job_finished / len(self.url_lst):.2f}%', end='\r')
                self.cond.release()
                self.job_queue.task_done()

    def _spawn_threads(self):
        ''' start threads as daemons '''
        for _ in range(0, self.concurrent):
            thread = threading.Thread(target=self._job)
            thread.daemon = True
            thread.start()

    def _parse(self):
        ''' parse res using parse_func '''
        for res in self.res_tmp_lst:
            try:
                data = self.parse_func(res)
                self.data_lst.append(data)
            except Exception as err:
                self.parse_err_lst.append({'url': res.url, 'err': str(err)})

if __name__ == '__main__':
    # sample for bumeran in Chile aka laborum
    URL_LST = []
    URL_BASE = 'https://www.laborum.cl/empleos-categoria-educacion-pagina-{}.html'
    for pg_num in range(1, 101):
        URL_LST.append(URL_BASE.format(pg_num))
    # false case
    URL_LST.extend(['www', 'htt://www.google.com', 'https://www.gggempleos-categoria-.com'])

    Scraper(name='bumeran_chile', concurrent=200, timeout=1)\
        .urls(URL_LST).parse(lambda x: x.text).run_until_done()

    # Scraper(name='bumeran_chile', concurrent=200, timeout=1)\
    #     .urls(URL_LST).parse(lambda x: x.text).run_max_loop(max_loop=100)

    # Scraper(name='bumeran_chile', concurrent=200, timeout=1)\
    #     .urls(URL_LST).parse(lambda x: x.text).run_interactive()