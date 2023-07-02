from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import json
import os
import shutil
import subprocess
import psutil
import threading
import time
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
    mainMenu.add_command(label = "Restart", command=reload_game_thread)


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
    
    tk.messagebox.showwarning(title=None, message='Please exit the game before edit!')
    app.geometry("300x150")
    clear_widget()
    cgameUser = tk.Checkbutton(app, text='GameUserSetting\n(cannot be restored)', variable=gameUserSetting, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultFile))
    cgameUser.place(x=20,y=10)
    cmapYellow = tk.Checkbutton(app, text='PrettyMap', variable=mapYellow, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultFile))
    cmapYellow.place(x=20,y=50)
    cmapRainbow = tk.Checkbutton(app, text='DirtyMap\n(close game first)', variable=mapRainbow, onvalue=1, offvalue=0, command=lambda: deselectCheckbox(defaultFile))
    cmapRainbow.place(x=160,y=45)
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
        #show menu
        showMenu()
        showLogo()
        app.geometry("250x120")
    else:
        lablePath.set('')


# function select variable
def selectVariable():
     
    with open("file/Variable.json") as file:
        var_data = json.load(file)

    if (Fog.get() == 1):
        addVariable(var_data["DelFog"],var_data["DelFog"],39)
    else:
        removeVariable(var_data["DelFog"])

    if (Foliage.get() == 1):
        addVariable(var_data["DelFoliage"],var_data["DelFoliage"],39)
    else:
        removeVariable(var_data["DelFoliage"])
        
    if (Light.get() == 1):
        addVariable(var_data["DelLight"],var_data["DelLight"],39)
        addVariable(var_data["DelfixPrettybug"],var_data["DelfixPrettybug"],39)
    else:
        removeVariable(var_data["DelfixPrettybug"])
        removeVariable(var_data["DelLight"])
        
    if (Materials.get() == 1):
        addVariable(var_data["DelMaterials"],var_data["DelMaterials"],39)
    else:
        removeVariable(var_data["DelMaterials"])
        
    if (Particles.get() == 1):
        addVariable(var_data["DelParticles"],var_data["DelParticles"],39)
    else:
        removeVariable(var_data["DelParticles"])
        
    if (Everything.get() == 1):
        addVariable(var_data["DelEverything"],var_data["DelEverything"],39)
    else:
        removeVariable(var_data["DelEverything"])
        
    if (defaultINI.get() == 1):
        removeVariable(constINI)
    else:
        addVariable('+CVars=t.maxfps=144',constINI,46)

    tk.messagebox.showinfo(title=None, message='Done')
    answer = tk.messagebox.askyesno(title=None, message='Do you want to Restart game?')
    if answer:
        reload_game_thread()
            

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
constINI = '''+CVars=t.maxfps=144
+CVars=FrameRateCap=144
+CVars=FrameRateMinimum=144
+CVars=MaxES2PixelShaderAdditiveComplexityCount=45
+CVars=MaxPixelShaderAdditiveComplexityCount=128
+CVars=MaxSmoothedFrameRate=144
+CVars=MinDesiredFrameRate=70
+CVars=MinSmoothedFrameRate=5
+CVars=r.CustomDepth=0
+CVars=ShowFlag.LightShafts=0
+CVars=ShowFlag.Refraction=0
+CVars=bDisablePhysXHardwareSupport=True
+CVars=bFirstRun=False
+CVars=FogDensity=0.0
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
+CVars=ShowFlag.ColorGrading=0
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
+CVars=ShowFlag.Game=0
+CVars=ShowFlag.LOD=0
+CVars=ShowFlag.Landscape=0
+CVars=ShowFlag.LargeVertices=0
+CVars=ShowFlag.LensFlares=0
+CVars=ShowFlag.LevelColoration=0
+CVars=ShowFlag.LightInfluences=0
+CVars=ShowFlag.LightMapDensity=0
+CVars=ShowFlag.LightRadius=0
+CVars=ShowFlag.Lighting=0
+CVars=ShowFlag.LpvLightingOnly=0
+CVars=ShowFlag.MeshEdges=0
+CVars=ShowFlag.MotionBlur=0
+CVars=ShowFlag.OnScreenDebug=0
+CVars=ShowFlag.OverrideDiffuseAndSpecular=0
+CVars=ShowFlag.Paper2DSprites=0
+CVars=ShowFlag.Particles=0
+CVars=ShowFlag.Pivot=0
+CVars=ShowFlag.PointLights=0
+CVars=ShowFlag.PostProcessMaterial=0
+CVars=ShowFlag.PostProcessing=0
+CVars=ShowFlag.PrecomputedVisibility=0
+CVars=ShowFlag.PreviewShadowsIndicator=0
+CVars=ShowFlag.ReflectionEnvironment=0
+CVars=ShowFlag.ReflectionOverride=0
+CVars=ShowFlag.SelectionOutline=0
+CVars=ShowFlag.ShadowFrustums=0
+CVars=ShowFlag.ShadowsFromEditorHiddenActors=0
+CVars=ShowFlag.SkeletalMeshes=0
+CVars=ShowFlag.SkyLighting=0
+CVars=ShowFlag.Snap=0
+CVars=ShowFlag.Specular=0
+CVars=ShowFlag.SpotLights=0
+CVars=ShowFlag.StaticMeshes=0
+CVars=ShowFlag.StationaryLightOverlap=0
+CVars=ShowFlag.StereoRendering=0
+CVars=ShowFlag.SubsurfaceScattering=0
+CVars=ShowFlag.TemporalAA=0
+CVars=ShowFlag.Tessellation=0
+CVars=ShowFlag.TestImage=0
+CVars=ShowFlag.TextRender=0
+CVars=ShowFlag.TexturedLightProfiles=0
+CVars=ShowFlag.Tonemapper=0
+CVars=ShowFlag.Translucency=0
+CVars=ShowFlag.VectorFields=0
+CVars=ShowFlag.VertexColors=0
+CVars=ShowFlag.Vignette=0
+CVars=ShowFlag.VisualizeAdaptiveDOF=0
+CVars=ShowFlag.VisualizeBuffer=0
+CVars=ShowFlag.VisualizeDOF=0
+CVars=ShowFlag.VisualizeDistanceFieldAO=0
+CVars=ShowFlag.VisualizeHDR=0
+CVars=ShowFlag.VisualizeLPV=0
+CVars=ShowFlag.VisualizeLightCulling=0
+CVars=ShowFlag.VisualizeMotionBlur=0
+CVars=ShowFlag.VisualizeOutOfBoundsPixels=0
+CVars=ShowFlag.VisualizeSSR=0
+CVars=ShowFlag.VisualizeSenses=0
+CVars=ShowFlag.Wireframe=0
+CVars=ShowFloatingDamageText=True
+CVars=TEXTUREGROUP_Character=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterNormalMap=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_CharacterSpecular=(MinLODSize=1,MaxLODSize=4,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Cinematic=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Effects=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=linear,MipFilter=point)
+CVars=TEXTUREGROUP_EffectsNotFiltered=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Lightmap=(MinLODSize=1,MaxLODSize=8,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_MobileFlattened=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_RenderTarget=(MinLODSize=1,MaxLODSize=128,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Shadowmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point,NumStreamedMips=3)
+CVars=TEXTUREGROUP_Skybox=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Heightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Terrain_Weightmap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_UI=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Vehicle=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleNormalMap=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_VehicleSpecular=(MinLODSize=1,MaxLODSize=256,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_Weapon=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponNormalMap=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WeaponSpecular=(MinLODSize=1,MaxLODSize=64,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_World=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldNormalMap=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=TEXTUREGROUP_WorldSpecular=(MinLODSize=1,MaxLODSize=2,LODBias=0,MinMagFilter=aniso,MipFilter=point)
+CVars=r.AOTrimOldRecordsFraction=0
+CVars=r.AmbientOcclusionLevels=0
+CVars=r.Atmosphere=0
+CVars=r.BloomQuality=0
+CVars=r.ClearWithExcludeRects=0
+CVars=r.CompileShadersForDevelopment=0
+CVars=r.DefaultFeature.AmbientOcclusion=False
+CVars=r.DefaultFeature.AntiAliasing=0
+CVars=r.DefaultFeature.AutoExposure=False
+CVars=r.DefaultFeature.Bloom=False
+CVars=r.DefaultFeature.LensFlare=False
+CVars=r.DefaultFeature.MotionBlur=False
+CVars=r.DepthOfFieldQuality=0
+CVars=r.DetailMode=0
+CVars=r.EarlyZPass=0
+CVars=r.ExposureOffset=0.3
+CVars=r.HZBOcclusion=0
+CVars=r.LensFlareQuality=0
+CVars=r.LightFunctionQuality=0
+CVars=r.LightShaftQuality=0
+CVars=r.LightShafts=0
+CVars=r.MaxAnisotropy=0
+CVars=r.MotionBlurQuality=0
+CVars=r.OneFrameThreadLag=1
+CVars=r.PostProcessAAQuality=0
+CVars=r.ReflectionEnvironment=0
+CVars=r.RefractionQuality=0
+CVars=r.SSAOSmartBlur=0
+CVars=r.SSR.Quality=0
+CVars=r.SSS.SampleSet=0
+CVars=r.SSS.Scale=0
+CVars=r.SceneColorFringe.Max=0
+CVars=r.SceneColorFringeQuality=0
+CVars=r.Shadow.CSM.MaxCascades=1
+CVars=r.Shadow.CSM.TransitionScale=0
+CVars=r.Shadow.DistanceScale=0.1
+CVars=r.Shadow.MaxResolution=2
+CVars=r.Shadow.MinResolution=2
+CVars=r.Shadow.RadiusThreshold=0.1
+CVars=r.ShadowQuality=0
+CVars=r.TonemapperQuality=0
+CVars=r.TriangleOrderOptimization=1
+CVars=r.TrueSkyQuality=0
+CVars=r.UpsampleQuality=0
+CVars=r.ViewDistanceScale=0
'''


# function add variable to ini file
def addVariable(wordCheck,variable,firstLine):

    with open('file/BaseDeviceProfiles.ini', 'r') as file:
        lines = file.readlines()
    for line_number, line in enumerate(lines, start=1):
        if line_number >= firstLine and wordCheck in line:
            checked = wordCheck
                
            break
    else:
        checked = 'none'


    if checked == wordCheck:
        pass
    else:
        file = open('file/BaseDeviceProfiles.ini', 'r')
        lines = file.readlines()
        file.close()
        lines.insert(firstLine, variable)
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
        renameFile(lablePath.get()+'/Engine/Content/EngineMaterials/DefaultDiffuse.uasset','file/DefaultDiffuse.uasset')

    if (mapRainbow.get() == 1):
        defaultFile.set(0)
        checkAndRename(lablePath.get()+'/Engine/Content/EngineMaterials/WeightMapPlaceholderTexture.uasset','file/WeightMapPlaceholderTexture.uasset')
        checkAndRename(lablePath.get()+'/Engine/Content/EngineResources/DefaultTexture.uasset','file/DefaultTexture.uasset')
    else:
        renameFile(lablePath.get()+'/Engine/Content/EngineMaterials/WeightMapPlaceholderTexture.uasset','file/WeightMapPlaceholderTexture.uasset')
        renameFile(lablePath.get()+'/Engine/Content/EngineResources/DefaultTexture.uasset','file/DefaultTexture.uasset')
    if (topWater.get() == 1):
        defaultFile.set(0)
        checkAndRename(lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient.uasset','file/SoftEdgeGradient.uasset')
        checkAndRename(lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient_Linear.uasset','file/SoftEdgeGradient_Linear.uasset')
    else:
        renameFile(lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient.uasset','file/SoftEdgeGradient.uasset')
        renameFile(lablePath.get()+'/ShooterGame/Content/PrimalEarth/Effects/Textures/Generic/SoftEdgeGradient_Linear.uasset','file/SoftEdgeGradient_Linear.uasset')
    
    tk.messagebox.showinfo(title=None, message='Done')
    answer = tk.messagebox.askyesno(title=None, message='Do you want to Restart game')
    if answer:
        reload_game_thread()


# move file
def copyFile(old_file,new_file):
    
    file = old_file
    destination = new_file
    shutil.copy(file, destination)


# rename file
def renameFile(file,old_name):
    
    if os.path.exists(file) and os.path.exists(file+'1'):
        os.remove(file+'1')
    elif os.path.exists(file+'1'):
        before = file+'1'
        after = file
        os.rename(before,after)
    elif os.path.exists(file):
        pass
    else:
        storage = old_name
        destination = file
        shutil.copy(storage, destination)    
        



#check first and rename
def checkAndRename(path,old_name):
    
    if os.path.exists(path):
        if (os.path.exists(path+'1') and os.path.exists(path)):
            os.remove(path)
    elif os.path.exists(path+'1'):
        if (os.path.exists(path)):
            os.remove(path)
    else:
        file = old_name
        destination = path
        shutil.copy(file, destination)
        
        before = path
        after = path+'1'
        os.rename(before,after)


# Define the function to reload the game
def reload_game():
    # Create a new thread
    t = threading.Thread(target=reload_game_thread)
    t.start()


# Define the function to run in the thread
def reload_game_thread():
    # Check if the game is running
    for p in psutil.process_iter():
        if p.name() == "ShooterGame.exe":
            # Close the game if it is running
            os.system("taskkill /f /im ShooterGame.exe")
            # Wait for game to sync with Steam cloud
            time.sleep(10)
            # Reload the game
            if os.path.exists("C:/Program Files (x86)/Steam/steam.exe"):
                subprocess.Popen(r"C:\Program Files (x86)\Steam\steam.exe -applaunch 346110")
            elif os.path.exists("D:/Steam/steam.exe"):
                subprocess.Popen(r"D:Steam\steam.exe -applaunch 346110")
            elif os.path.exists("E:/Steam/steam.exe"):
                subprocess.Popen(r"E:Steam\steam.exe -applaunch 346110")
            else:
                subprocess.Popen(lablePath.get() + '/ShooterGame/Binaries/Win64/ShooterGame_BE.exe')
            break
    else:
        tk.messagebox.showerror(title=None, message='Game is closed')



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


Label(app, textvariable=lablePath).pack(side=tk.BOTTOM)
lablePath.set(location)
browsePathBtn = tk.Button(
    app, text="Browse\nGame Location", command=getfilepath)
browsePathBtn.place(relx=.5, rely=.5,anchor= CENTER)

# get data from gamelocation.txt
getData()
    
app.config(menu=mainMenu)
app.mainloop()