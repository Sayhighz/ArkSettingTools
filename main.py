from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import json
import os
import shutil
import subprocess
import psutil

app = tk.Tk()
app.title('ARKSettingTools')
app.geometry('300x70')
app.resizable(width=False, height=False)
app.iconbitmap('favicon.ico')

logo_art = '''
██ ███ █╬█ █╬█ █ ███ █╬█
█▄ █▄█ █▄█ █▄█ █ █╬▄ █▄█
▄█ █╬█ ╬█╬ █╬█ █ █▄█ █╬█
'''


# show logo
def showLogo():
        
    global logo
    logo = tk.Label(app, text=logo_art)
    logo.place(x=5,y=1)


# delete widget
def clear_widget():

    logo.destroy()
    for widget in app.winfo_children():
        if isinstance(widget, tk.Checkbutton):  #clear checkbox
            widget.destroy()
            
    for widget in app.winfo_children():
        if isinstance(widget, tk.Button):   #clear button
            widget.destroy()


# menu
def showMenu():
    mainMenu.add_command(label = "Filegame", command=fileGameMenu)
    mainMenu.add_command(label = "CustomINI", command=iniMenu)
    mainMenu.add_command(label = "Restart", command=restartGame)


# custom ini
def iniMenu():

    app.geometry("400x190")
    clear_widget()
    cdelFog = tk.Checkbutton(app, text='Disable Fog\nปิดหมอก ',variable=Fog, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultINI))
    cdelFog.place(x=20,y=10)
    cdelFoliage = tk.Checkbutton(app, text='Disable Foliage/Resource\nปิดใบไม้/ทรัพยากรบางอย่าง',variable=Foliage, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultINI))
    cdelFoliage.place(x=20,y=50)
    cdelLight = tk.Checkbutton(app, text='Disable Light\nปิดแสงเงา',variable=Light, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultINI))
    cdelLight.place(x=20,y=90)
    cdelMaterials = tk.Checkbutton(app, text='Disable PlatZ/Beer/TekHelmet\nปิดเบียร์/หมวกเทค/ระเบิดแสง',variable=Materials, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultINI))
    cdelMaterials.place(x=200,y=10)
    cdelParticles = tk.Checkbutton(app, text='Disable TekRifle/mana Beam\nปิดวิถีกระสุน/แสงแอร์ดอร์ป',variable=Particles, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultINI))
    cdelParticles.place(x=200,y=50)
    cdelEverything = tk.Checkbutton(app, text='Disable a lot Effect\n(ไม่แนะนำ)',variable=Everything, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultINI))
    cdelEverything.place(x=200,y=90)
    cDefault = tk.Checkbutton(app, text='Default\nค่าเริ่มต้น',variable=defaultINI, onvalue=1, offvalue=0, command=defaultCheckbox)
    cDefault.place(x=200,y=130)
    generateBtn = tk.Button(app, text='Generate!', command=selectVariable, width=20)
    generateBtn.place(x=20,y=135)


# filegame edit checkbox
def fileGameMenu():
    
    app.geometry("300x150")
    clear_widget()
    cgameUser = tk.Checkbutton(app, text='GameUserSetting\n(cannot be restored)', variable=gameUserSetting, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultFile))
    cgameUser.place(x=20,y=10)
    cmapYellow = tk.Checkbutton(app, text='PrettyMap', variable=mapYellow, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultFile))
    cmapYellow.place(x=20,y=50)
    cmapRainbow = tk.Checkbutton(app, text='DirtyMap', variable=mapRainbow, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultFile))
    cmapRainbow.place(x=160,y=50)
    ctopWater = tk.Checkbutton(app, text='Clear Topwater\nเคลียผิวน้ำ', variable=topWater, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultFile))
    ctopWater.place(x=160,y=10)
    cdefault = tk.Checkbutton(app, text='Default\nคืนค่าเริ่มต้น', variable=defaultFile, onvalue=1, offvalue=0, command=defaultCheckboxfile)
    cdefault.place(x=160,y=80)
    editBtn = tk.Button(app, text='Edit File!', command=selectFileGame, width=15)
    editBtn.place(x=20,y=90)


# find file location
def getfilepath():

    file_path = filedialog.askdirectory(initialdir="/", title="Select a file")
    folder_check = file_path + '/ShooterGame/'

    # check game path
    if os.path.exists(folder_check):
        lablePath.set(file_path)
        with open('file/gamelocation.txt', "w")as file:
            file.write(lablePath.get())
        # show menu
        
        showMenu()
        showLogo()
        browsePathBtn.destroy()
        app.geometry("250x120")
    else:
        messagebox.showerror("Path", "Not found\nplease change directory")


# get data from file txt and check
def getData():
    checkDirectory = lablePath.get() + ('/ShooterGame/')
    if os.path.exists(checkDirectory):
        browsePathBtn.destroy()
        showMenu()
        showLogo()
        app.geometry("250x120")



# function select variable
def selectVariable():
     
    with open("file/Variable.json") as file:
        var_data = json.load(file)
    
    if (Fog.get() == 1):
        variable = var_data["DelFog"] 
        addVariable(variable)
    else:
        variable = var_data["DelFog"]
        removeVariable(variable)

    if (Foliage.get() == 1):
        variable = var_data["DelFoliage"] 
        addVariable(variable)
    else:
        variable = var_data["DelFoliage"]
        removeVariable(variable)
        
    if (Light.get() == 1):
        variable = var_data["DelLight"] 
        addVariable(variable)
    else:
        variable = var_data["DelLight"]
        removeVariable(variable)
        
    if (Materials.get() == 1):
        variable = var_data["DelMaterials"] 
        addVariable(variable)
    else:
        variable = var_data["DelMaterials"]
        removeVariable(variable)
        
    if (Particles.get() == 1):
        variable = var_data["DelParticles"] 
        addVariable(variable)
    else:
        variable = var_data["DelParticles"]
        removeVariable(variable)
        
    if (Everything.get() == 1):
        variable = var_data["DelEverything"] 
        addVariable(variable)
    else:
        variable = var_data["DelEverything"]
        removeVariable(variable)
        
    if (defaultINI.get() == 1):
        removeVariable(constINI)
    else:
        with open('file/BaseDeviceProfiles.ini', 'r') as file:
            lines = file.readlines()
        for line_number, line in enumerate(lines, start=1):
            if line_number >= 45 and '+CVars=ShowFloatingDamageText=True' in line:
                checked = 'found'
                break
            else:
                checked = 'none'
        if checked == 'found':
            pass
        else:
            file = open('file/BaseDeviceProfiles.ini', 'r')
            lines = file.readlines()
            file.close()
            lines.insert(45, constINI)
            file = open('file/BaseDeviceProfiles.ini', 'w')
            file.writelines(lines)
            file.close()
        copyFile('file/BaseDeviceProfiles.ini',lablePath.get()+'/Engine/Config/BaseDeviceProfiles.ini')

    tk.messagebox.showinfo(title=None, message='Done')
    answer = tk.messagebox.askyesno(title=None, message='Do you want to Restartgame?')
    if answer:
        restartGame()
        
        
        
        
    return variable,var_data
            

# deselect all checkbox            
def defaultCheckbox():
    Fog.set(0)
    Foliage.set(0)
    Light.set(0)
    Materials.set(0)
    Particles.set(0)
    Everything.set(0)


# deselect all checkbox
def defaultCheckboxfile():
    mapYellow.set(0)
    mapRainbow.set(0)
    topWater.set(0)


# deselect some checkbox
def deselectCheckbox(cb):
    
    cb.set(0)


# variable of ini
constINI = '''+CVars=ShowFloatingDamageText=True
+CVars=FogDensity=0.0
+CVars=FrameRateCap=144
+CVars=FrameRateMinimum=144
+CVars=MaxES2PixelShaderAdditiveComplexityCount=45
+CVars=MaxPixelShaderAdditiveComplexityCount=128
+CVars=MaxSmoothedFrameRate=144
+CVars=MinDesiredFrameRate=70
+CVars=MinSmoothedFrameRate=5
+CVars=NearClipPlane=12.0
+CVars=ShowFlag.AmbientOcclusion=0
+CVars=ShowFlag.AntiAliasing=0
+CVars=ShowFlag.Atmosphere=0
+CVars=ShowFlag.AtmosphericFog=0
+CVars=ShowFlag.AudioRadius=0
+CVars=ShowFlag.BSP=0
+CVars=ShowFlag.BSPSplit=0
+CVars=ShowFlag.BSPTriangles=0
+CVars=ShowFlag.BillboardSprites=0
+CVars=ShowFlag.Brushes=0
+CVars=ShowFlag.BuilderBrush=0
+CVars=ShowFlag.CameraAspectRatioBars=0
+CVars=ShowFlag.CameraFrustums=0
+CVars=ShowFlag.CameraImperfections=0
+CVars=ShowFlag.CameraInterpolation=0
+CVars=ShowFlag.CameraSafeFrames=0
+CVars=ShowFlag.CompositeEditorPrimitives=0
+CVars=ShowFlag.Constraints=0
+CVars=ShowFlag.Cover=0
+CVars=ShowFlag.Decals=0
+CVars=ShowFlag.DeferredLighting=0
+CVars=ShowFlag.DepthOfField=0
+CVars=ShowFlag.Diffuse=0
+CVars=ShowFlag.DirectLighting=0
+CVars=ShowFlag.DirectionalLights=0
+CVars=ShowFlag.DistanceCulledPrimitives=0
+CVars=ShowFlag.DistanceFieldAO=0
+CVars=ShowFlag.Editor=0
+CVars=ShowFlag.EyeAdaptation=0
+CVars=ShowFlag.Fog=1
+CVars=ShowFlag.Game=0
+CVars=ShowFlag.LOD=0
+CVars=ShowFlag.Landscape=0
+CVars=ShowFlag.LargeVertices=0
+CVars=ShowFlag.LensFlares=0
+CVars=ShowFlag.LevelColoration=0
+CVars=ShowFlag.LightInfluences=0
+CVars=ShowFlag.LightMapDensity=0
+CVars=ShowFlag.LightRadius=0
+CVars=ShowFlag.LightShafts=0
+CVars=ShowFlag.Lighting=0
+CVars=ShowFlag.LpvLightingOnly=0
+CVars=ShowFlag.MeshEdges=0
+CVars=ShowFlag.MotionBlur=0
+CVars=ShowFlag.OnScreenDebug=0
+CVars=ShowFlag.OverrideDiffuseAndSpecular=0
+CVars=ShowFlag.Paper2DSprites=0
+CVars=ShowFlag.Particles=0
+CVars=r.SceneColorFringe.Max=0
+CVars=r.oneframethreadlag=1
+CVars=t.maxfps=144

'''


# function add variable to ini file
def addVariable(variable):
    
    with open('file/BaseDeviceProfiles.ini', 'r') as file:
        lines = file.readlines()
        for line_number, line in enumerate(lines, start=1):
            if line_number >= 39 and variable in line:
                checked = variable
                
                break
        else:
            checked = 'none'

    if checked == variable:
        pass
    else:
        file = open('file/BaseDeviceProfiles.ini', 'r')
        lines = file.readlines()
        file.close()
        lines.insert(39, variable)
        file = open('file/BaseDeviceProfiles.ini', 'w')
        file.writelines(lines)
        file.close()
        copyFile('file/BaseDeviceProfiles.ini',lablePath.get()+'/Engine/Config/BaseDeviceProfiles.ini')


# function remove variable from ini file
def removeVariable(variable):
    
   file = open("file/BaseDeviceProfiles.ini", "r")
   content = file.read()
   removeVar = content.replace(variable, '')
   file = open("file/BaseDeviceProfiles.ini", "w")
   file.write(removeVar)
   file.close()
   copyFile('file/BaseDeviceProfiles.ini',lablePath.get()+'/Engine/Config/BaseDeviceProfiles.ini')


# select function of fileGame
def selectFileGame():
    
    if (gameUserSetting.get() == 1):

        copyFile('file/GameUserSettings.ini',lablePath.get()+'/ShooterGame/Saved/Config/WindowsNoEditor')
    
    if (mapYellow.get() == 1):
        defaultFile.set(0)
        checkAndRename(lablePath.get()+'/Engine/Content/EngineMaterials/DefaultDiffuse.uasset','file/DefaultDiffuse.uasset')
    else:
        renameFile(lablePath.get()+'/Engine/Content/EngineMaterials/DefaultDiffuse.uasset1',lablePath.get()+'/Engine/Content/EngineMaterials/DefaultDiffuse.uasset')

    if (mapRainbow.get() == 1):
        defaultFile.set(0)
        checkAndRename(lablePath.get()+'/Engine/Content/EngineMaterials/WeightMapPlaceholderTexture.uasset','WeightMapPlaceholderTexture.uasset')
        checkAndRename(lablePath.get()+'/Engine/Content/EngineResources/DefaultTexture.uasset','file/DefaultTexture.uasset')
    else:
        renameFile(lablePath.get()+'/Engine/Content/EngineMaterials/WeightMapPlaceholderTexture.uasset1',lablePath.get()+'/Engine/Content/EngineMaterials/WeightMapPlaceholderTexture.uasset')
        renameFile(lablePath.get()+'/Engine/Content/EngineResources/DefaultTexture.uasset1',lablePath.get()+'/Engine/Content/EngineResources/DefaultTexture.uasset')
        
    if (topWater.get() == 1):
        defaultFile.set(0)
        checkAndRename(lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient.uasset','file/SoftEdgeGradient.uasset')
        checkAndRename(lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient_Linear.uasset','file/SoftEdgeGradient_Linear.uasset')
    else:
        renameFile(lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient.uasset1',lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient.uasset')
        renameFile(lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient_Linear.uasset1',lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient_Linear.uasset')
    
    tk.messagebox.showinfo(title=None, message='Done')
    answer = tk.messagebox.askyesno(title=None, message='Do you want to Restartgame?')
    if answer:
        restartGame()
    
     
# move file
def copyFile(old_file,new_file):
    
    file = old_file
    destination = new_file
    shutil.copy(file, destination)


# rename file
def renameFile(old_name,new_name):
    
    if os.path.exists(new_name):
        pass
    else:
        before = old_name
        after = new_name
        os.rename(before,after)


#check first and rename
def checkAndRename(path,old_name):
    
    if os.path.exists(path):
        if (os.path.exists(path+'1') and os.path.exists(path)):
            os.remove(path+'1')
        before = path
        after = path+'1'
        os.rename(before,after)
    elif os.path.exists(path+'1'):
        pass
    else:
        if os.path.exists(path+'1'):
            os.remove(path+'1')
        file = old_name
        destination = path
        shutil.copy(file, destination)
        
        before = path
        after = path+'1'
        os.rename(before,after)
    print(path)


# function of restart game
def restartGame():

    ark_exe = lablePath.get() + '/ShooterGame/Binaries/Win64/ShooterGame.exe'
    
    if is_program_running('ShooterGame.exe'):
        subprocess.call(["taskkill", "/F", "/IM", 'ShooterGame.exe'])
        subprocess.Popen(ark_exe)
    else:
        tk.messagebox.showerror(title=None, message='Game is closed')
    

# check status game 
def is_program_running(program_name):
    
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == program_name:
            return True
    return False
    

# read location user
with open('file/gamelocation.txt', 'r')as ofile:
    location = ofile.read()

Fog = tk.IntVar()
Foliage = tk.IntVar()
Light = tk.IntVar()
Materials = tk.IntVar()
Particles = tk.IntVar()
Everything = tk.IntVar()
defaultINI = tk.IntVar()
lablePath = StringVar()
mainMenu = tk.Menu(app)
gameUserSetting = tk.IntVar()
mapYellow = tk.IntVar()
mapRainbow = tk.IntVar()
topWater = tk.IntVar()
defaultFile = tk.IntVar()


Label(app, text="change to ur path", textvariable=lablePath).pack(side=tk.BOTTOM)
lablePath.set(location)
browsePathBtn = tk.Button(
    app, text="Browse\nGame Location", command=getfilepath)
browsePathBtn.place(relx=.5, rely=.5,anchor= CENTER)

# get data from gamelocation.txt
getData()
    
app.config(menu=mainMenu)
app.mainloop()