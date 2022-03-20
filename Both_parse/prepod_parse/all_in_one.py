#!/usr/bin/env python
# coding: utf-8

# ## IMPORT

# In[1]:
import os
import sys

import pandas as pd
import numpy as np

import traceback
import json


# In[2]:


df_all_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
df_all_teacher = pd.DataFrame(columns = ["id", "teacherName"])


# In[3]:


df_tp_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
df_tp_teacher = pd.DataFrame(columns = ["id", "teacherName"])


# In[4]:

df_sheet_all = pd.read_excel((os.path.join(sys.path[0], r"rasp\unmer", "eht_unmer.xlsx")), sheet_name=None)

sheet_n = 0

for i in df_sheet_all:
    sheet_n += 1
    df_re = df_sheet_all[i]
    df_re = df_re.drop(df_re.index[[0, 1, 2, 3, 4]])
    df_re = df_re.rename(columns=df_re.iloc[0])
    df_re = df_re.drop(df_re.index[[0, -1, -2]])
    df_re = df_re.dropna(axis=1, how='all')
    df_re = df_re.fillna("пусто")
    df_re['numerator'] = "пусто"
    
    
    for i in range(len(df_re["numerator"].index)):
        if i % 2 == 0:
            df_re.iloc[i, -1] = 0
        else:
            df_re.iloc[i, -1] = 1
    
    df_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
    
    p_cell = []
    p_cab = 0
    p_predmet = 0
    p_prepod = 0
    df_hollow = []
    ci = -1
    cj = -1
    groupNames = df_re.columns
    
    try:
        for j in range(len(df_re.columns) - 3):
            if groupNames[j + 2] == groupNames[j + 1]:
                podGroup = 2
            else:
                podGroup = 1
            
            groupName = groupNames[j + 2]
            ci = -1
            cj += 1
            for i in range(len(df_re.index)):
                ci += 1
                br = 0
                if df_re.iloc[i, j + 2] != "пусто":
                    p_cell = df_re.iloc[i, j + 2].split()
                        
                        
                        
                    if ("Z" in p_cell):
                        p_cell = list(filter(lambda a: a != "Z", p_cell))
                    if ("..." in p_cell):
                        p_cell = list(filter(lambda a: a != "...", p_cell))
                    if (("БАЗ" in p_cell) or                     ("пр.Деловые" in p_cell) or ("л.Деловые" in p_cell) or                     ("Элективные" in p_cell) or ("л.Физическая" in p_cell) or                    ("пр.Физическая" in p_cell) or ("Физическая" in p_cell)) and ("химия" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            del p_cell[-1]
                        else:
                            p_cab = "-"
                        p_predmet = p_cell
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("лаб.Пром." in p_cell) and ("/" in p_cell):
                        p_cab = p_cell[-1]
                        p_prepod = p_cell[0] + " " + p_cell[1] + " " + "/" + "  " + p_cell[-3] + " " + p_cell[-2]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("пр.Организационное" in p_cell) or ("л.Организационное" in p_cell) and (len(p_cell[-2]) != 4):
                        p_cab = p_cell[-1]
                        del p_cell[-1]
                        p_prepod = "-"
                        p_predmet = p_cell
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif ("/" in p_cell) and ("л.ОППД" not in p_cell) and ("п/г" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            p_cell = list(filter(lambda a: a != p_cab, p_cell))
                        else:
                            p_cab = "-"
                            
                        if p_cell[-3] == "/":
                            p_prepod = p_cell[-5:]
                            p_predmet = p_cell[:-5]
                        else:
                            find_str = p_cell.index("/")
                            p_prepod = p_cell[find_str - 2] + " " + p_cell[find_str - 1] + " " + "/" + " " + p_cell[-2] + " " + p_cell[-1]
                            p_prepod = p_prepod.split()
                            
                            del p_cell[find_str - 2]
                            del p_cell[find_str - 2]
                            del p_cell[-2]
                            del p_cell[-1]
                            
                            p_predmet = p_cell
                            
                        
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "Вакансия" in p_cell:
                        p_cab = p_cell[-3]
                        p_predmet = p_cell[:-3]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "пр.Иностранный" in p_cell:
                        p_predmet = "пр.Иностранный язык"
                        del p_cell[0]
                        del p_cell[0]

                        if len(p_cell) < 3:
                            break
                        
                        # change
                        if "п/г" in p_cell:
                            p_cell.remove("п/г")
                            del p_cell[0]

                        if "(нем.)" in p_cell:
                            p_cell.remove("(нем.)")
                        if "(нем)" in p_cell:
                            p_cell.remove("(нем)")

                        if "делового" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык делового общения"
                            if "общения" in p_cell:
                                del p_cell[0]
                                p_predmet = "пр.Иностранный язык проф. и делового общения"

                        if "профессионального" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык профессионального общения"


                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    elif "иностранных" in p_cell:
                        p_predmet = "пр.Основы делового общения на иностранных языках"
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif (len([s for s in p_cell if s.isdigit()]) > 1) or ((len([s for s in p_cell if s.isdigit()]) == 1) and ("-" in p_cell[-1])) or (("111/2" in p_cell) and p_cell[-1][1].isdigit): 
                        p_predmet = []
                        
                        for bij in p_cell:
                            if bij.isdigit() or bij == "111/2":
                                p_cab = bij + " " + "/" + " " + p_cell[-1]
                                p_prepod = p_cell[p_cell.index(bij) - 2] + " " + p_cell[p_cell.index(bij) - 1] + " " + "/" + " "  + p_cell[-3] + " " + p_cell[-2]
                                p_predmet.append(p_cell[:p_cell.index(bij) - 2])
                                p_predmet.append("/")
                                p_predmet.append(p_cell[p_cell.index(bij) + 1: -3])
                                break
                        
                        
                        p_predmet = str(p_predmet)
                        p_predmet = p_predmet.replace("[", "")
                        p_predmet = p_predmet.replace("'", "")
                        p_predmet = p_predmet.replace("]", "")
                        p_predmet = p_predmet.replace(",", "")
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                        
                    elif "лаб.Прод." in p_cell:
                        for ch in p_cell:
                            if ch.isdigit():
                                p_cab = str(ch)
                                break
                        p_prepod = p_cell[p_cell.index(p_cab) - 2] + " " + p_cell[p_cell.index(p_cab) - 1]
                        p_predmet = p_cell[:p_cell.index(p_cab) - 2]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    

                    elif ("пр.Технологическое" in p_cell) or ("л.Технологическое" in p_cell) or ("пр.Тех." in p_cell):
                        p_predmet = p_cell[0] + " " + p_cell[1] + " " + p_cell[2]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        if  len(p_cell) < 3:
                            break
                        else:
                            p_cab = p_cell[-1]
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    else:
                        if (p_cell[-1] == ".МАЗ") and (p_cell[-2] == "а"):
                            p_cell.pop(-1)
                            p_cell.pop(-1)
                            p_cell.append("а.МАЗ")


                        if len(p_cell[-2]) < 4:
                            p_prepod = p_cell[-4] + " " + p_cell[-3] + p_cell[-2][1:]
                            p_predmet = p_cell[:-4]

                        elif "ГПДНевструев" in p_cell:
                            del p_cell[-2] 
                            del p_cell[-2]
                            p_prepod = "Невструев Ю.А."
                            p_predmet = p_cell[:-3]

                        else:
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            p_predmet = p_cell[:-3]

                        p_cab = p_cell[-1]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                            
    except Exception as e:
        # ... PRINT THE ERROR MESSAGE ... #
        print(ci, cj + 2, sheet_n, p_cell)
        print("Error - ", e)
        print(traceback.format_exc())
    
    
    for i in range(len(df_main["lessonName"])):
        peremn = df_main.iloc[i, 0]
        if isinstance(peremn, list):
            df_main.iloc[i, 0] = ' '.join(peremn)
    
    for i in range(len(df_main["lessonTeacher"])):
        peremn = df_main.iloc[i, 3]
        if isinstance(peremn, list):
            df_main.iloc[i, 3] = ' '.join(peremn)
    
    
    df_main['id'] = df_main.index
    
    cols = df_main.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_main = df_main[cols]
    
    teachers = np.unique(df_main["lessonTeacher"].values)
    
    teacher = pd.DataFrame(columns = ["id", "teacherName"])
    
    teacher['teacherName'] = teachers
    
    teacher['id'] = teacher.index
    
    df_tp_main = df_tp_main.append(df_main)
    df_tp_teacher = df_tp_teacher.append(teacher)
    

df_all_main = df_all_main.append(df_tp_main)
df_all_teacher = df_all_teacher.append(df_tp_teacher) 


# In[5]:


df_tp_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
df_tp_teacher = pd.DataFrame(columns = ["id", "teacherName"])


# In[6]:

df_sheet_all = pd.read_excel((os.path.join(sys.path[0], r"rasp\unmer", "eiu_unmer.xlsx")), sheet_name=None)

sheet_n = 0

for i in df_sheet_all:
    sheet_n += 1
    df_re = df_sheet_all[i]
    df_re = df_re.drop(df_re.index[[0, 1, 2, 3, 4]])
    df_re = df_re.rename(columns=df_re.iloc[0])
    df_re = df_re.drop(df_re.index[[0, -1, -2]])
    df_re = df_re.dropna(axis=1, how='all')
    df_re = df_re.fillna("пусто")
    df_re['numerator'] = "пусто"
    
    
    for i in range(len(df_re["numerator"].index)):
        if i % 2 == 0:
            df_re.iloc[i, -1] = 0
        else:
            df_re.iloc[i, -1] = 1
    
    df_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
    
    p_cell = []
    p_cab = 0
    p_predmet = 0
    p_prepod = 0
    df_hollow = []
    ci = -1
    cj = -1
    groupNames = df_re.columns
    
    try:
        for j in range(len(df_re.columns) - 3):
            if groupNames[j + 2] == groupNames[j + 1]:
                podGroup = 2
            else:
                podGroup = 1
            
            groupName = groupNames[j + 2]
            ci = -1
            cj += 1
            for i in range(len(df_re.index)):
                ci += 1
                br = 0
                if df_re.iloc[i, j + 2] != "пусто":
                    p_cell = df_re.iloc[i, j + 2].split()
                        
                        
                        
                    if ("Z" in p_cell):
                        p_cell = list(filter(lambda a: a != "Z", p_cell))
                    if ("..." in p_cell):
                        p_cell = list(filter(lambda a: a != "...", p_cell))
                    if (("БАЗ" in p_cell) or                     ("пр.Деловые" in p_cell) or ("л.Деловые" in p_cell) or                     ("Элективные" in p_cell) or ("л.Физическая" in p_cell) or                    ("пр.Физическая" in p_cell) or ("Физическая" in p_cell)) and ("химия" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            del p_cell[-1]
                        else:
                            p_cab = "-"
                        p_predmet = p_cell
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("лаб.Пром." in p_cell) and ("/" in p_cell):
                        p_cab = p_cell[-1]
                        p_prepod = p_cell[0] + " " + p_cell[1] + " " + "/" + "  " + p_cell[-3] + " " + p_cell[-2]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("пр.Организационное" in p_cell) or ("л.Организационное" in p_cell) and (len(p_cell[-2]) != 4):
                        p_cab = p_cell[-1]
                        del p_cell[-1]
                        p_prepod = "-"
                        p_predmet = p_cell
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif ("/" in p_cell) and ("л.ОППД" not in p_cell) and ("п/г" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            p_cell = list(filter(lambda a: a != p_cab, p_cell))
                        else:
                            p_cab = "-"
                            
                        if p_cell[-3] == "/":
                            p_prepod = p_cell[-5:]
                            p_predmet = p_cell[:-5]
                        else:
                            find_str = p_cell.index("/")
                            p_prepod = p_cell[find_str - 2] + " " + p_cell[find_str - 1] + " " + "/" + " " + p_cell[-2] + " " + p_cell[-1]
                            p_prepod = p_prepod.split()
                            
                            del p_cell[find_str - 2]
                            del p_cell[find_str - 2]
                            del p_cell[-2]
                            del p_cell[-1]
                            
                            p_predmet = p_cell
                            
                        
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "Вакансия" in p_cell:
                        p_cab = p_cell[-3]
                        p_predmet = p_cell[:-3]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "пр.Иностранный" in p_cell:
                        p_predmet = "пр.Иностранный язык"
                        del p_cell[0]
                        del p_cell[0]

                        if len(p_cell) < 3:
                            break
                        
                        # change
                        if "п/г" in p_cell:
                            p_cell.remove("п/г")
                            del p_cell[0]

                        if "(нем.)" in p_cell:
                            p_cell.remove("(нем.)")
                        if "(нем)" in p_cell:
                            p_cell.remove("(нем)")

                        if "делового" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык делового общения"
                            if "общения" in p_cell:
                                del p_cell[0]
                                p_predmet = "пр.Иностранный язык проф. и делового общения"

                        if "профессионального" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык профессионального общения"


                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    elif "иностранных" in p_cell:
                        p_predmet = "пр.Основы делового общения на иностранных языках"
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif (len([s for s in p_cell if s.isdigit()]) > 1) or ((len([s for s in p_cell if s.isdigit()]) == 1) and ("-" in p_cell[-1])) or (("111/2" in p_cell) and p_cell[-1][1].isdigit): 
                        p_predmet = []
                        
                        for bij in p_cell:
                            if bij.isdigit() or bij == "111/2":
                                p_cab = bij + " " + "/" + " " + p_cell[-1]
                                p_prepod = p_cell[p_cell.index(bij) - 2] + " " + p_cell[p_cell.index(bij) - 1] + " " + "/" + " "  + p_cell[-3] + " " + p_cell[-2]
                                p_predmet.append(p_cell[:p_cell.index(bij) - 2])
                                p_predmet.append("/")
                                p_predmet.append(p_cell[p_cell.index(bij) + 1: -3])
                                break
                        
                        
                        p_predmet = str(p_predmet)
                        p_predmet = p_predmet.replace("[", "")
                        p_predmet = p_predmet.replace("'", "")
                        p_predmet = p_predmet.replace("]", "")
                        p_predmet = p_predmet.replace(",", "")
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                        
                    elif "лаб.Прод." in p_cell:
                        for ch in p_cell:
                            if ch.isdigit():
                                p_cab = str(ch)
                                break
                        p_prepod = p_cell[p_cell.index(p_cab) - 2] + " " + p_cell[p_cell.index(p_cab) - 1]
                        p_predmet = p_cell[:p_cell.index(p_cab) - 2]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    

                    elif ("пр.Технологическое" in p_cell) or ("л.Технологическое" in p_cell) or ("пр.Тех." in p_cell):
                        p_predmet = p_cell[0] + " " + p_cell[1] + " " + p_cell[2]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        if  len(p_cell) < 3:
                            break
                        else:
                            p_cab = p_cell[-1]
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    else:
                        if (p_cell[-1] == ".МАЗ") and (p_cell[-2] == "а"):
                            p_cell.pop(-1)
                            p_cell.pop(-1)
                            p_cell.append("а.МАЗ")


                        if len(p_cell[-2]) < 4:
                            p_prepod = p_cell[-4] + " " + p_cell[-3] + p_cell[-2][1:]
                            p_predmet = p_cell[:-4]

                        elif "ГПДНевструев" in p_cell:
                            del p_cell[-2] 
                            del p_cell[-2]
                            p_prepod = "Невструев Ю.А."
                            p_predmet = p_cell[:-3]

                        else:
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            p_predmet = p_cell[:-3]

                        p_cab = p_cell[-1]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                            
    except Exception as e:
        # ... PRINT THE ERROR MESSAGE ... #
        print(ci, cj + 2, sheet_n, p_cell)
        print("Error - ", e)
        print(traceback.format_exc())
    
    
    for i in range(len(df_main["lessonName"])):
        peremn = df_main.iloc[i, 0]
        if isinstance(peremn, list):
            df_main.iloc[i, 0] = ' '.join(peremn)
    
    for i in range(len(df_main["lessonTeacher"])):
        peremn = df_main.iloc[i, 3]
        if isinstance(peremn, list):
            df_main.iloc[i, 3] = ' '.join(peremn)
    
    
    df_main['id'] = df_main.index
    
    cols = df_main.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_main = df_main[cols]
    
    teachers = np.unique(df_main["lessonTeacher"].values)
    
    teacher = pd.DataFrame(columns = ["id", "teacherName"])
    
    teacher['teacherName'] = teachers
    
    teacher['id'] = teacher.index
    
    df_tp_main = df_tp_main.append(df_main)
    df_tp_teacher = df_tp_teacher.append(teacher)
    

df_all_main = df_all_main.append(df_tp_main)
df_all_teacher = df_all_teacher.append(df_tp_teacher) 


# In[7]:


df_tp_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
df_tp_teacher = pd.DataFrame(columns = ["id", "teacherName"])


# In[8]:

df_sheet_all = pd.read_excel((os.path.join(sys.path[0], r"rasp\unmer", "pma_unmer.xlsx")), sheet_name=None)

sheet_n = 0

for i in df_sheet_all:
    sheet_n += 1
    df_re = df_sheet_all[i]
    df_re = df_re.drop(df_re.index[[0, 1, 2, 3, 4]])
    df_re = df_re.rename(columns=df_re.iloc[0])
    df_re = df_re.drop(df_re.index[[0, -1, -2]])
    df_re = df_re.dropna(axis=1, how='all')
    df_re = df_re.fillna("пусто")
    df_re['numerator'] = "пусто"
    
    
    for i in range(len(df_re["numerator"].index)):
        if i % 2 == 0:
            df_re.iloc[i, -1] = 0
        else:
            df_re.iloc[i, -1] = 1
    
    df_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
    
    p_cell = []
    p_cab = 0
    p_predmet = 0
    p_prepod = 0
    df_hollow = []
    ci = -1
    cj = -1
    groupNames = df_re.columns
    
    try:
        for j in range(len(df_re.columns) - 3):
            if groupNames[j + 2] == groupNames[j + 1]:
                podGroup = 2
            else:
                podGroup = 1
            
            groupName = groupNames[j + 2]
            ci = -1
            cj += 1
            for i in range(len(df_re.index)):
                ci += 1
                br = 0
                if df_re.iloc[i, j + 2] != "пусто":
                    p_cell = df_re.iloc[i, j + 2].split()
                        
                        
                        
                    if ("Z" in p_cell):
                        p_cell = list(filter(lambda a: a != "Z", p_cell))
                    if ("..." in p_cell):
                        p_cell = list(filter(lambda a: a != "...", p_cell))
                    if (("БАЗ" in p_cell) or                     ("пр.Деловые" in p_cell) or ("л.Деловые" in p_cell) or                     ("Элективные" in p_cell) or ("л.Физическая" in p_cell) or                    ("пр.Физическая" in p_cell) or ("Физическая" in p_cell)) and ("химия" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            del p_cell[-1]
                        else:
                            p_cab = "-"
                        p_predmet = p_cell
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("лаб.Пром." in p_cell) and ("/" in p_cell):
                        p_cab = p_cell[-1]
                        p_prepod = p_cell[0] + " " + p_cell[1] + " " + "/" + "  " + p_cell[-3] + " " + p_cell[-2]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("пр.Организационное" in p_cell) or ("л.Организационное" in p_cell) and (len(p_cell[-2]) != 4):
                        p_cab = p_cell[-1]
                        del p_cell[-1]
                        p_prepod = "-"
                        p_predmet = p_cell
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif ("/" in p_cell) and ("л.ОППД" not in p_cell) and ("п/г" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            p_cell = list(filter(lambda a: a != p_cab, p_cell))
                        else:
                            p_cab = "-"
                            
                        if p_cell[-3] == "/":
                            p_prepod = p_cell[-5:]
                            p_predmet = p_cell[:-5]
                        else:
                            find_str = p_cell.index("/")
                            p_prepod = p_cell[find_str - 2] + " " + p_cell[find_str - 1] + " " + "/" + " " + p_cell[-2] + " " + p_cell[-1]
                            p_prepod = p_prepod.split()
                            
                            del p_cell[find_str - 2]
                            del p_cell[find_str - 2]
                            del p_cell[-2]
                            del p_cell[-1]
                            
                            p_predmet = p_cell
                            
                        
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "Вакансия" in p_cell:
                        p_cab = p_cell[-3]
                        p_predmet = p_cell[:-3]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "пр.Иностранный" in p_cell:
                        p_predmet = "пр.Иностранный язык"
                        del p_cell[0]
                        del p_cell[0]

                        if len(p_cell) < 3:
                            break
                        
                        # change
                        if "п/г" in p_cell:
                            p_cell.remove("п/г")
                            del p_cell[0]

                        if "(нем.)" in p_cell:
                            p_cell.remove("(нем.)")
                        if "(нем)" in p_cell:
                            p_cell.remove("(нем)")

                        if "делового" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык делового общения"
                            if "общения" in p_cell:
                                del p_cell[0]
                                p_predmet = "пр.Иностранный язык проф. и делового общения"

                        if "профессионального" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык профессионального общения"


                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    elif "иностранных" in p_cell:
                        p_predmet = "пр.Основы делового общения на иностранных языках"
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif (len([s for s in p_cell if s.isdigit()]) > 1) or ((len([s for s in p_cell if s.isdigit()]) == 1) and ("-" in p_cell[-1])) or (("111/2" in p_cell) and p_cell[-1][1].isdigit): 
                        p_predmet = []
                        
                        for bij in p_cell:
                            if bij.isdigit() or bij == "111/2":
                                p_cab = bij + " " + "/" + " " + p_cell[-1]
                                p_prepod = p_cell[p_cell.index(bij) - 2] + " " + p_cell[p_cell.index(bij) - 1] + " " + "/" + " "  + p_cell[-3] + " " + p_cell[-2]
                                p_predmet.append(p_cell[:p_cell.index(bij) - 2])
                                p_predmet.append("/")
                                p_predmet.append(p_cell[p_cell.index(bij) + 1: -3])
                                break
                        
                        
                        p_predmet = str(p_predmet)
                        p_predmet = p_predmet.replace("[", "")
                        p_predmet = p_predmet.replace("'", "")
                        p_predmet = p_predmet.replace("]", "")
                        p_predmet = p_predmet.replace(",", "")
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                        
                    elif "лаб.Прод." in p_cell:
                        for ch in p_cell:
                            if ch.isdigit():
                                p_cab = str(ch)
                                break
                        p_prepod = p_cell[p_cell.index(p_cab) - 2] + " " + p_cell[p_cell.index(p_cab) - 1]
                        p_predmet = p_cell[:p_cell.index(p_cab) - 2]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    

                    elif ("пр.Технологическое" in p_cell) or ("л.Технологическое" in p_cell) or ("пр.Тех." in p_cell):
                        p_predmet = p_cell[0] + " " + p_cell[1] + " " + p_cell[2]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        if  len(p_cell) < 3:
                            break
                        else:
                            p_cab = p_cell[-1]
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    else:
                        if (p_cell[-1] == ".МАЗ") and (p_cell[-2] == "а"):
                            p_cell.pop(-1)
                            p_cell.pop(-1)
                            p_cell.append("а.МАЗ")


                        if len(p_cell[-2]) < 4:
                            p_prepod = p_cell[-4] + " " + p_cell[-3] + p_cell[-2][1:]
                            p_predmet = p_cell[:-4]

                        elif "ГПДНевструев" in p_cell:
                            del p_cell[-2] 
                            del p_cell[-2]
                            p_prepod = "Невструев Ю.А."
                            p_predmet = p_cell[:-3]

                        else:
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            p_predmet = p_cell[:-3]

                        p_cab = p_cell[-1]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                            
    except Exception as e:
        # ... PRINT THE ERROR MESSAGE ... #
        print(ci, cj + 2, sheet_n, p_cell)
        print("Error - ", e)
        print(traceback.format_exc())
    
    
    for i in range(len(df_main["lessonName"])):
        peremn = df_main.iloc[i, 0]
        if isinstance(peremn, list):
            df_main.iloc[i, 0] = ' '.join(peremn)
    
    for i in range(len(df_main["lessonTeacher"])):
        peremn = df_main.iloc[i, 3]
        if isinstance(peremn, list):
            df_main.iloc[i, 3] = ' '.join(peremn)
    
    
    df_main['id'] = df_main.index
    
    cols = df_main.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_main = df_main[cols]
    
    teachers = np.unique(df_main["lessonTeacher"].values)
    
    teacher = pd.DataFrame(columns = ["id", "teacherName"])
    
    teacher['teacherName'] = teachers
    
    teacher['id'] = teacher.index
    
    df_tp_main = df_tp_main.append(df_main)
    df_tp_teacher = df_tp_teacher.append(teacher)
    

df_all_main = df_all_main.append(df_tp_main)
df_all_teacher = df_all_teacher.append(df_tp_teacher) 


# In[9]:


df_tp_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
df_tp_teacher = pd.DataFrame(columns = ["id", "teacherName"])


# In[10]:

df_sheet_all = pd.read_excel((os.path.join(sys.path[0], r"rasp\unmer", "tf_unmer.xlsx")), sheet_name=None)

sheet_n = 0

for i in df_sheet_all:
    sheet_n += 1
    df_re = df_sheet_all[i]
    df_re = df_re.drop(df_re.index[[0, 1, 2, 3, 4]])
    df_re = df_re.rename(columns=df_re.iloc[0])
    df_re = df_re.drop(df_re.index[[0, -1, -2]])
    df_re = df_re.dropna(axis=1, how='all')
    df_re = df_re.fillna("пусто")
    df_re['numerator'] = "пусто"
    
    
    for i in range(len(df_re["numerator"].index)):
        if i % 2 == 0:
            df_re.iloc[i, -1] = 0
        else:
            df_re.iloc[i, -1] = 1
    
    df_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
    
    p_cell = []
    p_cab = 0
    p_predmet = 0
    p_prepod = 0
    df_hollow = []
    ci = -1
    cj = -1
    groupNames = df_re.columns
    
    try:
        for j in range(len(df_re.columns) - 3):
            if groupNames[j + 2] == groupNames[j + 1]:
                podGroup = 2
            else:
                podGroup = 1
            
            groupName = groupNames[j + 2]
            ci = -1
            cj += 1
            for i in range(len(df_re.index)):
                ci += 1
                br = 0
                if df_re.iloc[i, j + 2] != "пусто":
                    p_cell = df_re.iloc[i, j + 2].split()
                        
                        
                        
                    if ("Z" in p_cell):
                        p_cell = list(filter(lambda a: a != "Z", p_cell))
                    if ("..." in p_cell):
                        p_cell = list(filter(lambda a: a != "...", p_cell))
                    if (("БАЗ" in p_cell) or                     ("пр.Деловые" in p_cell) or ("л.Деловые" in p_cell) or                     ("Элективные" in p_cell) or ("л.Физическая" in p_cell) or                    ("пр.Физическая" in p_cell) or ("Физическая" in p_cell)) and ("химия" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            del p_cell[-1]
                        else:
                            p_cab = "-"
                        p_predmet = p_cell
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("лаб.Пром." in p_cell) and ("/" in p_cell):
                        p_cab = p_cell[-1]
                        p_prepod = p_cell[0] + " " + p_cell[1] + " " + "/" + "  " + p_cell[-3] + " " + p_cell[-2]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("пр.Организационное" in p_cell) or ("л.Организационное" in p_cell) and (len(p_cell[-2]) != 4):
                        p_cab = p_cell[-1]
                        del p_cell[-1]
                        p_prepod = "-"
                        p_predmet = p_cell
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif ("/" in p_cell) and ("л.ОППД" not in p_cell) and ("п/г" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            p_cell = list(filter(lambda a: a != p_cab, p_cell))
                        else:
                            p_cab = "-"
                            
                        if p_cell[-3] == "/":
                            p_prepod = p_cell[-5:]
                            p_predmet = p_cell[:-5]
                        else:
                            find_str = p_cell.index("/")
                            p_prepod = p_cell[find_str - 2] + " " + p_cell[find_str - 1] + " " + "/" + " " + p_cell[-2] + " " + p_cell[-1]
                            p_prepod = p_prepod.split()
                            
                            del p_cell[find_str - 2]
                            del p_cell[find_str - 2]
                            del p_cell[-2]
                            del p_cell[-1]
                            
                            p_predmet = p_cell
                            
                        
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "Вакансия" in p_cell:
                        p_cab = p_cell[-3]
                        p_predmet = p_cell[:-3]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "пр.Иностранный" in p_cell:
                        p_predmet = "пр.Иностранный язык"
                        del p_cell[0]
                        del p_cell[0]

                        if len(p_cell) < 3:
                            break
                        
                        # change
                        if "п/г" in p_cell:
                            p_cell.remove("п/г")
                            del p_cell[0]

                        if "(нем.)" in p_cell:
                            p_cell.remove("(нем.)")
                        if "(нем)" in p_cell:
                            p_cell.remove("(нем)")

                        if "делового" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык делового общения"
                            if "общения" in p_cell:
                                del p_cell[0]
                                p_predmet = "пр.Иностранный язык проф. и делового общения"

                        if "профессионального" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык профессионального общения"


                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    elif "иностранных" in p_cell:
                        p_predmet = "пр.Основы делового общения на иностранных языках"
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif (len([s for s in p_cell if s.isdigit()]) > 1) or ((len([s for s in p_cell if s.isdigit()]) == 1) and ("-" in p_cell[-1])) or (("111/2" in p_cell) and p_cell[-1][1].isdigit): 
                        p_predmet = []
                        
                        for bij in p_cell:
                            if bij.isdigit() or bij == "111/2":
                                p_cab = bij + " " + "/" + " " + p_cell[-1]
                                p_prepod = p_cell[p_cell.index(bij) - 2] + " " + p_cell[p_cell.index(bij) - 1] + " " + "/" + " "  + p_cell[-3] + " " + p_cell[-2]
                                p_predmet.append(p_cell[:p_cell.index(bij) - 2])
                                p_predmet.append("/")
                                p_predmet.append(p_cell[p_cell.index(bij) + 1: -3])
                                break
                        
                        
                        p_predmet = str(p_predmet)
                        p_predmet = p_predmet.replace("[", "")
                        p_predmet = p_predmet.replace("'", "")
                        p_predmet = p_predmet.replace("]", "")
                        p_predmet = p_predmet.replace(",", "")
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                        
                    elif "лаб.Прод." in p_cell:
                        for ch in p_cell:
                            if ch.isdigit():
                                p_cab = str(ch)
                                break
                        p_prepod = p_cell[p_cell.index(p_cab) - 2] + " " + p_cell[p_cell.index(p_cab) - 1]
                        p_predmet = p_cell[:p_cell.index(p_cab) - 2]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    

                    elif ("пр.Технологическое" in p_cell) or ("л.Технологическое" in p_cell) or ("пр.Тех." in p_cell):
                        p_predmet = p_cell[0] + " " + p_cell[1] + " " + p_cell[2]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        if  len(p_cell) < 3:
                            break
                        else:
                            p_cab = p_cell[-1]
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    else:
                        if (p_cell[-1] == ".МАЗ") and (p_cell[-2] == "а"):
                            p_cell.pop(-1)
                            p_cell.pop(-1)
                            p_cell.append("а.МАЗ")


                        if len(p_cell[-2]) < 4:
                            p_prepod = p_cell[-4] + " " + p_cell[-3] + p_cell[-2][1:]
                            p_predmet = p_cell[:-4]

                        elif "ГПДНевструев" in p_cell:
                            del p_cell[-2] 
                            del p_cell[-2]
                            p_prepod = "Невструев Ю.А."
                            p_predmet = p_cell[:-3]

                        else:
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            p_predmet = p_cell[:-3]

                        p_cab = p_cell[-1]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                            
    except Exception as e:
        # ... PRINT THE ERROR MESSAGE ... #
        print(ci, cj + 2, sheet_n, p_cell)
        print("Error - ", e)
        print(traceback.format_exc())
    
    
    for i in range(len(df_main["lessonName"])):
        peremn = df_main.iloc[i, 0]
        if isinstance(peremn, list):
            df_main.iloc[i, 0] = ' '.join(peremn)
    
    for i in range(len(df_main["lessonTeacher"])):
        peremn = df_main.iloc[i, 3]
        if isinstance(peremn, list):
            df_main.iloc[i, 3] = ' '.join(peremn)
    
    
    df_main['id'] = df_main.index
    
    cols = df_main.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_main = df_main[cols]
    
    teachers = np.unique(df_main["lessonTeacher"].values)
    
    teacher = pd.DataFrame(columns = ["id", "teacherName"])
    
    teacher['teacherName'] = teachers
    
    teacher['id'] = teacher.index
    
    df_tp_main = df_tp_main.append(df_main)
    df_tp_teacher = df_tp_teacher.append(teacher)
    

df_all_main = df_all_main.append(df_tp_main)
df_all_teacher = df_all_teacher.append(df_tp_teacher) 


# In[11]:


df_tp_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
df_tp_teacher = pd.DataFrame(columns = ["id", "teacherName"])


# In[12]:

df_sheet_all = pd.read_excel((os.path.join(sys.path[0], r"rasp\unmer", "uits_unmer.xlsx")), sheet_name=None)

sheet_n = 0

for i in df_sheet_all:
    sheet_n += 1
    df_re = df_sheet_all[i]
    df_re = df_re.drop(df_re.index[[0, 1, 2, 3, 4]])
    df_re = df_re.rename(columns=df_re.iloc[0])
    df_re = df_re.drop(df_re.index[[0, -1, -2]])
    df_re = df_re.dropna(axis=1, how='all')
    df_re = df_re.fillna("пусто")
    df_re['numerator'] = "пусто"
    
    
    for i in range(len(df_re["numerator"].index)):
        if i % 2 == 0:
            df_re.iloc[i, -1] = 0
        else:
            df_re.iloc[i, -1] = 1
    
    df_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
    
    p_cell = []
    p_cab = 0
    p_predmet = 0
    p_prepod = 0
    df_hollow = []
    ci = -1
    cj = -1
    groupNames = df_re.columns
    
    try:
        for j in range(len(df_re.columns) - 3):
            if groupNames[j + 2] == groupNames[j + 1]:
                podGroup = 2
            else:
                podGroup = 1
            
            groupName = groupNames[j + 2]
            ci = -1
            cj += 1
            for i in range(len(df_re.index)):
                ci += 1
                br = 0
                if df_re.iloc[i, j + 2] != "пусто":
                    p_cell = df_re.iloc[i, j + 2].split()
                        
                        
                        
                    if ("Z" in p_cell):
                        p_cell = list(filter(lambda a: a != "Z", p_cell))
                    if ("..." in p_cell):
                        p_cell = list(filter(lambda a: a != "...", p_cell))
                    if (("БАЗ" in p_cell) or                     ("пр.Деловые" in p_cell) or ("л.Деловые" in p_cell) or                     ("Элективные" in p_cell) or ("л.Физическая" in p_cell) or                    ("пр.Физическая" in p_cell) or ("Физическая" in p_cell)) and ("химия" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            del p_cell[-1]
                        else:
                            p_cab = "-"
                        p_predmet = p_cell
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("лаб.Пром." in p_cell) and ("/" in p_cell):
                        p_cab = p_cell[-1]
                        p_prepod = p_cell[0] + " " + p_cell[1] + " " + "/" + "  " + p_cell[-3] + " " + p_cell[-2]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        br = 1
                        continue
                    
                    
                    elif ("пр.Организационное" in p_cell) or ("л.Организационное" in p_cell) and (len(p_cell[-2]) != 4):
                        p_cab = p_cell[-1]
                        del p_cell[-1]
                        p_prepod = "-"
                        p_predmet = p_cell
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif ("/" in p_cell) and ("л.ОППД" not in p_cell) and ("п/г" not in p_cell):
                        if p_cell[-1].isdigit():
                            p_cab = p_cell[-1]
                            p_cell = list(filter(lambda a: a != p_cab, p_cell))
                        else:
                            p_cab = "-"
                            
                        if p_cell[-3] == "/":
                            p_prepod = p_cell[-5:]
                            p_predmet = p_cell[:-5]
                        else:
                            find_str = p_cell.index("/")
                            p_prepod = p_cell[find_str - 2] + " " + p_cell[find_str - 1] + " " + "/" + " " + p_cell[-2] + " " + p_cell[-1]
                            p_prepod = p_prepod.split()
                            
                            del p_cell[find_str - 2]
                            del p_cell[find_str - 2]
                            del p_cell[-2]
                            del p_cell[-1]
                            
                            p_predmet = p_cell
                            
                        
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "Вакансия" in p_cell:
                        p_cab = p_cell[-3]
                        p_predmet = p_cell[:-3]
                        p_prepod = "-"
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif "пр.Иностранный" in p_cell:
                        p_predmet = "пр.Иностранный язык"
                        del p_cell[0]
                        del p_cell[0]

                        if len(p_cell) < 3:
                            break
                        
                        # change
                        if "п/г" in p_cell:
                            p_cell.remove("п/г")
                            del p_cell[0]

                        if "(нем.)" in p_cell:
                            p_cell.remove("(нем.)")
                        if "(нем)" in p_cell:
                            p_cell.remove("(нем)")

                        if "делового" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык делового общения"
                            if "общения" in p_cell:
                                del p_cell[0]
                                p_predmet = "пр.Иностранный язык проф. и делового общения"

                        if "профессионального" in p_cell:
                            del p_cell[0]
                            del p_cell[0]
                            p_predmet = "пр.Иностранный язык профессионального общения"


                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    elif "иностранных" in p_cell:
                        p_predmet = "пр.Основы делового общения на иностранных языках"
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        for obj in range(0, len(p_cell), 3):
                            p_prepod = p_cell[obj] + " " + p_cell[obj + 1]
                            p_cab = p_cell[obj + 2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                    
                    elif (len([s for s in p_cell if s.isdigit()]) > 1) or ((len([s for s in p_cell if s.isdigit()]) == 1) and ("-" in p_cell[-1])) or (("111/2" in p_cell) and p_cell[-1][1].isdigit): 
                        p_predmet = []
                        
                        for bij in p_cell:
                            if bij.isdigit() or bij == "111/2":
                                p_cab = bij + " " + "/" + " " + p_cell[-1]
                                p_prepod = p_cell[p_cell.index(bij) - 2] + " " + p_cell[p_cell.index(bij) - 1] + " " + "/" + " "  + p_cell[-3] + " " + p_cell[-2]
                                p_predmet.append(p_cell[:p_cell.index(bij) - 2])
                                p_predmet.append("/")
                                p_predmet.append(p_cell[p_cell.index(bij) + 1: -3])
                                break
                        
                        
                        p_predmet = str(p_predmet)
                        p_predmet = p_predmet.replace("[", "")
                        p_predmet = p_predmet.replace("'", "")
                        p_predmet = p_predmet.replace("]", "")
                        p_predmet = p_predmet.replace(",", "")
                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                              ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    
                        
                    elif "лаб.Прод." in p_cell:
                        for ch in p_cell:
                            if ch.isdigit():
                                p_cab = str(ch)
                                break
                        p_prepod = p_cell[p_cell.index(p_cab) - 2] + " " + p_cell[p_cell.index(p_cab) - 1]
                        p_predmet = p_cell[:p_cell.index(p_cab) - 2]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                        continue
                    

                    elif ("пр.Технологическое" in p_cell) or ("л.Технологическое" in p_cell) or ("пр.Тех." in p_cell):
                        p_predmet = p_cell[0] + " " + p_cell[1] + " " + p_cell[2]
                        del p_cell[0]
                        del p_cell[0]
                        del p_cell[0]
                        if  len(p_cell) < 3:
                            break
                        else:
                            p_cab = p_cell[-1]
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                            df_main = df_main.append(df_hollow, ignore_index=True)
                        continue

                    else:
                        if (p_cell[-1] == ".МАЗ") and (p_cell[-2] == "а"):
                            p_cell.pop(-1)
                            p_cell.pop(-1)
                            p_cell.append("а.МАЗ")


                        if len(p_cell[-2]) < 4:
                            p_prepod = p_cell[-4] + " " + p_cell[-3] + p_cell[-2][1:]
                            p_predmet = p_cell[:-4]

                        elif "ГПДНевструев" in p_cell:
                            del p_cell[-2] 
                            del p_cell[-2]
                            p_prepod = "Невструев Ю.А."
                            p_predmet = p_cell[:-3]

                        else:
                            p_prepod = p_cell[-3] + " " + p_cell[-2]
                            p_predmet = p_cell[:-3]

                        p_cab = p_cell[-1]

                        df_hollow = pd.Series([p_predmet, df_re["Часы"].iloc[i], p_cab, p_prepod, df_re["Дни"].iloc[i], groupName, podGroup, df_re['numerator'].iloc[i]], 
                                                  ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
                        df_main = df_main.append(df_hollow, ignore_index=True)
                            
    except Exception as e:
        # ... PRINT THE ERROR MESSAGE ... #
        print(ci, cj + 2, sheet_n, p_cell)
        print("Error - ", e)
        print(traceback.format_exc())
    
    
    for i in range(len(df_main["lessonName"])):
        peremn = df_main.iloc[i, 0]
        if isinstance(peremn, list):
            df_main.iloc[i, 0] = ' '.join(peremn)
    
    for i in range(len(df_main["lessonTeacher"])):
        peremn = df_main.iloc[i, 3]
        if isinstance(peremn, list):
            df_main.iloc[i, 3] = ' '.join(peremn)
    
    
    df_main['id'] = df_main.index
    
    cols = df_main.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_main = df_main[cols]
    
    teachers = np.unique(df_main["lessonTeacher"].values)
    
    teacher = pd.DataFrame(columns = ["id", "teacherName"])
    
    teacher['teacherName'] = teachers
    
    teacher['id'] = teacher.index
    
    
    df_tp_main = df_tp_main.append(df_main)
    df_tp_teacher = df_tp_teacher.append(teacher)
    

df_all_main = df_all_main.append(df_tp_main)
df_all_teacher = df_all_teacher.append(df_tp_teacher) 


# In[13]:


df_tp_main = pd.DataFrame(columns = ['lessonName', 'lessonTime', 'lessonClass', "lessonTeacher", 'lessonDay', "groupName", "podGroup", 'numerator'])
df_tp_teacher = pd.DataFrame(columns = ["id", "teacherName"])


# # UNIQUE TEACHERS

# In[14]:


df_all_teacher = df_all_teacher.drop_duplicates(subset = "teacherName")


# In[15]:


df_all_teacher = df_all_teacher.reset_index()
df_all_teacher = df_all_teacher.drop('index', 1)


# In[16]:


for index, row in df_all_teacher.iterrows():
    if ("/" in row["teacherName"]) or ("-" in row["teacherName"]):
        df_all_teacher.drop(index, inplace=True)


# # CHANGE ID

# In[17]:


df_all_main = df_all_main.reset_index()
df_all_teacher = df_all_teacher.reset_index()

df_all_main = df_all_main.drop('index', 1)
df_all_teacher = df_all_teacher.drop('index', 1)

df_all_main["id"] = df_all_main.index
df_all_teacher["id"] = df_all_teacher.index

df_all_main["id"] += 1
df_all_teacher["id"] += 1


# In[20]:


#df_all_teacher.to_csv(r'csv\teacher.csv',index=False)


with open(os.path.join(sys.path[0], "JSON", "teacher.json"), "w", encoding='utf-8') as f:
    df_all_teacher.to_json(f, force_ascii=False)

# In[21]:


#df_all_main.to_csv(r'csv\lessonPair.csv',index=False)


with open(os.path.join(sys.path[0], "JSON", "lessonPair.json"), "w", encoding='utf-8') as f:
    df_all_main.to_json(f, force_ascii=False)
