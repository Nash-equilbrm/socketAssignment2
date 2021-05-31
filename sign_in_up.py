import json



        



def SignIn(username,password):
    try:
        data ={}
        file = open("USERS.json",'r') 
        data = json.load(file)
        for user in data:
            if data.get(user).get("username") == username and data.get(user).get("pass") == password:
                file.close()
                return True
        file.close()    
        return False
    except Exception as e:
        print(e)
        return False



def SignUp(username,password):
    try:
        data ={}
        with open("USERS.json",'r') as file:
            data = json.load(file)
        curent_users_count = len(data) + 1
        index ="User"+str(curent_users_count)

        new_user = {
            index:{
                "username":username,
                "pass":password
            }
        }
        data.update(new_user)
        with open("USERS.json",'w') as file:
            json.dump(data,file)
        return True
    except Exception as e:
        print(e)
        return False

