from bs4 import BeautifulSoup
import requests
import os
import sys
import time
import json
import ast
import copy


all_names = []
name_mini = {}


os.chdir(os.path.dirname(__file__))
current_dir = os.getcwd()


os.makedirs(current_dir + "/images", exist_ok = True)
os.makedirs(current_dir + "/JSON", exist_ok = True)


VSUET_SITE = "https://vsuet.ru"
VSUET_APP_TEACHERS = "https://vsuet.app/api/schedule/teachers"
VSUET_CHAIRS = "https://vsuet.ru/obuchenie/chairs"
VSUET_IMG_ANON = "https://vsuet.ru/images/user-def.png"


r_api = requests.get(VSUET_APP_TEACHERS)
soup_api = BeautifulSoup(r_api.content, features="html.parser")
api_all_prepod = soup_api.get_text()
r_api.close()


def get_all_caf():
    r = requests.get(VSUET_CHAIRS)
    soup = BeautifulSoup(r.content, features="html.parser")
    div = soup.find('div', {'itemprop': 'articleBody'})
    cafdr = []
    children = div.find_all("a")
    r.close()
    for child in children:
        cafdr.append(VSUET_SITE + child.get("href"))
    
    for i in range(len(cafdr)):
        try:
            if i == 2 or i == 10:
                cafdr[i] = cafdr[i].replace(VSUET_SITE, "")
            r = requests.get(cafdr[i])
            soup = BeautifulSoup(r.content, features="html.parser")
            a1 = soup.find("ul", {"class": "aside__menu nav flex-column"})
            a2 = a1.select_one(":nth-child(2)")
            n_of_i = 0
            if i == 2 or i == 10:
                a_str = a2.find("a", {"class": "nav-link"}).get("href")
                n_of_i = 1
            else:
                a_str = VSUET_SITE + a2.find("a", {"class": "nav-link"}).get("href")
            sotr_k(a_str, api_all_prepod, n_of_i)
            r.close()
        except:
            continue

def sotr_k(a_str, api_all_prepod, n_of_i):
    r = requests.get(a_str)
    soup_sotr = BeautifulSoup(r.content, features="html.parser")
    if n_of_i == 0:
        block_w_img = soup_sotr.find('div', {'class': 'content cat_chair staff'})
        alls = soup_sotr.find_all("a", {"class": "person-name"})
    else:
        block_w_img = soup_sotr.find('div', {'class': 'elementor-section-wrap'})
        alls_m = soup_sotr.find_all("h4", {"class": "elementor-image-box-title"})
        alls = []
        for ba in alls_m:
            alls.append(ba.find("a"))
    count_for_img = -1
    for b in alls:
        count_for_img += 1
        b_str = b.get_text()
        name_un = str(' '.join(b_str.split()))
        name_for_api = name_un[:]
        name_changer(name_for_api, api_all_prepod, count_for_img, block_w_img, n_of_i)


def find_img(count_for_img, block_w_img, n_of_i):
    a_img = block_w_img.select('img')[count_for_img]
    if n_of_i == 0:
        link = VSUET_SITE + "/" + a_img['src']
    else:
        link = a_img['src']
    name_img = name_mini["fullEnName"].replace(" ", "_").replace(".", "") + ".jpg"
    cr_pa = "/images" + "/" + name_img
    papka_w_img = current_dir + "/images" + "/" + name_img
    with open(papka_w_img, "wb") as file:
        im = requests.get(link)
        file.write(im.content)
        im.close()
    name_mini["image"] = cr_pa
    all_names.append(name_mini.copy())
    
def name_changer(name_for_api, api_all_prepod, count_for_img, block_w_img, n_of_i):
    name_for_api = name_for_api.split()
    name_for_api_ch = name_for_api[0].lower().capitalize() + " " + name_for_api[1][0] + "." + name_for_api[2][0] + "."
    if name_for_api_ch in api_all_prepod:
        name_mini["shortName"] = name_for_api_ch
        name_mini["fullRuName"] = ' '.join(name_for_api[0:3]).lower().title()
        name_mini["fullEnName"] = ' '.join(name_for_api[-3:])
        find_img(count_for_img, block_w_img, n_of_i)


def miss_api():
    api_all_prepod = soup_api.get_text()
    soup_a = str(soup_api)
    api_data = ast.literal_eval(soup_a)
    copy_of_all_names = all_names.copy()
    a_ar1 = []
    a_ar2 = []
    for i in copy_of_all_names:
        a_ar2.append(i["shortName"])
    for j in api_data["data"]:
        a_ar1.append(j["shortName"])
    to_change = set(a_ar1).symmetric_difference(set(a_ar2))
    with open(current_dir + "/images/user-def.png", "wb") as file:
        im = requests.get(VSUET_IMG_ANON)
        file.write(im.content)
        im.close()
    for i in to_change:
        name_mini["shortName"] = i
        name_mini["fullRuName"] = i
        name_mini["fullEnName"] = i
        name_mini["image"] = "/images/user-def.png"
        all_names.append(name_mini.copy())


def del_duplicates():
    return list({ each["shortName"] : each for each in all_names }.values())


def create_json():
    unique = del_duplicates()
    path_for_json = current_dir + "/JSON/teachers.json"
    with open(path_for_json, "w", encoding='utf-8') as file:
        json.dump(unique, file, ensure_ascii=False, indent=4)


get_all_caf()
miss_api()
create_json()