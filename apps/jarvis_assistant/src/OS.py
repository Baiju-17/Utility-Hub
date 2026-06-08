import os
# 1.file open karne ke liye pahle ek variable me file path store karo phie usko os.startfile(yaha par) me daal do to isse tumhara file open ho jayega 
def file():
    file = "C:\\Users\\baijn\\Videos\\SnapTube\\FREE Stream Starting Soon Overlay Template _ Stream Ending Overlay..mp4"
    os.startfile(file)
# 2. isse folder bhi on ho sakta he
def fol():
    folder = "C:\\Users\\baijn\\Videos\\Angel"
    os.startfile(folder)

def app():
    app = "MSI Center.exe"
    os.startfile(app)
# app()

def app1():
    app = 'YouTube'
    os.system('start'+ app +".exe")
# app1()

def music():
    # agar koi specific song ka play karna ho to bs uska address daal do to wahi wala bajega 
    musicfol = "C:\\Users\\baijn\\Music"
    os.startfile(musicfol)
# music()
while True:
    apps = input("enter App name = ")

    os.system(apps)

