
import os
import json
import time
import datetime

# os.system('mode con: cols=60 lines=17')

# чтение из файла джесон и обновление по запросу

# key/read
# key/write/msg

#smss = {'0001' : {'user_1':{1:'in1',2:'in2'}, 
#                  'user_2':{1:'in01',2:'in02'}}
#        }

smss = {
  "0001": {
    "party":["None", "user_1", "user_2"],
    "msgs": {
      "1": { "name":"user_1", "num":1, "msg": "svo0", "time": "07-31 15:36:29"}, 
      "2": { "name":"user_2", "num":1, "msg": "svoasf0", "time": "07-31 15:36:29"} 
    },
  }
}

print(smss)
print(smss["0001"]['party'][1])
print('user_1' in smss["0001"]['party'])


def read() :
  try: 
    with open('smski.json', 'r', encoding='utf-8') as file:
      data = json.load(file)
      smss.clear()
      smss.update(data)
  except FileNotFoundError: print('файл не найден'), time.sleep(1)

def write() :
    with open('smski.json', 'w', encoding='utf-8') as file:
      json.dump(smss, file, ensure_ascii=False, indent=2)
  
read()
print(smss)

def menu() : 
  user = input("name: ")
  #passw = input("passw: ")
  while True:
    try: c = input('key/mode/action : ')
    except KeyboardInterrupt: menu()
    v = c.split("/")
    print(v)
    print(smss)
    read_sms = read()
    if v[0] in smss: 
      print(smss['0001']["party"])
      if user in smss[v[0]]["party"] and len(v)>1:
        for j in smss[v[0]]["msgs"]:
          print(j), time.sleep(0.2)
        if v[1] == 'read': 
          print(smss)
          for smska in smss[v[0]]['msgs']:
            print('['+smss[v[0]]['msgs'][smska]['time']+']','@'+smss[v[0]]['msgs'][smska]['name']+':',smss[v[0]]['msgs'][smska]['msg'])
            time.sleep(0.2)
        elif v[1] == 'write': 
          num = int(tuple(smss[v[0]]['msgs'])[-1])+1
          num1 = int(tuple(smss[v[0]]['msgs'])[-1])+1
          print(num, num1)
          print(num), time.sleep(0.5)
          smss[v[0]]['msgs'][num] = {'name':user,'num':num,'msg':v[2],'time':str(datetime.datetime.now())[5:-7]}
          write_sms = write()
          print(smss), time.sleep(2)
        else: print("нету такого режима")
      else: print(f'пользователь @{user} не состоит в беседе'), time.sleep(1)
    else: print("нету таких"), time.sleep(1)


menu()



"""
while True:
  channel = input('channel: ')
  if channel in base:
    print(base[channel])
    for k in range(len(base[channel])):
      print(k), time.sleep(1)
    output_msg = input(' > ')
"""    