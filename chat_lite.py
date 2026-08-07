# sahur-chat lite / v 1.0 / 06.08.2026

import os
import time
import datetime
import json
import socket
#import requests
import threading


logs = [None, None, None]
flags = [None, None, None]
flag = None

data = {"users":["user_1"], "msgs":{}}

def write() :
  with open('database.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
def read() :
  try:
    with open('database.json', 'r', encoding='utf-8') as file:
      data_new = json.load(file)
      data.clear()
      data.update(data_new)
  except FileNotFoundError:
      print('файл "database" не найден'), time.sleep(1)
      _write = write()

def connect():
    pass
def disconnection():
    pass
def write_data_server():
    pass
def read_data_server():
    pass

def api():
    while True:
      pass

def login():
  while True:
    _read = read()
    username = input("username: ")
    if username == " ": exit()
    elif username in data['users']: return username
    else: continue

def menu() :
    username = login()
 # try:
    while True:
      os.system("cls")
      _read = read()
      for sms_num in data['msgs']:
         print('['+data['msgs'][sms_num]['time']+']','@'+data['msgs'][sms_num]['name'],':',data['msgs'][sms_num]['msg'])
      msg = input("> ")
      if msg == "": continue
      elif msg == " ": break
      elif msg == "clear": data["msgs"].clear()
      else: data['msgs'][len(data['msgs'])] = {'name':username, 'msg':msg, 'time':str(datetime.datetime.now())[5:-7]}
      update_write = write()
      _write = write_data_server()
  #except: pass


""" фоновая обработка соеденения . пока не нужно
def loop_api():
  _api = api()
  time.sleep(0.5)
def loop_menu():
  _menu = menu()
  time.sleep(0.6)
t1 = threading.Thread(target=loop_api) # Создаем потоки
t2 = threading.Thread(target=loop_menu)
t1.start() # запуск потоков
t2.start()
"""

def main():
  while True:
    #try:
      _menu = menu()
    #except: print("неизвестная ошибка"), time.sleep(0.5)

_main = main()
