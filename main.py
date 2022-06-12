from tkinter.ttk import Combobox
import minecraft_launcher_lib, os, subprocess, requests, asyncio, minepi, sys
from minecraft_launcher_lib import account, command
from tkinter import *

MINECRAFT_DIRECTORY = minecraft_launcher_lib.utils.get_minecraft_directory()

os.system("title Anti-P2W Launcher")
os.system('cls')

root = Tk()
top = Toplevel()

top.geometry('300x200')
top.resizable(width=False, height=False)
top.title('Anti-P2W Launcher')

root.title("Anti-P2W Launcher")
root.geometry("500x675")
root.resizable(width=False, height=False)

versionsLabel = Label(root, text="Versions")
versionBox = Listbox(root, width=60)

count = 0

versions = minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIRECTORY)
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

canvas = Canvas(root, width=200, height=400)
canvas.pack(side=RIGHT)

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

async def get_skin():
    email = emailTxt.get()
    password = passwordTxt.get()

    username = account.login_user(email, password)['selectedProfile']['name']

    p = minepi.Player(name=username)
    await p.initialize()
    await p.skin.render_skin(hr=0, vr=0)

    p.skin.skin.save('skin.png')

    img = PhotoImage(file='skin.png')
    canvas.create_image(0,0, anchor=NW, image=img)

def login():
    email = emailTxt.get()
    password = passwordTxt.get()

    if account.validate_access_token(account.login_user(email, password)['accessToken']):
        root.deiconify()
        asyncio.run(get_skin())
        top.destroy()

def cancel():
    top.destroy()
    root.destroy()
    sys.exit()

if not root.iconwindow:
    asyncio.run(get_skin())

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
    
    minecraft_launcher_lib.fabric.install_fabric("1.19", MINECRAFT_DIRECTORY)
    clientResponse = requests.get("https://workupload.com/start/peJLdkfkgNh")
    apiResponse = requests.get("https://www.curseforge.com/minecraft/mc-mods/fabric-api/download/3823269/file")
    open(MINECRAFT_DIRECTORY + "\\mods\\meteor-client-0.4.9.jar", "wb").write(clientResponse.content)
    open(MINECRAFT_DIRECTORY + "\\mods\\fabric_api.jar", "wb").write(apiResponse.content)

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

    clientResponse = requests.get("https://github.com/MatHax/API/raw/master/Download/1-18-2/MatHax-v1.7.6-Fabric_1.18.2.jar")
    apiResponse = requests.get("https://cdn-142.anonfiles.com/Nae2q1p2y7/83aef772-1655036736/fabric-api-0.54.0+1.18.2.jar")
    minecraft_launcher_lib.fabric.install_fabric("1.18.2", MINECRAFT_DIRECTORY)
    open(MINECRAFT_DIRECTORY + "\\mods\\mathax.jar", "wb").write(clientResponse.content)

def refreshVersions():
    versions = minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIRECTORY)
    versionBox.delete(0, END)
    count = 0
    for i in versions:
        count += 1
        versionBox.insert(count, i['id'])

def start():
    email = emailTxt.get()
    password = passwordTxt.get()

    username = account.login_user(email, password)['selectedProfile']['name']
    uuid = account.login_user(email, password)['selectedProfile']['id']

    for i in versionBox.curselection():
        version = versionBox.get(i)


    print('[UUID] [' + uuid + "]")
    access_token = account.login_user(email, password)['accessToken']

    print("[VALID] [" + str(account.validate_access_token(account.login_user(email, password)['accessToken'])) + "]")

    if account.validate_access_token(account.login_user(email, password)['accessToken']):
        options = {
            "username": username,
            "uuid": uuid,
            "token": access_token,
        }
    minecraft_command = command.get_minecraft_command(version, MINECRAFT_DIRECTORY, options)

    subprocess.call(minecraft_command)

installbtn = Button(root, text="Install Meteor", command=installMeteor)
installbtn.pack(side=TOP)

installmat = Button(root, text="Install MatHax", command=installMatHax)
installmat.pack(side=TOP)

refreshbtn = Button(root, text="Refresh Versions", command=refreshVersions)
refreshbtn.pack(side=TOP)

startButton = Button(root, text="Start", command=start)
startButton.pack(side=TOP)

root.withdraw()
root.mainloop()