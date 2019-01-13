import asyncio
import grequests
from bs4 import BeautifulSoup as bs
from sql_worker import sql_work

#глобальная переменная для хранения готовых результатов на запись
list_tasks = {}

def exception_handler(request, exception):
    print(exception)

async def parse_page(data, url):
    try:
        soup = bs(data, 'lxml')
        find_bs4 = soup.find('title') #пример тега для парсинга
        list_tasks.update({url:find_bs4.text.strip()})
    except AttributeError:
        print(url, 'has no text!')

async def main():
    #Page list может быть получен, например из базы (например, если пользователи загружают списки страниц для сбора с них данных)
    page_list = [
            'http://www.omax.ru',
            'http://www.akkond.ru',
            'http://www.trudeks.ru',
            'http://www.ppot.ru',
            'http://www.oaomoek.ru',
            'http://www.lottehotelvladivostok.com',
            'http://tavrida.com',
            'http://www.boesconstruction.com/',
            'https://ecocity26.ru',
            'http://www.oilgazholding.ru',
            'http://www.gelar.ru',
            'http://www.krasnoe-beloe.ru',
            'http://rabota.polyusgold.com',
            'http://www.tbm.ru',
            'http://www.metadynea.ru',
            'http://rabota.leroymerlin.ru',
            'http://www.colvir.com',
            'http://www.badenelit.org',
            'http://www.pulkovo-cargo.ru',
            'http://www.niva.su',
            'http://www.mkm.ru',
            'http://volga-ice.ru',
            'http://www.rabotavamrest.ru',
            'http://www.kareliaupofloor.ru',
            'http://www.ontexglobal.com/',]

    rs = []
    for p in page_list:
        rs.append(grequests.get(p, timeout=10))

    iter_rs = grequests.imap(rs, size=len(page_list), exception_handler=exception_handler)


    for page in iter_rs:
        task = asyncio.create_task(parse_page(page.text, page.url))
        await asyncio.gather(task)

if __name__ == '__main__':
    asyncio.run(main())
    sql_work(list_tasks)