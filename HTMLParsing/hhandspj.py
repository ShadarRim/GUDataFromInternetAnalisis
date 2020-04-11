from pprint import pprint
from bs4 import BeautifulSoup as bs
import re
import requests
import pandas as pd

def search_sj(keyword):
    sj_link = 'https://www.superjob.ru/'
    response = requests.get(f'{sj_link}/vacancy/search/?keywords={keyword}')
    i = 0
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
                if sal.text == 'По договорённости':
                    dict['sal_min'] = None
                    dict['sal_max'] = None
                    dict['sal_cur'] = None
                else:
                    sal_list = re.findall("\d+", sal.text)
                    if len(re.findall("от", sal.text)):
                        dict['sal_min'] = sal_list[0] if len(sal_list) == 1 else sal_list[0] + sal_list[1]
                        dict['sal_max'] = None
                    elif (len(re.findall("до", sal.text))):
                        dict['sal_min'] = None
                        dict['sal_max'] = sal_list[0] if len(sal_list) == 1 else sal_list[0] + sal_list[1]
                    elif (len(re.findall("—", sal.text))):
                        if len(sal_list) == 4:
                            dict['sal_min'] = sal_list[0] + sal_list[1]
                            dict['sal_max'] = sal_list[2] + sal_list[3]
                        elif len(sal_list) == 3:
                            dict['sal_min'] = sal_list[0]
                            dict['sal_max'] = sal_list[1] + sal_list[2]
                        else:
                            dict['sal_min'] = sal_list[0]
                            dict['sal_max'] = sal_list[1]
                    else:
                        dict['sal_min'] = sal_list[0] if len(sal_list) == 1 else sal_list[0] + sal_list[1]
                        dict['sal_max'] = sal_list[0] if len(sal_list) == 1 else sal_list[0] + sal_list[1]

                    if re.findall("руб", sal.text):
                        dict['sal_cur'] = "Rub"
                    else:
                        dict['sal_cur'] = "Not Rub"
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
        # print(hh_vac_block)
        hh_vac_list = hh_vac_block[0].find_all('div',
                                               {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'}) + \
                      hh_vac_block[0].find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
        # vacancy-serp__vacancy

        for elem in hh_vac_list:
            dict = {}

            dict['name'] = elem.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0].text
            dict['link'] = elem.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0]['href']

            sal_text = elem.find_all('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'})
            if len(sal_text) == 1:
                dict['sal_min'] = None
                dict['sal_max'] = None
                dict['sal_cur'] = None
            else:
                sal_text = sal_text[1].text
                sal_list = re.findall("\d+", sal_text)

                if len(re.findall("от", sal_text)):
                    dict['sal_min'] = sal_list[0] if len(sal_list) == 1 else sal_list[0] + sal_list[1]
                    dict['sal_max'] = None
                elif (len(re.findall("до", sal_text))):
                    dict['sal_min'] = None
                    dict['sal_max'] = sal_list[0] if len(sal_list) == 1 else sal_list[0] + sal_list[1]
                elif (len(re.findall("-", sal_text))):
                    if len(sal_list) == 4:
                        dict['sal_min'] = sal_list[0] + sal_list[1]
                        dict['sal_max'] = sal_list[2] + sal_list[3]
                    elif len(sal_list) == 3:
                        dict['sal_min'] = sal_list[0]
                        dict['sal_max'] = sal_list[1] + sal_list[2]
                    else:
                        dict['sal_min'] = sal_list[0]
                        dict['sal_max'] = sal_list[1]
                else:
                    dict['sal_min'] = sal_list[0] if len(sal_list) == 1 else sal_list[0] + sal_list[1]
                    dict['sal_max'] = sal_list[0] if len(sal_list) == 1 else sal_list[0] + sal_list[1]

                if re.findall("руб", sal_text):
                    dict['sal_cur'] = "Rub"
                elif re.findall("грн", sal_text):
                    dict['sal_cur'] = "Grn"
                elif re.findall('EUR', sal_text):
                    dict['sal_cur'] = 'EUR'
                elif re.findall('USD', sal_text):
                    dict['sal_cur'] = 'USD'
                else:
                    dict['sal_cur'] = 'Nor Rub'

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

print(pd.DataFrame(vac_list))

