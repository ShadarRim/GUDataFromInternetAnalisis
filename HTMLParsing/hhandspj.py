from pprint import pprint
from bs4 import BeautifulSoup as bs
import re
import requests
import pandas as pd

def search_sj(keyword):
    sj_link = 'https://www.superjob.ru/'
    response = requests.get(f'{sj_link}/vacancy/search/?keywords={keyword}')
    sj_vac_parse_list = []

    while True:
        if not response.ok:
            break
        response = response.text
        soup = bs(response, 'lxml')
        sj_vac_block = soup.find_all('div', {'class': '_3zucV undefined'})
        sj_vac_list = sj_vac_block[1].find_all('div', {'class': 'iJCa5 _2gFpt _1znz6 _2nteL'})

        for elem in sj_vac_list:
            dict = {}
            next = elem.find_all('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})
            if next:
                dict['name'] = next[0].find('a').text
                dict['link'] = sj_link + next[0].find('a')['href']
                dict['source'] = 'sj'
                sal = elem.find_all('span', {
                    'class': '_3mfro _2Wp8I _31tpt f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})[0]

                dict['sal_min'] = ''
                dict['sal_max'] = ''
                dict['sal_cur'] = ''

                sal_list = sal.text.split("\xa0")
                if 'от' in sal_list:
                    for elem in sal_list[1:len(sal_list)-1]:
                        dict['sal_min'] += elem
                elif 'до' in sal_list:
                    for elem in sal_list[1:len(sal_list)-1]:
                        dict['sal_max'] += elem
                elif '—' in sal_list:
                    pos = sal_list.index('—')
                    for elem in sal_list[:pos]:
                        dict['sal_min'] += elem
                    for elem in sal_list[pos+1:len(sal_list)-1]:
                        dict['sal_max'] += elem
                else:
                    for elem in sal_list[1:len(sal_list)-1]:
                        dict['sal_min'] += elem
                        dict['sal_max'] += elem

                dict['sal_min'] = None if dict['sal_min'] == '' else dict['sal_min']
                dict['sal_max'] = None if dict['sal_max'] == '' else dict['sal_max']
                dict['sal_cur'] = None if 'По договорённости' in sal_list else sal_list[-1]
            else:
                continue
            sj_vac_parse_list.append(dict)

        next_step = soup.find_all('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})
        if not next_step:
            break
        response = requests.get(f"{sj_link}{next_step[0]['href']}")

    return sj_vac_parse_list

def search_hh(keyword):
    hh_link = 'https://hh.ru'

    usag = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'

    response = requests.get(f'{hh_link}/search/vacancy?st=searchVacancy&text={keyword}', headers={'User-Agent': usag})
    hh_vac_parce_list = []
    while True:
        soup = bs(response.text, 'lxml')
        hh_vac_block = soup.find_all('div', {'class': 'vacancy-serp'})
        hh_vac_list = hh_vac_block[0].find_all('div',
                                               {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'}) + \
                      hh_vac_block[0].find_all('div', {'data-qa': 'vacancy-serp__vacancy'})

        for lelem in hh_vac_list:
            dict = {}

            dict['name'] = lelem.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0].text
            dict['link'] = lelem.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0]['href']
            dict['source'] = 'hh'

            sal = lelem.find_all('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'})

            if len(sal) == 1:
                dict['sal_min'] = None
                dict['sal_max'] = None
                dict['sal_cur'] = None
            else:
                dict['sal_min'] = ''
                dict['sal_max'] = ''
                dict['sal_cur'] = ''
                spec_sal = sal[1].text
                spec_sal = spec_sal.replace(' ', "\xa0")
                spec_sal = spec_sal.replace('-', "\xa0-\xa0")

                sal_list = spec_sal.split("\xa0")

                if 'от' in sal_list:
                    for elem in sal_list[1:len(sal_list) - 1]:
                        dict['sal_min'] += elem
                elif 'до' in sal_list:
                    for elem in sal_list[1:len(sal_list) - 1]:
                        dict['sal_max'] += elem
                elif '-' in sal_list:
                    pos = sal_list.index('-')
                    for elem in sal_list[:pos]:
                        dict['sal_min'] += elem
                    for elem in sal_list[pos + 1:len(sal_list) - 1]:
                        dict['sal_max'] += elem
                else:
                    for elem in sal_list[1:len(sal_list) - 1]:
                        dict['sal_min'] += elem
                        dict['sal_max'] += elem

                dict['sal_min'] = None if dict['sal_min'] == '' else dict['sal_min']
                dict['sal_max'] = None if dict['sal_max'] == '' else dict['sal_max']
                dict['sal_cur'] = None if 'По договорённости' in sal_list else sal_list[-1]

            hh_vac_parce_list.append(dict)

        next = soup.find_all('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if next:
            next = next[0]['href']
        else:
            break
        response = requests.get(f'{hh_link}{next}', headers={'User-Agent': usag})
    return hh_vac_parce_list




keyword = 'python'
vac_list = search_sj(keyword) + search_hh(keyword)
#pprint(vac_list)

print(pd.DataFrame(vac_list))

