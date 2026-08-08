# Sahur-PTU Chat / v 1.0 / 03.08.2026

# команды админа: 
#  admin - открыть админ меню
# 
#  base - вывести всю базу  
#  users - список всех пользователей
#  channels - список всех каналов 
#  complains - список жалоб
#  
#  id search - поиск по айди
#  name search - поиск по имени
#  ban <айди> - блокировка  пользователя
#  del <айди> - удаление пользователя 

import os
import sys
import json
import time
import datetime
import atexit
from colorama import init, Fore, Back, Style

init()
# os.system('mode con: cols=60 lines=17')
print("sahur-chat / v 1.0 / 03.08.2026") # сделать проверку на обновления 

# чтение из файла джесон и обновление по запросу

# модерация чата, отображение в общем меню в каких беседах состоит юзер, возможность смены данных аккаунта, администрация всего мессенджера
# возможность создавать новые каналы и управлять ими

# постоянное фоновое чтение базы с сервера

# key/read
# key/write/msg

log = [None, None, None, None]
flag = [None, None, None, None]

local = {"login":{}, "status":"False"}

smss = {
  "sessions" : {},
  "logs" : {},
  "updates" : {},
  "complaints" : {},

  "admins":{"user_1" : "user_1"},
  "users": { "1" : {"name":"user_1", "passw":"1234", "activity":"inactive", "status":"unblocked"},
             "2" : {"name":"user_2", "passw":"1234", "activity":"inactive", "status":"unblocked"} },

  "channels":{
    "0001": {
      "party":{ "None":{}, 
                "user_1":{'rank':'admin', 'status':'unmute'}, 
                "user_2":{'rank':'participant', 'status':'unmute'}},
      "msgs": {
        "1": { "name":"user_1", "num":1, "msg": "svo0", "time": "07-31 15:36:29"}, 
        "2": { "name":"user_2", "num":1, "msg": "svo1", "time": "07-31 15:36:29"} } }
        }
    }

# вывод в цикле до конца ввсех сообщений а затем поле ввода, если ввод "" то выход, если " " то обновление истории, все что иначе записывается как сообщение

def read_local():
  try: 
    with open('local.json', 'r', encoding='utf-8') as file:
      data = json.load(file)
      local.clear()
      local.update(data)
  except FileNotFoundError: print('файл "local" не найден'), time.sleep(1)

def write_local() : 
  with open('local.json', 'w', encoding='utf-8') as file:  
    json.dump(local, file, ensure_ascii=False, indent=2)



def write() : 
  with open('smski.json', 'w', encoding='utf-8') as file:  
    json.dump(smss, file, ensure_ascii=False, indent=2)

def read() :
  try: 
    with open('smski.json', 'r', encoding='utf-8') as file:
      data = json.load(file)
      smss.clear()
      smss.update(data)
  except FileNotFoundError: print('файл "smski" не найден'), time.sleep(1)


def _exit(): 
  print(log), time.sleep(1)
  try: del smss['sessions'][str(log[3])]
  except KeyError: print("сессия не найдена"), time.sleep(0.4)
  smss['users'][log[1]]['activity'] = "inactive" 
  update_write_local = write_local()
  update_write = write()
  flag[1] = True
  print('сохранение'), time.sleep(0.5)
  sys.exit()

@atexit.register
def on_exit():
    if flag[1] == True: pass
    else:
      print("завершаемся"), time.sleep(0.3)
      safe_exit = _exit() 


def complain():
  while True:
    print('[1] - Просмотреть свои жалобы') 
    new_complain = input("Опишите вашу проблему: ") 
    if new_complain == ' ': break
    elif new_complain == '1': 
      _read = read()
      for n in smss['complaints']:
        if log[0] == smss['complaints'][n]['name']:
          print('['+smss['complaints'][n]['time']+']','['+smss['complaints'][n]['status']+']','@'+smss['complaints'][n]['name'],':',smss['complaints'][n]['complain']), time.sleep(0.1)
    else: 
      smss['complaints'][len(smss['complaints'])] = {'name':log[0],'complain':new_complain,'answer':'none','status':'new', 'time':str(datetime.datetime.now())[:-10]}
      update_write = write()
      print("сообщение переданно администратору"), time.sleep(1)
      break


def admin_menu():
  while True:
    #admin_key = input("key: ")
    _read = read()
    command = input(">_ ")
    if command == 'help':
      print("base - вывести всю базу") 
      print("users - список всех пользователей")
      print("channels - список всех каналов ")
      print("complains - список жалоб\n")
      print("id search - поиск по айди")
      print("name search - поиск по имени")
      print("ban - блокировка  пользователя")
      print("unban - разблокировка пользователя")
      print("del user - удаление пользователя")
      print("del channel - удаление канала")
    if command == "base": print(smss)
    elif command == "users": 
      for j in smss['users']: print(j, smss['users'][j])
    elif command == "channels": 
      for ch in smss['channels']: print(ch)
    elif command == "complains": 
      _read = read()
      num = 0
      if len(smss['complaints']) > 0:
        for com in smss["complaints"]: 
          print('['+smss['complaints'][com]['time']+']','['+smss['complaints'][com]['status']+']','@'+smss['complaints'][com]['name'],':',smss['complaints'][com]['complain']), time.sleep(0.1)
          num += 1
      else: print("none")
      print("[1] - Выбрать\n[2] - Назад")
      de = input(">> ")
      if de == '1': 
          _read = read()
          num_com = input("номер жалобы: ")
          if num_com in smss['complaints']: 
            print(' @'+smss['complaints'][num_com]['name'],smss['complaints'][num_com]['complain'], "\n[1] - Ответить\n[2] - Назад")
            de = input(">> ")
            if de == "1":
              answer = input("ответ: ")
              smss['complaints'][num_com]['answer'] = answer
              print('[1] - Статус "отвечен"')
              de = input("> ")
              if de == "1": smss['complaints'][num_com]['status'] = "completed"
              else: continue
              if answer == " ": break
              update_write = write()
            elif de == '2': continue
          else: print("нету такой")
      elif de == '2': continue
    elif command == "id search":
      id_search = input("id: ")
      if id_search in smss['users']: print(id_search, smss['users'][id_search])
      else: print("нету такого"), time.sleep(0.2)
    elif command == 'name search':
      name = input("имя: ")
      for id1 in smss['users']:
        if name == smss['users'][id1]['name']:
          print("нашли \n", smss['users'][id1][name])
      else: print("никого не нашли")
    elif command == "ban":
      id1 = input("id: ")
      if id1 in smss['users']:
        print(f"пользователь {id1} {smss['users'][id1]['name']} заблокирован")
        smss['users'][id1]['status'] = 'blocked'
        update_write = write()
    elif command == "unban":
      id1 = input("id: ")
      if id1 in smss['users']:
        print(f"пользователь {id1} {smss['users'][id1]['name']} разблокирован")
        smss['users'][id1]['status'] = 'unblocked'
        update_write = write()
    elif command == "del user":
      id1 = input("id: ")
      if id1 in smss['users']:
        print(f"пользователь {id1} {smss['users'][id1]['name']} удалён")
        del smss['users'][id1]
        update_write = write()
    elif command == "del channel":
      c_name = input("название: ")
      if id1 in smss['users']:
        print(f"канал {c_name} удалён")
        del smss['channels'][c_name]
        update_write = write()
    elif command == "exit": break
    elif command == " ": break


def login():
  smss['sessions'].clear()
  while True:
    read_local()
    if local['status'] == "True":
      if flag[0] != 'change':
        print(1)
        log[0] = local['login']['name']
        log[1] = local['login']['id']
        log[2] = True
        log[3] = local['login']['num_session']
        num_session = len(smss['sessions'])
        smss["users"][log[1]]["activity"] = "active"
        smss["sessions"][num_session] = {'name':log[0], 'time':str(datetime.datetime.now())[:-10]}
        update_write = write()
        break
    #os.system("cls")
    else:
      data = read()
      user = input("name: ")
      s = False
      for user1 in smss["users"]:
        if user == smss["users"][user1]["name"]:
          s = 'svo'
          passw = input("passw: ")
          if passw == smss["users"][user1]["passw"]:
            if smss['users'][user1]['status'] == 'unblocked':
              print("вход успешный"), time.sleep(0.5)
              num_session = len(smss['sessions'])
              smss["users"][user1]["activity"] = "active"
              smss["sessions"][user] = {'name':user, 'time':str(datetime.datetime.now())[:-10]}
              local['status'] = "True"
              local['login'] = {"name":user,"id":user1,"num_session":num_session}
              update_write_local = write_local()
              update_write = write()
              s = True
              log[0] = user
              log[1] = user1
              log[2] = s
              log[3] = num_session
              break
            else: 
              log[0] = user
              print("ваша учетная запись заблокированна!")
              print("[1] - Обратиться в поддержку")
              de = input("> ")
              if de == '1': complain()
          else: print("неправильно")
    if s == False: 
      print("нету таких"), time.sleep(1)
      continue
    elif s == True: break


def menu() :
  user, user1, s, num_session = log
  while s == True:
    os.system('cls')
    if user in smss["admins"]: print("[admin]","@"+ user)
    else: print(" @",user)
    try: channel = input('channel : ')
    except KeyboardInterrupt: _exit()
    read_sms = read()
    if channel == 'rename':
      rename = input("новое имя: ")
      if len(rename) > 1 and len(rename) < 20:
        for j in smss['users']:
          print(j)
          print(smss['users'][j])
          if rename == smss['users'][j]['name']:
            print('есть такой уже'), time.sleep(1)
            return 'in_the_dict'
        smss['users'][user1]['name'] = rename
        if user in smss['admins']:
          del smss['admins'][user]
          smss['admins'][rename] = rename
        user = rename
        update_write = write()
        continue
      else: print("имя должно содержать не менее 1го и не более 20 символов"), time.sleep(1.5)
    if channel == 'repassw':
      repassw = input('новый пароль: ')
      if len(repassw) > 3 and len(repassw) < 30:
        smss['users'][user1]['passw'] = repassw 
        update_write = write()
        continue
      else: print("пароль должен содержать не менее 3 и не более 30 символов"), time.sleep(1.5)
    elif channel == 'change': return 'change'
    elif channel == 'exit': safe_exit = _exit()
    elif channel == ' ': safe_exit = _exit()
    elif channel == 'support': complain()
    elif channel == 'admin': 
      if user in smss['admins']: admin_menu()
    elif channel in smss['channels']: 
      if user in smss['channels'][channel]["party"] or user in smss["admins"]:
          while True:
           os.system('cls')
           read_sms = read()
           print(Fore.YELLOW+" Channel :", channel, Style.RESET_ALL)
           for smska in smss['channels'][channel]['msgs']:
             if smss['channels'][channel]['msgs'][smska]['name'] == user:
              print('['+smss['channels'][channel]['msgs'][smska]['time']+']',Fore.GREEN+'@'+smss['channels'][channel]['msgs'][smska]['name']+':',smss['channels'][channel]['msgs'][smska]['msg'],Style.RESET_ALL)
             else: 
              print('['+smss['channels'][channel]['msgs'][smska]['time']+']',Fore.BLUE+'@'+smss['channels'][channel]['msgs'][smska]['name']+':',smss['channels'][channel]['msgs'][smska]['msg'],Style.RESET_ALL)
             time.sleep(0.05)
           new_msg = input('>> ')
           if new_msg == '': continue
           elif new_msg == ' ': break
           elif new_msg == 'leave':
              if user in smss['channels'][channel]['party']:
                del smss['channels'][channel]['party'][user]
                print("вы покинули беседу")
                print(smss['channels'][channel]), time.sleep(1)
                write()
                break
              else: break
           elif new_msg == 'clear':
            if user in smss['channels'][channel]['party']:
              if smss['channels'][channel]['party'][user]['status'] == "unmute" or user in smss['admins']:
                smss['channels'][channel]['msgs'].clear()
                print("история обнулена"), time.sleep(1)
                write_sms = write()
              else: print("вы замьючены"), time.sleep(1)
            if user in smss['admins']:
              smss['channels'][channel]['msgs'].clear()
              print("история обнулена"), time.sleep(1)
              write_sms = write()
           else: 
            if user in smss['channels'][channel]['party']:
              if smss['channels'][channel]['party'][user]['status'] == "unmute":
                if len(smss['channels'][channel]['msgs']) > 0: 
                  num = int(tuple(smss['channels'][channel]['msgs'])[-1])+1
                  num1 = int(tuple(smss['channels'][channel]['msgs'])[-1])+1
                else: num = 0
                smss['channels'][channel]['msgs'][num] = {'name':user,'num':num,'msg':new_msg,'time':str(datetime.datetime.now())[5:-7]}
                write_sms = write()
                continue  
            if user in smss['admins']:
                if len(smss['channels'][channel]['msgs']) > 0: 
                  num = int(tuple(smss['channels'][channel]['msgs'])[-1])+1
                  num1 = int(tuple(smss['channels'][channel]['msgs'])[-1])+1
                else: num = 0
                smss['channels'][channel]['msgs'][num] = {'name':user,'num':num,'msg':new_msg,'time':str(datetime.datetime.now())[5:-7]}
                write_sms = write()
                continue
              #print(smss), time.sleep(2)
            else: print('вы замьючены'), time.sleep(1)
      else: print(f'пользователь @{user} не состоит в беседе'), time.sleep(1)
    else: print("нету таких"), time.sleep(1)
    if channel == "help":
      print(' меню:')
      print('/rename - смена имени')
      print('/repassw - сменя пароля')
      print('/change - смена ученой записи')
      print('/exit - выход из программы')
      print('/support - написать в поддержку')
      print('/create - создание канала')
      print('/del channel - удаление своего канала')
      print(' чат:')
      print('пустой ввод - обновление истории')
      print('пробел - выход в меню')
      print('/party - список участников')
      print('/clear - чистка истории')
      print('/leave - покинуть чат')
      print(' админские команды в чате:')
      print('/add <name> - добавить участника')
      print('/kick <name> - выгнать участника')
      print('/mute <name> - замутить участника')
      print('/unmute <name> - размутить участника')

      input()


def main ():  # центральная догма
  while True:
    flag = [None]
  
    def main_login (): 
        a1 = login()
    def main_menu ():
      while True:
        a2 = menu()
        if a2 == 'change': return 'change'
        if a2 == 'leave': continue
        if a2 == 'svo_1': continue
        if a2 == 'svo_2': break
        if a2 == 'in_the_dict': flag[0] = 'in_the_dict'
        break

    while True: # основной исполняемый алгоритм
      time.sleep(0.01)
      _read_local = read_local()
      _read = read()
      if flag == 'in_the_dict':
          b2 = main_menu()
          break
          #if b2 == 'login': continue
      else: 
          b1 = main_login()
          b2 = main_menu()
          if b2 == 'change':
            flag[0] = 'change'
          break
      


main_1 = main()


