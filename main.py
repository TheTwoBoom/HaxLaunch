from tkinter.ttk import Combobox
import minecraft_launcher_lib, os, subprocess, requests
from minecraft_launcher_lib import account, command
from tkinter import *
from PIL import ImageTk
from urllib.request import urlopen

MINECRAFT_DIRECTORY = minecraft_launcher_lib.utils.get_minecraft_directory()

root = Tk()
top = Toplevel()

top.geometry('300x200')
top.resizable(width=False, height=False)
top.title('HaxLaunch')

root.title("HaxLaunch")
root.geometry("500x675")
root.resizable(width=False, height=False)

versionsLabel = Label(root, text="Versions")
versionBox = Listbox(root, width=60)

versions = minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIRECTORY)
count = 0
for i in versions:
    count += 1
    versionBox.insert(count, i['id'])

versionsLabel.pack()
versionBox.pack()

current_value = StringVar()

altLabel = Label(top, text="Alt Presets")
altBox = Combobox(top, textvariable=current_value,
                       values=[ "Cojo2@optonline.net:Brandon0119",
                                "marco_godbout1@hotmail.com:dragon003","juliannah@live.ca:Quimmik1",
                                "HolyLevi45@gmail.com:slycooper1125","tuna@fernand.com:fernie53",
                                "wladkai@yahoo.de:010203040506kl","amberwang319@gmail.com:Aw40048109",
                                "marcos.marjor@gmail.com:Audi.r-8",
                                "meditator101@gmail.com:Sassanid1453!",
                                "vianneycuvelier97@gmail.com:Theicewizz7$"], state='readonly')

def usealt(event):
    alt = current_value.get().split(":")
    emailTxt.delete(0, END)
    emailTxt.insert(0, alt[0])

    passwordTxt.delete(0, END)
    passwordTxt.insert(0, alt[1])

altBox.bind('<<ComboboxSelected>>', usealt)
altLabel.pack()
altBox.pack()

emailLabel = Label(top, text="E-Mail / Username")
emailLabel.pack()
emailTxt = Entry(top, width=30)
emailTxt.pack()

pwdLabel = Label(top, text="Password")
pwdLabel.pack()
passwordTxt = Entry(top, width=30)
passwordTxt.pack()

loginBtn = Button(top, text="Login", command=lambda:login())
cancelBtn = Button(top, text="Cancel", command=lambda:cancel())

loginBtn.pack()
cancelBtn.pack()

def show_skin():
    uuid = account.login_user(globals()['email'], globals()['password'])['selectedProfile']['id']
    raw_data = urlopen(f'https://crafatar.com/renders/body/{uuid}').read()
    image = ImageTk.PhotoImage(data=raw_data)
    skinLabel = Label(image=image)
    skinLabel.image = image
    skinLabel.pack(side=RIGHT)

def login():
    globals()['email'] = emailTxt.get()
    globals()['password'] = passwordTxt.get()

    if account.validate_access_token(account.login_user(globals()['email'], globals()['password'])['accessToken']):
        root.deiconify()
        show_skin()
        top.destroy()

def cancel():
    top.destroy()
    root.destroy()
    sys.exit()

def installMeteor():
    try:
        os.remove(MINECRAFT_DIRECTORY + "\\mods\\meteor-client-0.4.9.jar")
    except:
        pass
    try:
        os.remove(MINECRAFT_DIRECTORY + "\\mods\\fabric_api.jar")
    except:
        pass
    try:
        os.remove(MINECRAFT_DIRECTORY + "\\mods\\mathax.jar")
    except:
        pass
    
    if not minecraft_launcher_lib.fabric.is_version_valid("1.18.2", MINECRAFT_DIRECTORY):
        minecraft_launcher_lib.fabric.install_fabric("1.18.2", MINECRAFT_DIRECTORY)
    clientResponse = requests.get("https://meteorclient.com/download")
    open(MINECRAFT_DIRECTORY + "\\mods\\meteor-client-0.4.9.jar", "wb").write(clientResponse.content)

def installMatHax():
    try:
        os.remove(MINECRAFT_DIRECTORY + "\\mods\\meteor-client-0.4.9.jar")
    except:
        pass
    try:
        os.remove(MINECRAFT_DIRECTORY + "\\mods\\fabric_api.jar")
    except:
        pass
    try:
        os.remove(MINECRAFT_DIRECTORY + "\\mods\\mathax.jar")
    except:
        pass

    if not minecraft_launcher_lib.fabric.is_version_valid("1.18.2", MINECRAFT_DIRECTORY):
        minecraft_launcher_lib.fabric.install_fabric("1.18.2", MINECRAFT_DIRECTORY)
    clientResponse = requests.get("https://github.com/MatHax/API/raw/master/Download/1-18-2/MatHax-v1.7.6-Fabric_1.18.2.jar")
    open(MINECRAFT_DIRECTORY + "\\mods\\mathax.jar", "wb").write(clientResponse.content)

def refreshVersions():
    versions = minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIRECTORY)
    versionBox.delete(0, END)
    count = 0
    for i in versions:
        count += 1
        versionBox.insert(count, i['id'])

def start():
    username = account.login_user(globals()['email'], globals()['password'])['selectedProfile']['name']
    uuid = account.login_user(globals()['email'], globals()['password'])['selectedProfile']['id']

    for i in versionBox.curselection():
        version = versionBox.get(i)

    print('[UUID] [' + uuid + "]")
    access_token = account.login_user(globals()['email'], globals()['password'])['accessToken']

    print("[VALID] [" + str(account.validate_access_token(account.login_user(globals()['email'], globals()['password'])['accessToken'])) + "]")

    if account.validate_access_token(account.login_user(globals()['email'], globals()['password'])['accessToken']):
        options = {
            "username": username,
            "uuid": uuid,
            "token": access_token,
        }
    minecraft_command = command.get_minecraft_command(version, MINECRAFT_DIRECTORY, options)

    subprocess.call(minecraft_command)

installmetor = Button(root, text="Install Meteor", command=installMeteor)
installmetor.pack(side=TOP)

installmat = Button(root, text="Install MatHax", command=installMatHax)
installmat.pack(side=TOP)

refreshbtn = Button(root, text="Refresh Versions", command=refreshVersions)
refreshbtn.pack(side=TOP)

startButton = Button(root, text="Start", command=start)
startButton.pack(side=TOP)

root.withdraw()
root.mainloop()
