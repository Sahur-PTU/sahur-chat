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

# точечное удаление сообщений 

# постоянное фоновое чтение базы с сервера

# key/read
# key/write/msg

log = [None, None, None, None]
flag = [None, None, None, None]
errors = [None] 

local = {"login":{}, "status":"False"}

smss = {
  "sessions" : {      
     "user_3" : {
        "first": "2026-08-13 19:43",
        "last": "2026-08-13 19:43"} },
  "logs" : {},
  "updates" : {},
  "support" : { 
    "user_2":{
      "number":"1",
      "username":"user_2",
      "adminname":"",
      "msgs":{
        "1": { "name":"user_2", "num":1, "msg": "почему на реботает смена аккаунтов?", "time": "09-06 16:36:29"},
            } 
          } 
        },

  "admins": {"user_1" : "user_1"},
  "users": { "1" : {"name":"user_1", "passw":"1234", "activity":"inactive", "status":"unblocked"},
             "2" : {"name":"user_2", "passw":"1234", "activity":"inactive", "status":"unblocked"} },

  "channels":{
    "0001": {
      "party": { "None" : {}, 
                 "user_1" : {'rank':'admin', 'status':'unmute'}, 
                 "user_2" : {'rank':'participant', 'status':'unmute'}},
      "msgs": {
        "1": { "name":"user_1", "num":1, "msg": "svo0", "time": "07-31 15:36:29"}, 
        "2": { "name":"user_2", "num":1, "msg": "svo1", "time": "07-31 15:36:29"} } }
        }
    }

# вывод в цикле до конца ввсех сообщений а затем поле ввода, если ввод "" то выход, если " " то обновление истории, все что иначе записывается как сообщение

def error():
  print(f"ошибка {errors[0]}")

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
  except FileNotFoundError: 
    print('файл "smski" не найден'), time.sleep(1)
    _write = write()


def _exit(): 
  print(log), time.sleep(0.5)
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
      print("завершаемся"), time.sleep(0.5)
      safe_exit = _exit() 

def complain():
  while True:
    os.system("cls")
    _read = read()
    chat_n = log[0]
    if chat_n in smss['support']:
        print(Fore.YELLOW,"support chat :", log[0], Style.RESET_ALL)
        for smska in smss['support'][chat_n]['msgs']:
          if smss['support'][chat_n]['msgs'][smska]['name'] == log[0]:
            print('['+smss['support'][chat_n]['msgs'][smska]['time']+']',Fore.GREEN+'@'+smss['support'][chat_n]['msgs'][smska]['name']+':',smss['support'][chat_n]['msgs'][smska]['msg'],Style.RESET_ALL)
          else: 
            print('['+smss['support'][chat_n]['msgs'][smska]['time']+']',Fore.BLUE+'@'+smss['support'][chat_n]['msgs'][smska]['name']+':',smss['support'][chat_n]['msgs'][smska]['msg'],Style.RESET_ALL)
        new_msg = input(">> ")
        if new_msg == " ": return "exit"
        elif new_msg == "": continue
        elif new_msg == 'del': pass  
        else: 
          num = len(smss['support'][chat_n]['msgs']) + 1
          smss['support'][chat_n]['msgs'][num] = {'name':log[0],'num':num,'msg':new_msg,'time':str(datetime.datetime.now())[5:-7]}
          update_write = write()
          continue
    else: 
      if len(smss['support']) > 0: num = len(smss['support'])
      elif len(smss['support']) == 0: num = 1
      smss['support'][chat_n] = {"number":num, "username": log[0], "adminname":"", "msgs":{"1":{'name':'sys','num':num,'msg':'новый чат','time':str(datetime.datetime.now())[5:-7]} }}
      update_write = write()
      continue


def api() :
  try:
    def connect():
      pass
    def disconnect():
      pass
    def write_data_server():
      pass
    def read_data_server():
      pass

    def m_api() :
      while True:
        try: 
          pass
        except: pass

    def settings() :
      while True:
        try: 
          pass
        except: pass

  except: pass


def admin_menu():
  while True:
    #admin_key = input("key: ")
    _read = read()
    command = input(">_ ")
    if command == 'help':
      print("base - вывести всю базу") 
      print("users - список всех пользователей")
      print("channels - список всех каналов ")
      print("sessions - список всех активных сессий")
      print("support - чаты поддержки\n")
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
    elif command == "support": 
     while True:
      _read = read()
      if len(smss['support']) > 0:
        for user in smss["support"]: 
          if len(smss['support'][user]) > 0:
            if len(smss['support'][user]['msgs']) > 0:
              for sms in smss['support'][user]['msgs']:
                sms1 = smss['support'][user]['msgs'][sms]['msg']
              print(' ['+smss['support'][user]['username']+']',':',smss['support'][user]['msgs'][sms]['msg'][0:30]+'...')
            else: pass
          else: pass
      else: print("none")
      chat_n = input("название чата: ")
      _read = read()
      if chat_n == ' ': break
      if chat_n in smss['support']: 
          while True:
            os.system("cls")
            print(Fore.YELLOW,"support chat :", user, Style.RESET_ALL)
            for smska in smss['support'][chat_n]['msgs']:
              if len(smss['support'][chat_n]['msgs']) == 0: break
              if smss['support'][chat_n]['msgs'][smska]['name'] == log[0]:
                print('['+smss['support'][chat_n]['msgs'][smska]['time']+']',Fore.GREEN+'@'+smss['support'][chat_n]['msgs'][smska]['name']+':',smss['support'][chat_n]['msgs'][smska]['msg'],Style.RESET_ALL)
              else: print('['+smss['support'][chat_n]['msgs'][smska]['time']+']',Fore.BLUE+'@'+smss['support'][chat_n]['msgs'][smska]['name']+':',smss['support'][chat_n]['msgs'][smska]['msg'],Style.RESET_ALL)
            answer = input(">> ")
            if answer == ' ': break
            elif answer == '': continue
            elif answer == 'clear': 
              num = len(smss['support'][chat_n]['msgs'])+1
              smss['support'][chat_n]['msgs'].clear()
              smss['support'][chat_n]['msgs'] = {"1":{'name':'sys','num':num,'msg':'новый чат','time':str(datetime.datetime.now())[5:-7]} }
              update_write = write()
              continue
            else:
              num = len(smss['support'][chat_n]['msgs'])+1
              smss['support'][chat_n]['msgs'][num] = {'name':log[0],'num':num,'msg':answer,'time':str(datetime.datetime.now())[5:-7]}
              update_write = write()
              continue
      else: print("нету такого чата")
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
      if c_name in smss['channels']:
        print(f"канал {c_name} удалён")
        del smss['channels'][c_name]
        update_write = write()
      else: print("нет таких")
    elif command == "exit": break
    elif command == " ": break


def login():
  def login_1():
    while True:
      data = read()
      user = input("name: ")
      if user == " ": safe_exit = _exit()
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
              if user in smss['sessions']: first = smss['sessions'][user]['first']
              else: first = str(datetime.datetime.now())[:-10]
              smss["sessions"][user] = {'first':first, 'last':str(datetime.datetime.now())[:-10]}
              local['status'] = "True"
              local['login'] = {"name":user,"id":user1,"num_session":num_session}
              update_write_local = write_local()
              update_write = write()
              s = True
              log[0] = user
              log[1] = user1
              log[2] = s
              log[3] = num_session
              return "allowed"
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
  #os.system("cls")
  smss['sessions'].clear()
  while True:
    read_local()
    read()
    if local['status'] == "True":
      if flag[0] != 'change':
        if flag[0] != 'leave acc':
          log[0] = local['login']['name']
          log[1] = local['login']['id']
          log[2] = True
          log[3] = local['login']['num_session']
          num_session = len(smss['sessions'])
          smss["users"][log[1]]["activity"] = "active"
          if log[0] in smss['sessions']: first = smss['sessions'][log[0]]['first']
          else: first = str(datetime.datetime.now())[:-10]
          smss["sessions"][log[0]] = {'first':first, 'last':str(datetime.datetime.now())[:-10]}
          update_write = write()
          break
        else: 
          _login_1 = login_1()
          if _login_1 == "allowed": break
      else: 
        _login_1 = login_1()
        if _login_1 == "allowed": break
    else: 
      _login_1 = login_1()
      if _login_1 == "allowed": break
     


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
      else: print("имя должно содержать не менее 1-го и не более 20 символов"), time.sleep(1.5)
    if channel == 'repassw':
      repassw = input('новый пароль: ')
      if len(repassw) > 3 and len(repassw) < 30:
        smss['users'][user1]['passw'] = repassw 
        update_write = write()
        continue
      else: print("пароль должен содержать не менее 3-х и не более 30 символов"), time.sleep(1.5)
    elif channel == 'change': return 'change'
    elif channel == 'exit': safe_exit = _exit()
    elif channel == ' ': safe_exit = _exit()
    elif channel == 'support': complain()
    elif channel == 'create': 
      chat_name = input("название чата: ")
      if len(chat_name) > 1 and len(chat_name) < 20:
        smss['channels'][chat_name] = {'party':{log[0]:{"rank":"admin","status":"unmute"}}, 'msgs':{}}
        num = len(smss['channels'][chat_name]['msgs'])+1
        smss['channels'][chat_name]['msgs'][num] = {'name':'sys','num':num,'msg':'новый чат','time':str(datetime.datetime.now())[5:-7]}
        update_write = write()
        print("чат успешно создан!"), time.sleep(1)
      else: print("название должено содержать не менее 1-го и не более 20 символов"), time.sleep(1.5)
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
                print('['+smss['channels'][channel]['msgs'][smska]['time']+']',Fore.GREEN+smska,'@'+smss['channels'][channel]['msgs'][smska]['name']+':',smss['channels'][channel]['msgs'][smska]['msg'],Style.RESET_ALL)
              else: 
                print('['+smss['channels'][channel]['msgs'][smska]['time']+']',Fore.BLUE+smska,'@'+smss['channels'][channel]['msgs'][smska]['name']+':',smss['channels'][channel]['msgs'][smska]['msg'],Style.RESET_ALL)
              time.sleep(0.05)
            new_msg = input('>> ')
            if new_msg == '': continue
            elif new_msg == ' ': break
            elif new_msg == 'leave':
                if user in smss['channels'][channel]['party']:
                  del smss['channels'][channel]['party'][user]
                  print("вы покинули беседу")
                  print(smss['channels'][channel]), time.sleep(1)
                  num = len(smss['channels'][channel]['msgs'])
                  smss['channels'][channel]['msgs'][num] = {'name':'sys','num':num,'msg':f'@{user} покинул чат','time':str(datetime.datetime.now())[5:-7]}
                  update_write = write()
                  break
                else: break 
            elif new_msg == 'del': 
              del_num = input("номер сообщения: ")
              if del_num in smss['channels'][channel]['msgs']:
                if user == smss['channels'][channel]['msgs'][del_num]['name']:
                  print('<'+smss['channels'][channel]['msgs'][del_num]['msg']+'>', 'удалено'), time.sleep(1)
                  del smss['channels'][channel]['msgs'][del_num]
                  update_write = write()
                else: print("это не ваше сообщение"), time.sleep(1)
              else: print("нету такого сообщения"), time.sleep(1)
            elif new_msg == 'clear':
              if user in smss['channels'][channel]['party']:
                if smss['channels'][channel]['party'][user]['status'] == "unmute" or user in smss['admins']:
                  smss['channels'][channel]['msgs'].clear()
                  num = len(smss['channels'][channel]['msgs'])
                  smss['channels'][channel]['msgs'][num] = {'name':'sys','num':num,'msg':'новый чат','time':str(datetime.datetime.now())[5:-7]}
                  print("история обнулена"), time.sleep(1)
                  write_sms = write()
                  continue
                else: print("вы замьючены"), time.sleep(1)
              if user in smss['admins']:
                smss['channels'][channel]['msgs'].clear()
                num = len(smss['channels'][channel]['msgs'])
                smss['channels'][channel]['msgs'][num] = {'name':'sys','num':num,'msg':'новый чат','time':str(datetime.datetime.now())[5:-7]}
                print("история обнулена"), time.sleep(1)
                write_sms = write()
            elif new_msg == 'add':
              for user_in_chat in smss['channels'][channel]['party']:
                print(user_in_chat), time.sleep(0.3)
                if smss['channels'][channel]['party'][user_in_chat]['rank'] == 'admin': flag[0] = 'in_admins'
              if flag[0] == 'in_admins' or user in smss['admins']:
                add_user_name = input("имя пользователя: ")
                for num_user in smss['users']:
                  if add_user_name == smss['users'][num_user]['name']: 
                    smss['channels'][channel]['party'][add_user_name] = {'rank':'participant','status':'unmute'}
                    print(f"пользователь {add_user_name} успешно добавлен!"), time.sleep(1)
                    num = len(smss['channels'][channel]['msgs'])
                    smss['channels'][channel]['msgs'][num] = {'name':'sys','num':num,'msg':f'@{add_user_name} добавлен в чат','time':str(datetime.datetime.now())[5:-7]}
                    update_write = write()
                    flag[1] = 'in_users'
                  else: flag[1] = 'not_in_users'
                if flag[1] == 'not_in_users': print("пользователя с таким именем не существует"), time.sleep(1.5)
              else: print("у вас недостаточно прав для таких махинаций"), time.sleep(1.5)
            elif new_msg == 'kick':
              for user_in_chat in smss['channels'][channel]['party']:
                print(user_in_chat), time.sleep(0.3)
                if smss['channels'][channel]['party'][user_in_chat]['rank'] == 'admin': flag[0] = 'in_admins'
              if flag[0] == 'in_admins' or user in smss['admins']:
                kick_user_name = input("имя пользователя: ")
                for num_user in smss['users']:
                  if kick_user_name == smss['users'][num_user]['name']: 
                    if kick_user_name in smss['channels'][channel]['party']:
                      del smss['channels'][channel]['party'][kick_user_name]
                      print(f"пользователь {kick_user_name} успешно удалён из беседы!"), time.sleep(1)
                      num = len(smss['channels'][channel]['msgs'])
                      smss['channels'][channel]['msgs'][num] = {'name':'sys','num':num,'msg':f'@{kick_user_name} удалён из чата','time':str(datetime.datetime.now())[5:-7]}
                      update_write = write()
                      flag[1], flag[2] = 'in_users', 'in_party'
                    else: flag[2] = 'not_in_party'
                  else: flag[1] = 'not_in_users'
                if flag[1] == 'not_in_users': print("пользователя с таким именем не существует"), time.sleep(1.5)
                elif flag[2] == 'not_in_party': print("пользователь не состоит в беседе"), time.sleep(1.5)
              else: print("у вас недостаточно прав для таких махинаций"), time.sleep(1.5)
            elif new_msg == 'mute':
              for user_in_chat in smss['channels'][channel]['party']:
                print(user_in_chat), time.sleep(0.3)
                if smss['channels'][channel]['party'][user_in_chat]['rank'] == 'admin': flag[0] = 'in_admins'
              if flag[0] == 'in_admins' or user in smss['admins']:
                mute_user_name = input("имя пользователя: ")
                for num_user in smss['users']:
                  if mute_user_name == smss['users'][num_user]['name']: 
                    if mute_user_name in smss['channels'][channel]['party']:
                      smss['channels'][channel]['party'][mute_user_name]['status'] = 'mute'
                      print(f"пользователь {mute_user_name} успешно замьючен!"), time.sleep(1)
                      num = len(smss['channels'][channel]['msgs'])
                      smss['channels'][channel]['msgs'][num] = {'name':'sys','num':num,'msg':f'@{mute_user_name} замьючен','time':str(datetime.datetime.now())[5:-7]}
                      update_write = write()
                      flag[1], flag[2] = 'in_users', 'in_party'
                    else: flag[2] = 'not_in_party'
                  else: flag[1] = 'not_in_users'
                if flag[1] == 'not_in_users': print("пользователя с таким именем не существует"), time.sleep(1.5)
                elif flag[2] == 'not_in_party': print("пользователь не состоит в беседе"), time.sleep(1.5)
              else: print("у вас недостаточно прав для таких махинаций"), time.sleep(1.5)

            elif new_msg == 'unmute':
              for user_in_chat in smss['channels'][channel]['party']:
                print(user_in_chat), time.sleep(0.3)
                if smss['channels'][channel]['party'][user_in_chat]['rank'] == 'admin': flag[0] = 'in_admins'
              if flag[0] == 'in_admins' or user in smss['admins']:
                mute_user_name = input("имя пользователя: ")
                for num_user in smss['users']:
                  if mute_user_name == smss['users'][num_user]['name']: 
                    if mute_user_name in smss['channels'][channel]['party']:
                      smss['channels'][channel]['party'][mute_user_name]['status'] = 'unmute'
                      print(f"пользователь {mute_user_name} успешно размьючен!"), time.sleep(1)
                      num = len(smss['channels'][channel]['msgs'])
                      smss['channels'][channel]['msgs'][num] = {'name':'sys','num':num,'msg':f'@{mute_user_name} размьючен','time':str(datetime.datetime.now())[5:-7]}
                      update_write = write()
                      flag[1], flag[2] = 'in_users', 'in_party'
                    else: flag[2] = 'not_in_party'
                  else: flag[1] = 'not_in_users'
                if flag[1] == 'not_in_users': print("пользователя с таким именем не существует"), time.sleep(1.5)
                elif flag[2] == 'not_in_party': print("пользователь не состоит в беседе"), time.sleep(1.5)
              else: print("у вас недостаточно прав для таких махинаций"), time.sleep(1.5)
            else: 
              if user in smss['channels'][channel]['party']:
                if smss['channels'][channel]['party'][user]['status'] == "unmute":
                  num = len(smss['channels'][channel]['msgs'])
                  smss['channels'][channel]['msgs'][num] = {'name':user,'num':num,'msg':new_msg,'time':str(datetime.datetime.now())[5:-7]}
                  write_sms = write()
                  continue 
              if user in smss['admins']:
                num = len(smss['channels'][channel]['msgs'])
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
      print('/change - смена учёной записи')
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
    flag_1 = [None]
  
    def main_login (): 
        a1 = login()
    def main_menu ():
      while True:
        a2 = menu()
        if a2 == 'change': 
          flag[0] = 'change'
          smss['users'][log[1]]['activity'] = "inactive"
          del smss['sessions'][log[0]]
          local['login'].clear()
          local['status'] = "False"
          print(local), time.sleep(1)
          update_write_local = write_local()
          update_write = write()
        if a2 == 'leave': continue
        if a2 == 'svo_1': continue
        if a2 == 'svo_2': break
        if a2 == 'in_the_dict': flag[0] = 'in_the_dict'
        break

    while True: # основной исполняемый алгоритм
      time.sleep(0.01)
      _read_local = read_local()
      _read = read()
      if flag_1 == 'in_the_dict':
          b2 = main_menu()
          break
          #if b2 == 'login': continue
      else: 
          b1 = main_login()
          b2 = main_menu()
          break
      


main_1 = main()


