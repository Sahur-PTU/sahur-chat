# sahur-chat server / v 1.0 / 13.08.2026

import os
import sys
import time
import datetime
import json
import socket
import requests
import threading


logs = [None, None, None]
flags = [None, None, None]
flag = None
errors = [None] 

data = {"users":["user_1"], "msgs":{}}


def error():
  print(f"ошибка {errors[0]}")


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



def api():
    def connect():
        pass
    def disconnect():
        pass
    def write_data_server():
        pass
    def read_data_server():
        pass

  #try:
    while True:
        pass
  #except: pass


def check_masterKey():
  #try
    while True: 
        pass
  #except: None


def check_admin():
  #try
    while True: 
        pass
  #except: None

def check_user() :
  #try
    while True: 
        pass
  #except: None

def check_passw() :
  #try
    while True: 
        pass
  #except: None

def check_party() :
  #try
    while True: 
        pass
  #except: None


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
