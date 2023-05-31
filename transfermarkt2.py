# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:24 2022
Updated on Wed May 31 13:29 2023

@author: FIRATKABAN
@contributer: cerebnismus
"""


from collections import namedtuple
from bs4 import BeautifulSoup       # bs4 kütüphanesini import ediyoruz
import requests                     # requests kütüphanesini import ediyoruz
from requests import Session        # 
import time, csv, psycopg2, sys
from parsel   import Selector
