import subprocess
import minecraft_launcher_lib
import json
import tkinter as tk
import tkinter.ttk as ttk
import requests

def alt_auth(token):
    data = json.dumps({"agent":{"name":"Minecraft","version":1}, "username":token,"password":"abcde"})
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://authserver.thealtening.com/authenticate', data=data, headers=headers)
    return (r.text)
def auth(username,password):
    data = json.dumps({"agent":{"name":"Minecraft","version":1}, "username":username,"password":password})
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://authserver.mojang.com/authenticate', data=data, headers=headers)
    return (r.text)

class MinecraftLauncher:
    def mc_run(self):

        password = self.input_pass.get()
        user = self.input_user.get()
        account = auth.auth(user, password)
        data = json.loads(account)
        return_profile = data['selectedProfile']
        server = self.input_ip.get()
        options = {
            "username": return_profile['name'],
            "uuid": return_profile['id'],
            "token": data['accessToken'],
            "server": server,
        }
        mc_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command("1.16.5", mc_directory, options)
        subprocess.run(minecraft_command)
    def __init__(self, master=None):
        # build ui
        self.frame1 = ttk.Frame(master)
        self.input_ip = ttk.Entry(self.frame1)
        self.input_ip.place(anchor="nw", relx="0.02", rely="0.09", x="0", y="0")
        self.label_ip = ttk.Label(self.frame1)
        self.label_ip.configure(text="Server IP ")
        self.label_ip.place(anchor="nw", relx="0.25", rely="0.0", x="0", y="0")
        self.input_user = ttk.Entry(self.frame1)
        self.input_user.place(anchor="nw", relx="0.02", rely="0.30", x="0", y="0")
        self.label_user = ttk.Label(self.frame1)
        self.label_user.configure(text="Username")
        self.label_user.place(anchor="nw", relx="0.23", rely="0.2", x="0", y="0")
        self.input_pass = ttk.Entry(self.frame1)
        self.input_pass.place(anchor="nw", relx="0.02", rely="0.5", x="0", y="0")
        self.label_pass = ttk.Label(self.frame1)
        self.label_pass.configure(text="Password")
        self.label_pass.place(anchor="nw", relx="0.25", rely="0.40", x="0", y="0")
        self.play = ttk.Button(self.frame1)
        self.play.configure(text="Play", command= lambda: MinecraftLauncher.mc_run(self))
        self.play.place(anchor="nw", relx="0.65", rely="0.05", x="0", y="0")
        self.frame1.configure(height="200", width="200")
        self.frame1.pack(side="top")

        # Main widget
        self.mainwindow = self.frame1

    def run(self):
        self.mainwindow.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftLauncher(root)
    app.run()
