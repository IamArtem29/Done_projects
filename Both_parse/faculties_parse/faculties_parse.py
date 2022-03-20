# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import os
import sys
import copy


SITE = "https://vsuet.ru/obuchenie/faculties"
r = requests.get(SITE)
soup = BeautifulSoup(r.content, features="html.parser")


faculties = []
all_a = soup.find_all(class_ = "box-service__item")
for el in soup.find_all('div', class_ = "box-service__title"):
    faculties.append(el.get_text())

all_faculties = []
number = -1

for i in all_a:
    number += 1
    fac = {}
    fac["name"] = faculties[number]
    i_url = "https://vsuet.ru" + i.get("href")
    r = requests.get(i_url)
    soup = BeautifulSoup(r.content, features="html.parser")
    decan = {}
    decan["fullName"] = soup.find(class_ = "dept-info__h-name").text
    decan['job'] = "Декан"
    decan['degree'] = soup.find(class_ = "dept-info__h-degree").text
    decan['image'] = soup.find(class_ = "img-thumbnail")['src']
    fac["decan"] = decan
    sotrs = []
    all_mem = soup.find_all(class_ = "persons__item")

    for i in all_mem:
        sotr = {}
        sotr["fio"] = i.find(class_ = "persons__info").find(class_ = "fio").text.strip()
        sotr["dolzhn"] = i.find(class_ = "persons__info").find(class_ = "dolzhn").text
        sotr["regal"] = i.find(class_ = "persons__info").find(class_ = "regal").text.strip()
        sotr['image'] =  i.find(class_ = "persons__img person__img_br_50").find(class_ = "img-thumbnail")['src']
        sotrs.append(sotr)

    fac["members"] = sotrs
    contacts = {}
    contacts['tel'] = soup.find(class_ = "fas fa-phone").next_element.next_element.text.split(',\r\n')
    contacts['address'] = soup.find(class_ = "fas fa-map-marker").next_element.next_element.text
    fac["contacts"] = contacts

    if fac["name"] == 'Экология и химическая технология ':
        alls = soup.find_all("b")
        spe =["бакалавриат", "специалитет", "магистратура", "аспирантура"]
        cout = 0
        speco = {}
        speco_large = []
        all_speco = []
        speccc = ""

        for jaja in alls:
            cout += 1
            if jaja.next_element in soup.find_all("font"):
                xaxaxa = ' '.join(jaja.next_element.next_element.next_element.next_element.split())
            else:
                xaxaxa = ' '.join(jaja.next_element.split())

            if xaxaxa not in spe:
                xaxaxaxa = jaja.next_element.next_element.split()
                name_speccc = " ".join(xaxaxaxa)
            else:
                if speco_large != []:
                    if cout == 5:
                        speco["name"] = "бакалавриат"
                        speco["table"] = speco_large
                        all_speco.append(speco.copy())
                    elif cout == 8:
                        speco["name"] = "специалитет"
                        speco["table"] = speco_large
                        all_speco.append(speco.copy())
                    elif cout == 12:
                        speco["name"] = "магистратура"
                        speco["table"] = speco_large
                        all_speco.append(speco.copy())
                    else:
                        speco["name"] = "аспирантура"
                        speco["table"] = speco_large
                        all_speco.append(speco.copy())
                speco_large = []
                continue

            code_speccc = xaxaxa
            if (cout == 6) or (cout == 7):
                prof_speccc = jaja.next_element.next_element.next_element.next_element.next_element.next_element.next_element
            else:
                prof_speccc = jaja.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element
            speco_mini = {}
            speco_mini["code_speccc"] = code_speccc
            speco_mini["name_speccc"] = name_speccc
            speco_mini["prof_speccc"] = prof_speccc
            speco_large.append(copy.copy(speco_mini))
        speco["name"] = "аспирантура"
        speco["table"] = speco_large
        all_speco.append(copy.copy(speco))
        fac["specialization"] = all_speco
    else:
        alla = []
        all_h4 = soup.find_all(class_ = "block-heading mt-0 mb-3")
        if all_h4 == []:
            all_h4 = soup.find_all(class_ = "my-3 h5 text-center")
            for h in all_h4:
                ha = h.text
                if "Направление" in ha or "Направления" in ha:
                    alla.append(ha)
        else:
            for h in all_h4:
                ha = h.find("span").text
                if "Направление" in ha or "Направления" in ha:
                    alla.append(ha)
        if alla == [] and soup.find_all(class_ = "my-3 h5 text-center") != []:
            all_h4 = soup.find_all(class_ = "my-3 h5 text-center")
            for h in all_h4:
                ha = h.find("span").text
                if "Направление" in ha or "Направления" in ha:
                    alla.append(ha)
        elif alla == [] and soup.find_all("h5",{"class": "text-center"}) != []:
            all_h4 = soup.find_all("h5", class_ = "text-center")
            for h in all_h4:
                ha = h.find("span").text
                if "Направление" in ha or "Направления" in ha:
                    alla.append(ha)
        speco = {}
        specos = []
        all_speco = []
        stop = len(alla)
        counte = -1
        if (soup.find_all(class_ = "table table-bordered") == []) and (soup.find_all(class_ = "table table-bordered table-hover fs-16") != []):
            for gub in soup.find_all(class_ = "table table-bordered table-hover fs-16"):
                counte += 1
                if counte == stop:
                    break
                speco["name"] = alla[counte]
                napr_s = alla[counte]
                gub_sub = gub.find_all("tbody")
                for sub in gub_sub:
                    for sub_sub in sub.find_all("tr"):
                        spec_mini = {}
                        spec_mini["id"] = sub_sub.find_all('td')[0].text
                        spec_mini["name"] = sub_sub.find_all('td')[1].text
                        spec_mini["profiles"] = sub_sub.find_all('td')[2].text.rstrip().replace("\n", " ")
                        specos.append(copy.copy(spec_mini))
                    speco['table'] = specos
                    specos = []
                all_speco.append(copy.copy(speco))
            fac["specialization"] = all_speco
        elif (soup.find_all(class_ = "table table-bordered") == []) and (soup.find_all(class_ = "table table-bordered fs-16") != []):
            for gub in soup.find_all(class_ = "table table-bordered fs-16"):
                counte += 1
                if counte == stop:
                    break
                speco["name"] = alla[counte]
                napr_s = alla[counte]
                gub_sub = gub.find_all("tbody")
                for sub in gub_sub:
                    for sub_sub in sub.find_all("tr"):
                        spec_mini = {}
                        spec_mini["id"] = sub_sub.find_all('td')[0].text
                        spec_mini["name"] = sub_sub.find_all('td')[1].text
                        spec_mini["profiles"] = sub_sub.find_all('td')[2].text.rstrip().replace("\n", " ")
                        specos.append(copy.copy(spec_mini))
                    speco['table'] = specos
                    specos = []
                all_speco.append(copy.copy(speco))
            fac["specialization"] = all_speco
        else:
            for gub in soup.find_all(class_ = "table table-bordered"):
                counte += 1
                if counte == stop:
                    break
                speco["name"] = alla[counte]
                napr_s = alla[counte]
                gub_sub = gub.find_all("tbody")
                for sub in gub_sub:
                    for sub_sub in sub.find_all("tr"):
                        spec_mini = {}
                        spec_mini["id"] = sub_sub.find_all('td')[0].text
                        spec_mini["name"] = sub_sub.find_all('td')[1].text
                        spec_mini["profiles"] = sub_sub.find_all('td')[2].text.rstrip().replace("\n", " ")
                        specos.append(copy.copy(spec_mini))
                    speco['table'] = specos
                    specos = []
                all_speco.append(copy.copy(speco))
            fac["specialization"] = all_speco

    a = -1
    cafd = soup.find(class_ = "aside aside-left sticky-top").find_all(class_ = "nav-link")
    li_ca = {}
    all_li = []
    
    for ar in cafd:
        a += 1
        if "Кафедра" not in ar.get_text():
            del cafd[a:]
            break
        else:
            li_ca["name"] = ar.get_text()
            li_ca["hyper"] = "https://vsuet.ru/" + ar['href']
            cafd[a] = ar
            all_li.append(copy.deepcopy(li_ca))
    fac["cafedr"] = all_li
    all_faculties.append(fac)

def to_json(all_faculties):
    with open(os.path.join(sys.path[0], "all_faculties.json"), "w", encoding='utf-8') as f:
        json.dump(all_faculties, f, ensure_ascii=False, indent=4)

to_json(all_faculties)