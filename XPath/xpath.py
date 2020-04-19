from lxml import html
import requests
from datetime import datetime, timedelta
from pprint import pprint

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

def req_to_lenta():
    main_link = 'https://lenta.ru'
    response = requests.get(main_link, headers=header)
    root = html.fromstring(response.text)
    items = root.xpath("//div[@class='span4']/div[@class='item']")
    list_news = []

    for item in items:
        dict_news = {}
        dict_news['link'] = main_link+str(item.xpath("./a/@href")[0])
        dict_news['title'] = item.xpath("./a/text()")[0].replace('\xa0', ' ')
        dict_news['time'] = item.xpath("./a/time/@datetime")[0]
        dict_news['source'] = 'Lenta.ru'
        list_news.append(dict_news)

    return list_news

def req_to_yandex():
    main_link = 'https://yandex.ru'
    response = requests.get(main_link+'/news', headers=header)
    root = html.fromstring(response.text)
    items = root.xpath("//div[@class='story__topic']")
    list_news = []

    for item in items:
        dict_news = {}
        dict_news['link'] = main_link + str(item.xpath("./h2/a/@href")[0])
        dict_news['title'] = item.xpath("./h2/a/text()")[0]
        text = item.xpath("./../div[@class='story__info']/div[@class='story__date']/text()")[0].replace('\xa0', ' ')
        text_list = text.split(' ')
        if 'вчера' in text_list:
            dict_news['time'] = text_list[-1] + ', ' + (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')
            index = text_list.index('вчера')
        else:
            dict_news['time'] = text_list[-1] + ', ' + datetime.now().strftime('%d.%m.%Y')
            index = len(text_list)-1

        source = text_list[0]
        for elem in text_list[1:index]:
            source += f' {elem}'
        dict_news['source'] = source
        list_news.append(dict_news)

    return list_news

def req_to_mail():
    main_link = 'https://news.mail.ru/'
    response = requests.get(main_link, headers=header)
    root = html.fromstring(response.text)
    links_list = []
    links_list += root.xpath("//a[@class='newsitem__title link-holder']/@href")
    #links_list += root.xpath("//a[@class='link link_flex']/@href")
    #links_list += root.xpath("//a[@class='photo photo_full photo_scale js-topnews__item']/@href")
    #links_list += root.xpath("//a[@class='photo photo_small photo_scale photo_full js-topnews__item']/@href")
    #links_list += root.xpath("//a[@class='list__text']/@href")
    list_news = []

    for link in links_list:
        dict_news = {}
        if 'mail' in link:
            response = requests.get(link, headers=header)
            dict_news['link'] = link
        else:
            response = requests.get(main_link+link[1:], headers=header)
            dict_news['link'] = main_link+link[1:]
        root = html.fromstring(response.text)
        dict_news['title'] = root.xpath("//h1[@class='hdr__inner']/text()")[0]
        time_text = root.xpath("//span[@class='note__text breadcrumbs__text js-ago']/text()")
        time_list = time_text[0].split(' ')
        if time_list[0].isdigit():
            dict_news['time'] = time_text[0] + ' ' + datetime.now().strftime('%Y')
        else:
            dict_news['time'] = time_list[0] + ', ' + datetime.now().strftime('%d.%m.%Y')

        dict_news['source'] = root.xpath("//span[@class='note']/a/span[@class='link__text']/text()")[0]

        list_news.append(dict_news)


        #    print(link)

    return list_news

#pprint(req_to_lenta())

#pprint(req_to_yandex())

#pprint(req_to_mail())