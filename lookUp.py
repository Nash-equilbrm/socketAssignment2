import json

def getCommand(command):
    switcher = {
        "F_ID": 1,
        "F_Name": 2,
        "F_Type": 3,
        "F_Author": 4
    }
    return switcher.get(command)

def valid_command(command):
    params = command.split(' ')
    first_param =params[0]
    return getCommand(first_param) is not None

def standardlize_param(param):
    s= param
    if param[0]=='\"' or param[0]=='\'':
        s = s[1:]
    if param[len(param)-1] =='\"' or param[len(param)-1]=='\'':
        s = s[: len(param)-2 ]
    return s

def get_param(command):
    first_slash = command.find(' ')
    first_param = command[:first_slash]
    sencond_param = command[first_slash+1:]
    first_param = getCommand(first_param)
    sencond_param = standardlize_param(sencond_param)
    if first_param == 1:
        try:
            sencond_param = int(sencond_param)
        except Exception:
            sencond_param = -1
    return first_param,sencond_param



def search_results(cmd,arg):
    info = []
    with open("BOOKS.json",'r') as file:
        data = json.load(file)
        if cmd == 1:
            for book in data:
                # if str(type(data[book].get("id"))) == '<class \'int\'>':
                #     arg = int(arg)
                # else:
                #     arg = str(arg)
                
                if str(data[book].get("id")) == str(arg):
                    info.append([data[book].get("id"), data[book].get("name"),data[book].get("author"),data[book].get("year"),data[book].get("type")])

        elif cmd == 2:
            for book in data:
                if data[book].get("name") == arg:
                    info.append([data[book].get("id"), data[book].get("name"),data[book].get("author"),data[book].get("year"),data[book].get("type")])

        elif cmd == 3:
            for book in data:
                if data[book].get("type") == arg:
                    info.append([data[book].get("id"), data[book].get("name"),data[book].get("author"),data[book].get("year"),data[book].get("type")])
        

        elif cmd == 4:
            for book in data:
                if data[book].get("author") == arg:
                    info.append([data[book].get("id"), data[book].get("name"),data[book].get("author"),data[book].get("year"),data[book].get("type")])

    return info


def book_directory(id,extension):
    dir ='BOOKS\\'+str(id)+"\\"
    with open('BOOKS.json','r') as file:
        data = json.load(file)
        for book in data:
            check_id = str(data[book].get("id"))
            if check_id == id:
                dir += data[book].get("name") +extension
    return dir