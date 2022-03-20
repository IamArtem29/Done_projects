#!/usr/bin/env python
# coding: utf-8

# # Parsing

# In[1]:


import requests as req
import os
import sys


# In[2]:

with req.get("https://vsuet.ru/images/student/schedule/uits_osen_21_22.xlsx") as rq:
    with open(os.path.join(sys.path[0], "rasp\mer", "uits_mer.xlsx"), "wb") as file:
        file.write(rq.content)


# In[3]:

with req.get("https://vsuet.ru/images/student/schedule/pma_osen_21_22.xlsx") as rq:
    with open(os.path.join(sys.path[0], "rasp\mer", "pma_mer.xlsx"), "wb") as file:
        file.write(rq.content)


# In[4]:

with req.get("https://vsuet.ru/images/student/schedule/eht_osen_21_22.xlsx") as rq:
    with open(os.path.join(sys.path[0], "rasp\mer", "eht_mer.xlsx"), "wb") as file:
        file.write(rq.content)


# In[5]:

with req.get("https://vsuet.ru/images/student/schedule/tf_osen_21_22.xlsx") as rq:
    with open(os.path.join(sys.path[0], "rasp\mer", "tf_mer.xlsx"), "wb") as file:
        file.write(rq.content)


# In[6]:

with req.get("https://vsuet.ru/images/student/schedule/eiu_osen_21_22.xlsx") as rq:
    with open(os.path.join(sys.path[0], "rasp\mer", "eiu_mer.xlsx"), "wb") as file:
        file.write(rq.content)

