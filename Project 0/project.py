from cryptography.fernet import Fernet
import os
import random
import string

progname = "Manager Of Passwords"
filename = "loginfo.txt"
design="="*53
if not os.path.exists(filename):
    f = open(filename, "w")
    f.close()
    print(design.center(150))
    print(progname.center(150))
    print(design.center(150))

else:
    print(design.center(150))
    print(progname.center(150))
    print(design.center(150))


def encryption(password, key):
    if not isinstance(key, Fernet):
        if isinstance(key, str):
            key = key.encode()
        key = Fernet(key)
    password = key.encrypt(password.encode())
    return password

def decryption(password, key):
    password = password.encode()
    key = Fernet(key)
    password = key.decrypt(password).decode()
    return password

def SignIn(username,password):
    f=open("loginfo.txt","a")
    f.write(username+","+password+"\n")
    f.close()
    print("account created we hope you enjoy using Manager of Passwords")
    f=open(username+".txt","w")  
    f.close()

def login(username,password):
    f=open("loginfo.txt","r")
    list=f.readlines()
    f.close()
    length=len(list)
    for i in range(0,length):
        user,Pass=list[i].strip().split(",")
        if user==username and Pass==password:
            return 1
        
    return 2
def PasswordGeneration(lenght):
    All_characters=string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    password=random.choices(All_characters,k=lenght)
    return "".join(password)
    

def RemovePassword(userfolder):
    f = open(userfolder, "r")
    listOfPasswords = f.readlines()
    f.close()
    length = len(listOfPasswords)

    passlength = 0
    userlength = 0

    for i in range(length):
        key, account, password = listOfPasswords[i].strip().split(",")
        password = decryption(password, key)
        if len(account) > userlength:
            userlength = len(account)
        if len(password) > passlength:
            passlength = len(password)
        listOfPasswords[i] = [account, password]

    print("=" * 53)
    print("No.   Account Name" + " " * (userlength - len("Account Name")) + "   Password")
    print("=" * 53)

    for i in range(length):
        account_spaces = userlength - len(listOfPasswords[i][0])
        password_spaces = passlength - len(listOfPasswords[i][1])
        print(str(i + 1) + "   " + listOfPasswords[i][0] + " " * account_spaces + "   " + listOfPasswords[i][1] + " " * password_spaces)

    print("=" * 53)

    remove_no = int(input("Enter the number of the password you want to remove: "))
    listOfPasswords.pop(remove_no - 1)
    length = len(listOfPasswords)

    f = open(userfolder, "w")
    for i in range(length):
        key = Fernet.generate_key().decode()
        password = encryption(listOfPasswords[i][1], key)
        f.write(key + "," + listOfPasswords[i][0] + "," + password.decode() + "\n")
    f.close()
    print("Password has been successfully removed")


def Changepassword(userfolder):
    f = open(userfolder, "r")
    listOfPasswords = f.readlines()
    f.close()
    length = len(listOfPasswords)

    passlength = 0
    userlength = 0

    for i in range(length):
        key, account, password = listOfPasswords[i].strip().split(",")
        password = decryption(password, key)
        if len(account) > userlength:
            userlength = len(account)
        if len(password) > passlength:
            passlength = len(password)
        listOfPasswords[i] = [key, account, password]

    print("=" * 53)
    print("No.   Account Name" + " " * (userlength - len("Account Name")) + "   Password")
    print("=" * 53)

    for i in range(length):
        account_spaces = userlength - len(listOfPasswords[i][1])
        password_spaces = passlength - len(listOfPasswords[i][2])
        print(str(i + 1) + "   " + listOfPasswords[i][1] + " " * account_spaces + "   " + listOfPasswords[i][2] + " " * password_spaces)

    print("=" * 53)

    changeno = int(input("Enter the number of the password you want to change: "))
    newpass = input("Enter new password: ")
    listOfPasswords[changeno - 1][2] = newpass

    f = open(userfolder, "w")
    for i in range(len(listOfPasswords)):
        key = listOfPasswords[i][0]
        account = listOfPasswords[i][1]
        password = encryption(listOfPasswords[i][2], key)
        f.write(key + "," + account + "," + password.decode() + "\n")
    f.close()

    print("Password has been successfully changed")


def ViewPassword(userfolder):
    f = open(userfolder, "r")
    listOfPasswords = f.readlines()
    f.close()
    length = len(listOfPasswords)
    passlength = 0
    userlength = 0

    for i in range(length):
        key, account, password = listOfPasswords[i].strip().split(",")
        key = key.encode()
        password = decryption(password, key)
        if len(account) > userlength:
            userlength = len(account)
        if len(password) > passlength:
            passlength = len(password)

        listOfPasswords[i] = [account, password]

    print("=" * 53)
    print("Account Name" + " " * (userlength - len("Account Name")) + "   Password")
    print("=" * 53)

    for i in range(length):
        account_spaces = userlength - len(listOfPasswords[i][0])
        password_spaces = passlength - len(listOfPasswords[i][1])
        print(listOfPasswords[i][0] + " " * account_spaces + "       " + listOfPasswords[i][1] + " " * password_spaces)

    print("=" * 53)


def SearchPassword(userfolder):
    SearchedAcc = input("Enter the account/username of the password you want to search: ")
    print("1. View password")
    print("2. Remove password")
    print("3. Change password")
    choice = int(input("Enter the process you want to carry out: "))

    f = open(userfolder, "r")
    listOfPasswords = f.readlines()
    f.close()
    length = len(listOfPasswords)
    flag = 0

    for i in range(length):
        key, account, password = listOfPasswords[i].strip().split(",")
        password = decryption(password, key)
        listOfPasswords[i] = [key, account, password]

        if SearchedAcc == account:
            flag=1
            if choice == 1:
                print("=" * 53)
                print("Account Name        Password")
                print("=" * 53)
                print(account + "        " + password)
                break

            elif choice == 2:
                listOfPasswords.pop(i)
                print("Password and account successfully removed")
                break

            elif choice == 3:
                newpass = input("Enter new password: ")
                password = encryption(newpass, key)
                listOfPasswords[i] = [key, account, password]
                print("Password successfully changed")
                break

        

    f = open(userfolder, "w")
    if flag == 1:
        length = len(listOfPasswords)
        for i in range(length):
            f.write(listOfPasswords[i][0] + "," + listOfPasswords[i][1] + "," + listOfPasswords[i][2].decode() + "\n")
    else:
        print("Account not found")
    f.close()


userfolder = ""

while 1:
    print("1. Sign-in to create account")
    print("2. Login into Account")
    print()
    choice = int(input("Enter number to login or Sign-In: "))
    while 1:
        if choice == 1:
            print()
            print("Username must contain 12 or less characters")
            username = input("Enter your username: ")
            print()
            print("Password must contain 8 or more characters and 12 or less characters")
            password = input("Enter your password: ")
            userlength = len(username)
            passlength = len(password)

            if userlength <= 12:
                if passlength <= 12 and passlength >= 8:
                    SignIn(username, password)
                    userfolder = username + ".txt"
                    break
                else:
                    print("Password invalid...")
                    print("Password must contain 8 or more characters and 12 or less characters")
            else:
                print("Username invalid...")
                print("Username must contain 12 or less characters")

        elif choice == 2:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if login(username, password) == 1:
                print("Successfully logged in")
                userfolder = username + ".txt"
                break
            else:
                print("Logging unsuccessful")
                print("Try again or sign in")
                choice = int(input("Enter 1 to sign in OR 2 to login: "))
                continue

    break

while userfolder != "":
    print("="*45)
    print("1. Add new password")
    print("2. Remove password")
    print("3. Change password")
    print("4. View password")
    print("5. Search password by account/username for remove/change/view")
    print("6.Generate a strong password")
    print("7.Save and Exit....")
    print("="*45)
    print()
    choice = int(input("Enter the number of the process you want to do: "))

    if choice == 1:
        genkey = Fernet.generate_key()
        key = Fernet(genkey)
        account = input("Enter username/gmail: ")
        password = input("Enter the password: ")
        password = encryption(password, key)
        password = password.decode()
        f = open(userfolder, 'a')
        f.write(genkey.decode() + "," + account + "," + password + "\n")
        f.close()
    elif choice == 2:
        RemovePassword(userfolder)
    elif choice == 3:
        Changepassword(userfolder)
    elif choice == 4:
        ViewPassword(userfolder)
    elif choice == 5:
        SearchPassword(userfolder)
    elif choice==6:
        print("password can't be less than 8 characters")
        lenght=int(input("Enter the number of characters you want your password to be:"))
        print(PasswordGeneration(lenght))
    elif choice==7:
        break
    else:
        print("Invalid input......")
