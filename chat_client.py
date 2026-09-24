# Sahur-PTU Chat / v 0.3.2 / 18.08.2026

import os
import sys
import json
import time
import datetime
import subprocess
import threading
import atexit

from colorama import init, Fore, Back, Style

import auto_history 

# Правки:
# 1. Пофиксить ограничения для админов и статус владельца 
# 2. Запретить админу удалять свой же аккаунт через панель админа 
# 3. Добавить переменные с данными версии и добавить возможность узнавать их   *
# 4. Починить подгон параметров и сделать вариацию для телефона
# 5. Вычислять айди используя конвертирование айди последнего пользователя
# 6. Получше изолировать админ панель
# 7. Смену аккаунтов починить
# 8. Выбрать и наладить комбинированный режим
# 9. Нормальзовать работу потоков и их остановке по команде
# 10. Начать тестировку API
# 11. Сделать протокол полного отключения работы мессенджера прямо из клиента админа 

init()  
# os.system('mode con: cols=60 lines=17')
version = "sahur-chat / v 0.3.3 / 09.08.2026"
print(version) # сделать проверку на обновления 

#  /admin - открыть админ меню

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
mode = ["manual_update"]

forbidden = ['help','rename','repassw','change','exit',' ','support','create','rename chat','del chat','party','clear','leave','add','kick',
'mute','unmute','admins','base','users','channels','chats','sessions','support','id search','name search','ban','unban','del user','del channel']

local = {"login":{}, "status":"False", "settings":{"mode":"manual_update"}, "cache":{"channel":"0001", "username":"user_2"}}

smss = {
  "sessions" : {      
     "user_3" : {
        "ip": "none",
        "first": "2026-08-13 19:43",
        "last": "2026-08-13 19:43"} },
  "logs" : {},
  "updates" : {},
  "applications" : {},
  "support" : { 
    "user_2":{
      "number":"1",
      "username":"user_2",
      "adminname":"",
      "msgs":{ "1": { "name":"user_2", "num":1, "msg": "почему на реботает смена аккаунтов?", "time": "09-06 16:36:29"}, } } },
  
  "admins": {"user_1" : "user_1"},
  "users": { "1" : {"id": "1", "name":"user_1", "passw":"1234", "activity":"inactive", "status":"unblocked", "reg_date":""},
             "2" : {"id": "2", "name":"user_2", "passw":"1234", "activity":"inactive", "status":"unblocked", "reg_date":""},
             "3" : {"id": "3", "name":"user_3", "passw":"1234", "activity":"inactive", "status":"unblocked", "reg_date":""} },

  "channels":{
    "0001": {
      "chat_name":"0001",
      "party": { "user_1" : {'rank':'owner', 'status':'unmute'}, 
                 "user_2" : {'rank':'participant', 'status':'unmute'}},
      "msgs": {
        "1": { "name":"user_1", "num":1, "msg": "svo0", "time": "07-31 15:36:29"}, 
        "2": { "name":"user_2", "num":1, "msg": "svo1", "time": "07-31 15:36:29"} } }
        }
    }

parameters = {'system':"none", 'clearOutput':'none','runFile':'none'}
def crossPlatform():
  global parameters
  if sys.platform == "win32": parameters = {'system': "win32", 'clearOutput': "cls", 'runFile': "os.startfile"}
  if sys.platform == "darwin": parameters = {'system': "drawin", 'clearOutput':"clear",'runFile': "subprocess.run"}
  if sys.platform == "xdg-open": parameters = {'system': "xdg-open", 'clearOutput':"clear", 'runFile': "subprocess.run"}

# вывод в цикле до конца ввсех сообщений а затем поле ввода, если ввод "" то выход, если " " то обновление истории, все что иначе записывается как сообщение

def error(err, sec): # функция обработки ошибки
  #errors = [['001', ],]
  print(f"ошибка : {err}"); time.sleep(sec)

# os.mkdir('data')

def write_local() : # запись локальных данных
  with open('data/local.json', 'w', encoding='utf-8') as file:  
    json.dump(local, file, ensure_ascii=False, indent=2)

def read_local(): # чтение локальных данных
  try: 
    with open('data/local.json', 'r', encoding='utf-8') as file:
      new_data = json.load(file)
      local.clear(); local.update(new_data)
  except FileNotFoundError: 
    print('файл "local.json" не найден'); time.sleep(1)
    _write_local = write_local(); print("создан в локальной папке"); time.sleep(1)


def write() : # запись данных
  with open('data/smski.json', 'w', encoding='utf-8') as file:  
    json.dump(smss, file, ensure_ascii=False, indent=2)

def read() : # чтение данных
  try: 
    with open('data/smski.json', 'r', encoding='utf-8') as file:
      new_data = json.load(file)
      smss.clear(); smss.update(new_data)
  except FileNotFoundError: 
    print('файл "smski.json" не найден'); time.sleep(1)
    _write = write(); print("создан в локальной папке"); time.sleep(1)


def _exit(): # безопасный выход
  print(log), time.sleep(0.5)
  if log[1] in smss['users']: smss['users'][log[1]]['activity'] = "inactive" 
  update_write_local = write_local()
  update_write = write()
  flag[1] = True
  print('сохранение'); time.sleep(0.5)
  sys.exit()

@atexit.register
def on_exit(): # отслеживание выхода
    if flag[1] == True: pass
    else:
      print("завершаемся"); time.sleep(0.5)
      safe_exit = _exit() 

def check_admin(channel, username) : # сверка имени админа в базе
  if username in smss['admins']: return "in_sahur_admins"
  if smss['channels'][channel]['party'][username]['rank'] == 'admin': return "true_admin"
  if smss['channels'][channel]['party'][username]['rank'] == 'owner': return "true_owner"
  else: return "fake"

def system_msg(chat_name, msg) : # отправка системного сообщения
    num = len(smss['channels'][chat_name]['msgs']) + 1
    smss['channels'][chat_name]['msgs'][num] = {'name':'sys','num':num,'msg':msg,'time':str(datetime.datetime.now())[5:-7]}
    update_write = write()

def support_chat(chat_n): # чат с поддержкой 
  while True:
    os.system(parameters['clearOutput'])
    _read = read()
    if chat_n in smss['support']:
        print(Fore.YELLOW,"support chat :", chat_n, Style.RESET_ALL)
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
      num = len(smss['support'])
      smss['support'][chat_n] = {"number":num,"username":log[0],"adminname":"","msgs":{"1":{'name':'sys','num':num,'msg':'новый чат','time':str(datetime.datetime.now())[5:-7]} }}
      update_write = write()
      continue



def api() : # обмен с сервером
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


def admin_menu(): # админ панель
  while True:
    #admin_key = input("key: ")
    _read = read()
    command = input(">_ ")
    if command == 'help': # шпоргалка админа
      print("/base - вывести всю базу") 
      print("/users - список всех пользователей")
      print("/admins - список всех админов")
      print("/channels - список всех каналов ")
      print("/sessions - список всех активных сессий")
      print("/applications - список заявок на регистрацию")
      print("/support - чаты поддержки\n")
      print("/id search - поиск по айди")
      print("/name search - поиск по имени")
      print("/ban - блокировка  пользователя")
      print("/unban - разблокировка пользователя")
      print("/del user - удаление пользователя")
      print("/del channel - удаление канала")
    if command == "base" or command == '/base': # вывод всей базы
      for dataSUBBLOK in smss:
        print('*',dataSUBBLOK, ':'); time.sleep(0.1)
        for dataLINE in smss[dataSUBBLOK]:
          print(' ', smss[dataSUBBLOK][dataLINE])
    elif command == "users" or command == '/users': # список пользователей
      for j in smss['users']: print(j, smss['users'][j]); time.sleep(0.01)
    elif command == "admins" or command == '/admins': # список админов
      for j in smss['admins']: print(j, smss['admins'][j]); time.sleep(0.01)
    elif command == "channels" or command == '/channels': # список чатов
      for chat_name in smss['channels']:
          for sms in smss['channels'][chat_name]['msgs']: pass
          print(' ['+smss['channels'][chat_name]['chat_name']+']',':',smss['channels'][chat_name]['msgs'][sms]['msg'][0:30]+'...'); time.sleep(0.05)
    elif command == "sessions" or command == '/sessions': # список сессий
      for j in smss['sessions']: print('['+j+']\n', 'first :',smss['sessions'][j]['first'],'\n last  :',smss['sessions'][j]['last']); time.sleep(0.05)
    elif command == "applications" or command == '/applications': # список зачвок на регистрацию
      for applc in smss['applications']:
        print('',smss['applications'][applc]['num'], smss['applications'][applc]); time.sleep(0.05)
      applc1 = input("номер заявки: ")
      if applc1 in smss['applications']:
        print(smss['applications'][applc1], "\n[1] - Одобрить\n[2] - Отклонить")
        de = input(" > ")
        if de == '1':
          for id_user in smss['users']: id1 = str(int(smss['users'][id_user]['id']) + 1)
          smss['users'][id1] = {"id":id1, "name":smss['applications'][applc1]['name'], "passw":smss['applications'][applc1]['passw'],
                                "activity": "inactive", "status": "unblocked", "reg_date": str(datetime.datetime.now())[:-10] }
          del smss['applications'][applc1]
          update_write = write()
          print("пользователь успешно добавлен!"); time.sleep(1)
        else: pass
      else: print("нету такой"); time.sleep(1)
    elif command == "support" or command == '/support': # меню поддержки
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
          support_chat(chat_n)
      else: print("нету такого чата")
    elif command == "id search" or command == '/id search': # поиск по айди
      id_search = input("id: ")
      if id_search in smss['users']: print(id_search, smss['users'][id_search])
      else: print("нету такого"); time.sleep(0.2)
    elif command == 'name search' or command == '/name search': # поиск по имени
      name = input("имя: ")
      for id1 in smss['users']:
        if name == smss['users'][id1]['name']:
          print("нашли \n", smss['users'][id1])
          flag[3] = "allowed"
      if flag[3] != "allowed": print("никого не нашли")
    elif command == "ban" or command == '/ban': # блокировка пользователя
      id1 = input("id: ")
      if id1 in smss['users']:
        print(f"пользователь {id1} {smss['users'][id1]['name']} заблокирован")
        smss['users'][id1]['status'] = 'blocked'
        update_write = write()
    elif command == "unban" or command == '/unban': # разблокировка пользователя
      id1 = input("id: ")
      if id1 in smss['users']:
        print(f"пользователь {id1} {smss['users'][id1]['name']} разблокирован")
        smss['users'][id1]['status'] = 'unblocked'
        update_write = write()
    elif command == "del user" or command == '/del user': # удаление пользователя
      id1 = input("id: ")
      if id1 in smss['users']:
        del_username = smss['users'][id1]['name']
        print(f"{Fore.RED}точно удалить все данные пользователя [{id1}] @{del_username}?{Fore.RESET}")
        de = input(" Y/N ? : ")
        if de == 'y' or de == 'Y':
          l_f_a = leave_from_acc(log[0], log[1])
          del smss['users'][id1]
          update_write = write()
          print(f"пользователь {id1} {del_username} удалён"); time.sleep(1)
          if id1 == log[1]: 
            return "back_in_start_menu"
        else: continue
    elif command == "del channel" or command == '/del channel': # удаление чата
      c_name = input("название: ")
      if c_name in smss['channels']:
        print(f"канал {c_name} удалён")
        del smss['channels'][c_name]
        update_write = write()
      else: print("нет таких")
    elif command == "exit" or command == "/exit" or command == " ": break # выход из админ-панели


def login(): # авторизация
  def login_1(): # авторизация с нуля
    while True:
      data = read()
      user = input("name: ")
      if user == " ": return "exit"
      s = False
      for user1 in smss["users"]:
        if user == smss["users"][user1]["name"]:
          s = 'svo'
          passw = input("passw: ")
          if passw == smss["users"][user1]["passw"]:
            if smss['users'][user1]['status'] == 'unblocked':
              print("вход успешный"); time.sleep(0.5)
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
              if de == '1': support_chat(user)
          else: print("неправильно")
      if s == False: 
         print("нету таких"); time.sleep(1)
         continue
      elif s == True: break
  #os.system(parameters['clearOutput'])
  while True:
    _read_local = read_local()
    _read = read()
    if local['status'] == "True" and len(local['login']) > 2: # проверка на наличия сохранения логина в локальном хранилище
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
          if _login_1 == "allowed" or _login_1 == "exit": break
      else: 
        _login_1 = login_1()
        if _login_1 == "allowed" or _login_1 == "exit": break
    else: 
      _login_1 = login_1()
      if _login_1 == "allowed" or _login_1 == "exit": break

def registration() : # регистрация
  while True:
    try:
      name = input("введите имя: ")
      if name == " ": return "exit"
      passw = input("придумайте пароль: ")
      if passw == " ": return "exit"
      if len(passw) > 3 and len(passw) < 30:
        for id_users in smss['users']:
          if name == smss['users'][id_users]['name']:
            print("пользователь с таким именем уже есть"); time.sleep(1)
            break
        else:
          num = str(len(smss['applications']) + 1) 
          smss['applications'][num] = {"num":num,"name":name, 'passw':passw, "time":str(datetime.datetime.now())[5:-7]} 
          update_write = write()
          print("заявка на регистрацию успешно отправлена!"); time.sleep(1)
          print("модерация мессенджера рассмотрит её в ближайшее время"); time.sleep(1.5)
          return "allowed"
      else: print("пароль должен содержать не менее 3-х и не более 30 символов"); time.sleep(1.5)
    except KeyboardInterrupt: break

def commands(channel, user, user1) :
  #try:
    if channel == '/version': print(version); input("< ")

    elif channel == '/settings': 
        print("[1] - Режим отображения истории"); time.sleep(0.1)
        print("[2] - Назад"); time.sleep(0.1)
        de = input("> ")
        if de == '1': 
          print("[1] - Ручное обновление"); time.sleep(0.1)
          print("[2] - Отдельное окно"); time.sleep(0.1)
          print("[3] - Комбинированный"); time.sleep(0.1)
          de == input(">> ")
          if de == '1': local['settings']['mode'] = "manual_update"
          elif de == '2': local['settings']['mode'] = "separate_update"
          elif de == '3': local['settings']['mode'] = "auto_update"
          else: return 'continue'
          _write_local = write_local()
          print("настройки сохранены"); time.sleep(1)
        elif de == '2' or de == ' ': return 'continue'


    elif channel == '/channels': # список чатов
      for chat_name in smss['channels']:
          if user in smss['channels'][chat_name]['party']:
            for sms in smss['channels'][chat_name]['msgs']: pass
            print(' ['+smss['channels'][chat_name]['chat_name']+']',':',smss['channels'][chat_name]['msgs'][sms]['msg'][0:30]+'...'); time.sleep(0.05)
      input("< ")
      return 'continue'

    elif channel == '/rename': # смена имени
      rename = input("новое имя: ")
      if len(rename) > 1 and len(rename) < 20: 
        if rename not in forbidden:
          for j in smss['users']:
            if rename == smss['users'][j]['name']:
              print('есть такой уже'), time.sleep(1)
              return 'in_the_dict'
          if user in smss['support']:
            print("ого, даже в поддержку писал"); time.sleep(0.5)
            support_chat_data = smss['support'][user]
            del smss['support'][user]
            smss['support'][rename] = support_chat_data
            smss['support'][rename]['username'] = rename
            print(smss['support'][rename]); time.sleep(5)
          smss['users'][user1]['name'] = rename
          session_data = smss['sessions'][user]
          del smss['sessions'][user]
          smss['sessions'][rename] = session_data
          local['login']['name'] = rename
          user = rename
          log[0] = rename
          for chat_name in smss['channels']:
            if user in smss['channels'][chat_name]['party']:
              print("нашли бегунка"); time.sleep(0.3)
              print(smss['channels'][chat_name]['party'][user]); time.sleep(0.5)
              del smss['channels'][chat_name]['party'][user]
              smss['channels'][chat_name]['party'][rename] = {'name':rename,'rank':'participant','status':'unmute'}
              break
          else: print('не, нету в чатах'); time.sleep(0.5)
          if user in smss['admins']:
            del smss['admins'][user]
            smss['admins'][rename] = rename
          print("имя изменено!"); time.sleep(1)
          update_write = write()
          update_write_local = write_local()
          return 'continue'
        else: 
          print("имя не может содержать системные команды и флаги"); time.sleep(2)
          return 'continue'
      else: 
        print("имя должно содержать не менее 1-го и не более 20 символов"); time.sleep(2)
        return 'continue'

    elif channel == '/repassw': # смена пароля
      repassw = input('новый пароль: ')
      if len(repassw) > 3 and len(repassw) < 30:
        smss['users'][user1]['passw'] = repassw 
        update_write = write()
        print("пароль успешно изменён!"); time.sleep(1)
        return 'continue'
      else: print("пароль должен содержать не менее 3-х и не более 30 символов"); time.sleep(1.5)

    elif channel == '/change': # смена учётки
        l_f_a = leave_from_acc(log[0], log[1])
        return "back_in_start_menu"

    elif channel == '/exit' or channel == ' ': safe_exit = _exit() # безопасный выход

    elif channel == '/support': support_chat(user) # чат с поддержкой

    elif channel == '/create': # создание чата
      chat_name = input("название чата: ")
      if len(chat_name) > 1 and len(chat_name) < 20:
        if chat_name not in forbidden:
          smss['channels'][chat_name] = {'chat_name':chat_name,'party':{log[0]:{"rank":"owner","status":"unmute"}}, 'msgs':{}}
          _system_msg = system_msg(chat_name, "новый чат")
          print("чат успешно создан!"); time.sleep(1)
        else: print("имя не может содержать системные команды и флаги"); time.sleep(2)
      else: print("название должено содержать не менее 1-го и не более 20 символов"); time.sleep(1.5)
    
    elif channel == "/del channel": # удаление своего чата
      chat_name = input("название: ")
      if chat_name in smss['channels']:
        if user in smss['channels'][chat_name]['party']:
          if smss['channels'][chat_name]['party'][user]['rank'] == 'admin':
              del smss['channels'][chat_name]
              update_write = write()
              print(f"канал {chat_name} удалён"); time.sleep(1)
          else: print("вы не являетесь владельцем этого чата"); time.sleep(1)
        else: print("вы не в списке данного чата"); time.sleep(1)
      else: print("не существует такого чата"); time.sleep(1)

    elif channel == '/rename channel': # смена имени своего чата
      chat_name = input("текущее название чата: ")
      if chat_name in smss['channels']:
        if user in smss['channels'][chat_name]['party']:
          if smss['channels'][chat_name]['party'][user]['rank'] == "owner":
            rename_chat = input("новое название: ")
            if len(rename_chat) > 1 and len(rename_chat) < 20:
              smss['channels'][chat_name]['chat_name'] = rename_chat
              chat_data = smss['channels'][chat_name]
              smss['channels'][rename_chat] = chat_data
              del smss['channels'][chat_name]
              _system_msg = system_msg(rename_chat, "чат переименован")
              print("чат успешно переименован!"); time.sleep(1)
            else: print("название должено содержать не менее 1-го и не более 20 символов"); time.sleep(1.5)
          else: print("вы не владелец чата"); time.sleep(1.5)
        else: print("вы не состоите в этом чате"); time.sleep(1.5)
      else: print("такого чата не существует"); time.sleep(1.5)

    elif channel == '/admin' or channel == 'admin': # админ-панель
      if user in smss['admins']: admin_menu()

    else: 
      print("такой команды не существует"); time.sleep(1)

def channel_commands(channel, user, user1, new_msg):
            if new_msg == '/leave' or new_msg == '/leave ': # покидание чата
                if user in smss['channels'][channel]['party']:
                  del smss['channels'][channel]['party'][user]
                  print("вы покинули беседу")
                  print(smss['channels'][channel]); time.sleep(1)
                  _system_msg = system_msg(channel, f"@{user} покинул чат")
                  return 'break'
                else: return 'break'

            elif new_msg.startswith('/del'): # удаление сообщения
              elms_command = new_msg.split(" ")
              if len(elms_command) > 1: del_num = elms_command[1]
              else: return 'error_command' 
              if del_num in smss['channels'][channel]['msgs']:
                  _chek_admin = check_admin(channel, user)
                  if smss['channels'][channel]['msgs'][del_num]['name'] == user or _chek_admin == 'true_admin' or _chek_admin == 'true_owner' or _chek_admin == 'in_sahur_admins':
                    print('<'+smss['channels'][channel]['msgs'][del_num]['msg']+'>', 'удалено'); time.sleep(1)
                    smss['channels'][channel]['msgs'][del_num]['msg'] = "сообщение удалено"
                    update_write = write()
                  else: print("это не ваше сообщение"); time.sleep(1)
              else: print("нету такого сообщения"); time.sleep(1)

            elif new_msg == '/party' or new_msg == '/party ': # список участников чата
              print("участники чата:")
              for participant in smss['channels'][channel]['party']:
                print(' @'+participant, '['+smss['channels'][channel]['party'][participant]['rank']+']'); time.sleep(0.03)
              input("< ")

            elif new_msg == '/clear' or new_msg == '/clear ': # полная очистка истории чата
              if user in smss['channels'][channel]['party']:
                _chek_admin = check_admin(channel, user)
                if _chek_admin == 'true_admin' or _chek_admin == 'true_owner' or _chek_admin == 'in_sahur_admins':
                  if smss['channels'][channel]['party'][user]['status'] == "unmute" or user in smss['admins']:
                    smss['channels'][channel]['msgs'].clear()
                    _system_msg = system_msg(channel, "чат очищен")
                    write_sms = write()
                    print("история обнулена"); time.sleep(1)
                    return 'continue'
                  else: print("вы замьючены"); time.sleep(1)
                else: print("у вас недостаточно прав для таких махинаций"); time.sleep(1)

            elif new_msg.startswith('/add admin'): # выдача админки участнику
              elms_command = new_msg.split(" ")
              if len(elms_command) > 2: add_admin_name = elms_command[2]
              else: return 'error_command' 
              _chek_admin = check_admin(channel, user)
              if _chek_admin == 'true_owner' or _chek_admin == 'in_sahur_admins':
                if add_admin_name in smss['channels'][channel]['party']:
                  if smss['channels'][channel]['party'][add_admin_name]['rank'] != 'owner' or user in smss['admins']:
                    smss['channels'][channel]['party'][add_admin_name]['rank'] = 'admin'
                    _system_msg = system_msg(channel, f"@{add_admin_name} получил статус администратора")
                    update_write = write()
                    print(f"пользователь {add_admin_name} теперь админ!"); time.sleep(1)
                  else: print("вы не можете понизить владельца"); time.sleep(1)
                else: print("пользователь не состоит в беседе"); time.sleep(1.5)
              else: print("у вас недостаточно прав для таких махинаций"); time.sleep(1.5)

            elif new_msg.startswith('/add'): # добавление участника в чат
              elms_command = new_msg.split(" ")
              if len(elms_command) > 1: add_user_name = elms_command[1]
              else: return 'error_command' 
              _chek_admin = check_admin(channel, user)
              if _chek_admin == 'true_admin' or _chek_admin == 'true_owner' or _chek_admin == 'in_sahur_admins':
                for user_id in smss['users']:
                  if add_user_name == smss['users'][user_id]['name']:
                    if add_user_name in smss['channels'][channel]['party']: 
                      print("пользователь уже состоит в беседе"); time.sleep(1)
                      break
                    smss['channels'][channel]['party'][add_user_name] = {'rank':'participant','status':'unmute'}
                    _system_msg = system_msg(channel, f"@{add_user_name} добавлен в чат")
                    update_write = write()
                    print(f"пользователь {add_user_name} успешно добавлен!"); time.sleep(1)
                    break
                else: print("пользователя с таким именем не существует"); time.sleep(1.5)
              else: print("у вас недостаточно прав для таких махинаций"); time.sleep(1.5)

            elif new_msg.startswith('/demote'): # разжалование администратора
              elms_command = new_msg.split(" ")
              if len(elms_command) > 1: demote_name = elms_command[1]
              else: return 'error_command' 
              _chek_admin = check_admin(channel, user)
              if _chek_admin == 'true_owner' or _chek_admin == 'in_sahur_admins':
                if demote_name in smss['channels'][channel]['party']:
                  if smss['channels'][channel]['party'][demote_name]['rank'] == "admin":
                    print(smss['channels'][channel]['party'][demote_name]); time.sleep(1.5)
                    smss['channels'][channel]['party'][demote_name]['rank'] = "participant"
                    _system_msg = system_msg(channel, f"участник @{demote_name} разжалован")
                    update_write = write()
                    print(f"админ {demote_name} успешно разжалован!"); time.sleep(1)
                  else: print("участник не является администратором"); time.sleep(1)
                else: print("пользователь не состоит в этой беседе"); time.sleep(1) 
              else: print("у вас недостаточно прав для таких махинаций"); time.sleep(1)

            elif new_msg.startswith('/kick'): # исключение участника из чата
              elms_command = new_msg.split(" ")
              if len(elms_command) > 1: kick_user_name = elms_command[1]
              else: return 'error_command' 
              _chek_admin = check_admin(channel, user)
              if _chek_admin == 'true_admin' or _chek_admin == 'true_owner' or _chek_admin == 'in_sahur_admins':
                if kick_user_name in smss['channels'][channel]['party']:
                  if smss['channels'][channel]['party'][kick_user_name]['rank'] != "admin" or smss['channels'][channel]['party'][kick_user_name]['rank'] != "owner":
                      del smss['channels'][channel]['party'][kick_user_name]
                      _system_msg = system_msg(channel, f"@{kick_user_name} исключён из чата")
                      update_write = write()
                      print(f"пользователь {kick_user_name} успешно удалён из беседы!"); time.sleep(1)
                  else: print("нельзя удалять админов и владельцев"); time.sleep(1.5)
                else: print("пользователь не состоит в беседе"); time.sleep(1.5)
              else: print("у вас недостаточно прав для таких махинаций"); time.sleep(1.5)

            elif new_msg.startswith('/mute'): # мут участника в чате
              elms_command = new_msg.split(" ")
              if len(elms_command) > 1: mute_user_name = elms_command[1]
              else: return 'error_command' 
              _chek_admin = check_admin(channel, user)
              if _chek_admin == 'true_admin' or _chek_admin == 'true_owner' or _chek_admin == 'in_sahur_admins':
                if mute_user_name in smss['channels'][channel]['party']:
                  if smss['channels'][channel]['party'][mute_user_name]['rank'] != "admin" or smss['channels'][channel]['party'][user]['rank'] != 'owner':
                        smss['channels'][channel]['party'][mute_user_name]['status'] = 'mute'
                        _system_msg = system_msg(channel, f"@{mute_user_name} замьючен")
                        update_write = write()
                        print(f"пользователь {mute_user_name} успешно замьючен!"); time.sleep(1)
                  else: print("нельзя мутить админов"); time.sleep(1.5)
                else: print("пользователь не состоит в беседе"); time.sleep(1.5)
              else: print("у вас недостаточно прав для таких махинаций"); time.sleep(1.5)

            elif new_msg.startswith('/unmute'): # размут участника в чате
              elms_command = new_msg.split(" ")
              if len(elms_command) > 1: mute_user_name = elms_command[1]
              else: return 'error_command' 
              _chek_admin = check_admin(channel, user)
              if _chek_admin == 'true_admin' or _chek_admin == 'true_owner' or _chek_admin == 'in_sahur_admins':
                if mute_user_name in smss['channels'][channel]['party']:
                      smss['channels'][channel]['party'][mute_user_name]['status'] = 'unmute'
                      _system_msg = system_msg(channel, f"@{mute_user_name} размьючен")
                      update_write = write()
                      print(f"пользователь {mute_user_name} успешно размьючен!"); time.sleep(1)
                else: print("пользователь не состоит в беседе"); time.sleep(1.5)
              else: print("у вас недостаточно прав для таких махинаций"); time.sleep(1.5)

            else: 
              print("такой команды не существует"); time.sleep(1)
  #except: pass

def menu() : # основное меню
  user, user1, s, num_session = log
  while s == True:
    os.system(parameters['clearOutput'])
    read_sms = read()
    if user in smss["admins"]: print("[admin]","@"+ user)
    else: print(" @"+user)
    try: channel = input('channel : ')
    except KeyboardInterrupt: _exit()

    if channel == ' ' or channel == '  ': safe_exit = _exit()

    elif channel in smss['channels']: # открытие чата
        if mode[0] == "manual_update":
          if user in smss['channels'][channel]["party"] or user in smss["admins"]:
            while True:
              os.system(parameters['clearOutput'])
              read_sms = read()
              print(Fore.YELLOW+" Channel :", channel, Style.RESET_ALL)
              for smska in smss['channels'][channel]['msgs']:
                if smss['channels'][channel]['msgs'][smska]['name'] == user:
                  print('['+smss['channels'][channel]['msgs'][smska]['time']+']',Fore.GREEN+smska,'@'+smss['channels'][channel]['msgs'][smska]['name']+':',smss['channels'][channel]['msgs'][smska]['msg'],Style.RESET_ALL)
                else: # возможно добавить отключение отображения удалённых сообщений
                  print('['+smss['channels'][channel]['msgs'][smska]['time']+']',Fore.BLUE+smska,'@'+smss['channels'][channel]['msgs'][smska]['name']+':',smss['channels'][channel]['msgs'][smska]['msg'],Style.RESET_ALL)
                time.sleep(0.05)
              print("------------------------------------------")
              new_msg = input('>> ')
              if new_msg == '':  # обновление истории
                if user in smss['channels'][channel]['party']: continue
                else: 
                  print("вы были исключены"); time.sleep(1)
                  break
              elif new_msg == ' ': break # возврат в меню
              elif new_msg.startswith("/"):
                _channel_commands = channel_commands(channel, user, user1, new_msg)
                if _channel_commands == "continue": continue
                if _channel_commands == "break": break
                if _channel_commands == "error_command": _error  = error("неправильный ввод команды", 2)
              else: # запись нового сообщения
                if user in smss['channels'][channel]['party'] or user in smss['admins']:
                  if smss['channels'][channel]['party'][user]['status'] == "unmute":
                    num = len(smss['channels'][channel]['msgs']) + 1
                    smss['channels'][channel]['msgs'][num] = {'name':user,'num':num,'msg':new_msg,'time':str(datetime.datetime.now())[5:-7]}
                    write_sms = write()
                    continue
                  else: print('вы замьючены'); time.sleep(1)
                else: 
                  print("вы были исключены"); time.sleep(1)
                  return 'break'
          else: print(f'пользователь @{user} не состоит в беседе'); time.sleep(1)


        elif mode[0] == "separate_update":
            print("separate_update"); time.sleep(1)
            subprocess.Popen([r'D:\.Profile\Desktop\hackerskie_codi\Python\projects\history_msg.exe'])

        elif mode[0] == "auto_update": 
            print("auto_update"); time.sleep(1)
            auto_history.main()

    elif channel.startswith("/") or channel == "admin":
          _menu_commands = commands(channel, user, user1)
          if _menu_commands == "continue": continue
          if _menu_commands == "break": break
          if _menu_commands == "back_in_start_menu": return "back_in_start_menu"
    

    elif channel == "help" or channel == '/help': # шпоргалка 
      print(' меню:')
      print('/settings - меню настроек')
      print('/channels - список чатов в которых состоишь')
      print('/rename - смена имени')
      print('/repassw - сменя пароля')
      print('/change - смена учёной записи')
      print('/exit - выход из программы')
      print('/support - написать в поддержку')
      print('/create - создание канала')
      print('/rename channel - смена имени чата')
      print('/del channel - удаление своего канала')
      print(' чат:')
      print('пустой ввод - обновление истории')
      print('пробел - выход в меню')
      print('/party - список участников')
      print('/clear - чистка истории')
      print('/leave - покинуть чат')
      print(' админские команды в чате:')
      print('/add <имя> - добавить участника')
      print('/add admin <имя> - выдать админские права')
      print('/demote <имя> - разжаловать админа')
      print('/kick <имя> - выгнать участника')
      print('/mute <имя> - замутить участника')
      print('/unmute <имя> - размутить участника')
      print('Пробел практически во всех полях ввода - возврат назад')
      input("< ")
    else: print("нету таких"); time.sleep(1)

def leave_from_acc(name, _id):
        flag[0] = 'change'
        smss['users'][_id]['activity'] = "inactive"
        del smss['sessions'][name]
        local['login'].clear()
        local['status'] = "False"
        update_write_local = write_local()
        update_write = write()
        print(local); time.sleep(1)


def start_menu() : # начальное меню
  if local['status'] == 'True' and len(local['login']) > 2: return "loginned"
  while True:
    try:
      print("[1] - Вход")
      print("[2] - Регистрация")
      de = input(">> ")
      if de == " ": safe_exit = _exit()
      elif de == '1': return "login"
      elif de == '2': return "reg"
    except KeyboardInterrupt: break


def main ():  # центральная догма
  while True:
    flag_1 = [None]
    _crossPlatform = crossPlatform()
    def main_start() :
      while True: 
        a0 = start_menu()
        if a0 == "loginned": break
        elif a0 == 'login': return "login"
        elif a0 == 'reg': 
          r0 = registration()
          if r0 == 'exit': continue
          if r0 == 'allowed': continue
        else: pass
    
    def main_login() : 
        a1 = login()
        if a1 == "exit": return "exit"
    def main_menu() :
      while True:
        a2 = menu()
        if a2 == "back_in_start_menu": return "back_in_start_menu"
        if a2 == 'leave': continue
        if a2 == 'svo_1': continue
        if a2 == 'svo_2': break
        if a2 == 'in_the_dict': flag[0] = 'in_the_dict'
        break

    while True: # основной исполняемый алгоритм

      def loop_one(): # поток основной
       while not stop_event.is_set():
        while True:
          _read_local = read_local()
          _read = read()
          mode[0] = local['settings']['mode']
          if flag_1 == 'in_the_dict':
            b2 = main_menu()
            break
          else: 
            b0 = main_start()
            b1 = main_login()
            if b1 == "exit": continue
            b2 = main_menu()
            if b2 == "back_in_start_menu": continue
            break
      def loop_two(): # поток чтения
       while not stop_event.is_set():
        while True:
          time.sleep(1)
          _read_local = read_local()
          _read = read()

      stop_event = threading.Event()
      t1 = threading.Thread(target=loop_one) #, args=(stop_event,))
      t2 = threading.Thread(target=loop_two) # , args=(stop_event,))
      t1.start()
      t2.start()
      stop_event.set()
      t1.join()
      t2.join()
      _exit()

if __name__ == "__main__":
  main_1 = main()


