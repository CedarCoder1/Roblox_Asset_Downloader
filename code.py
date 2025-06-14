import os
import requests
import zipfile
# AppSettings.xml is missing! (Probably isn't even included.)
# Please put the engine downloads into one function. Like this: def download_engine(versionHash):
platform = input("Which platform? (Windows, Mac OS): ").lower() # , RCCService, Extra's)
versionHash = input("What version? Type list to get a list downloaded. (For example: 012239e64a274975): ")
buildtype = "" # buildtype is set somewhere else.      

temp_dir = os.path.join(os.getcwd(), "Output") 
extra_dir = os.path.join(os.getcwd(), "Extra's")   
downloadVersionSite = "https://setup.rbxcdn.com/version-"                                 

def download_file(url):
    print("Downloading " + url.split('/')[3])
    local_filename = url
    if local_filename.find("content-platform") != -1:
        local_filename = url.split('-')[4]
    elif local_filename.find("content-api") != -1:
        local_filename = "content-api-docs.zip"
    elif local_filename.find("content") != -1 or local_filename.find("extracontent") != -1:
        local_filename = url.split('-')[3]
    else:
        local_filename = url.split('-')[2]
    location = os.path.join(temp_dir, local_filename)

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(location, 'wb') as f:
          for chunk in r.iter_content(chunk_size=8192): 
            # If you have chunk encoded response uncomment if
            # and set chunk_size parameter to None.
            #if chunk: 
            f.write(chunk)
    print("Successfully downloaded: " + str(local_filename))
    return local_filename

def download_extra(url):
    print("Downloading " + url.split('/')[3])
    local_filename = url
    if local_filename.find("-API-Dump.json") != -1:
        local_filename = "API-Dump.json"
    elif local_filename.find("-") != -1:
        local_filename = url.split('-')[2]
    elif local_filename.find("mac/") != -1:
        local_filename = url.split('/')[4]
    else:
        local_filename = url.split('/')[3]

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        with open(os.path.join(extra_dir, local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    print("Successfully downloaded: " + str(local_filename))
    return local_filename

def unzip_file(file, OtherLocation):
    if OtherLocation == "Content": 
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(os.path.join(temp_dir, "content", file.split('.')[0]))
    elif OtherLocation == True:
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(os.path.join(temp_dir, file.split('.')[0]))
    elif OtherLocation == False:
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(temp_dir)
    elif OtherLocation == "ContentTextures": 
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(os.path.join(temp_dir, "content", "textures"))
    elif OtherLocation == "PlatformContent": 
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(os.path.join(temp_dir, "PlatformContent", "pc", file.split('.')[0]))
    elif OtherLocation == "ExtraContent": 
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(os.path.join(temp_dir, "ExtraContent", file.split('.')[0]))
    elif OtherLocation == "Qt5": 
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(os.path.join(temp_dir, "Plugins", file.split('.')[0]))
    elif OtherLocation == "PlatformContent-shared_compression_dictionaries": 
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(os.path.join(temp_dir, "PlatformContent", "pc", "shared_compression_dictionaries"))
    elif OtherLocation == "content-api_docs": 
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(os.path.join(temp_dir, "content", "api_docs"))
    os.remove(os.path.join(temp_dir, file))
    print("Successfully unzipped: " + str(file))
    return file

def unzip_extra(file):
    with zipfile.ZipFile(os.path.join(extra_dir, file), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(extra_dir, file.split('.')[0]))
    os.remove(os.path.join(extra_dir, file))
    print("Successfully unzipped: " + str(file))
    return file

def download_engine(versionHash): # For downloading mutual folders and files.
    # Content
        os.makedirs(os.path.join(temp_dir, "content"), exist_ok=True)

        # Content Avatar
        download = download_file(downloadVersionSite + versionHash + "-content-avatar.zip")
        unzip = unzip_file("avatar.zip", "Content")
        
        # Content Sky
        download = download_file(downloadVersionSite + versionHash + "-content-sky.zip")
        unzip = unzip_file("sky.zip", "Content")
        
        # Content Sounds
        download = download_file(downloadVersionSite + versionHash + "-content-sounds.zip")
        unzip = unzip_file("sounds.zip", "Content")
        
        # Content Models
        download = download_file(downloadVersionSite + versionHash + "-content-models.zip")
        unzip = unzip_file("models.zip", "Content")
        
        # Content Configs
        download = download_file(downloadVersionSite + versionHash + "-content-configs.zip")
        unzip = unzip_file("configs.zip", "Content")
        
        # Content Fonts
        download = download_file(downloadVersionSite + versionHash + "-content-fonts.zip")
        unzip = unzip_file("fonts.zip", "Content")
        
        # Content Textures
        os.makedirs(os.path.join(temp_dir, "content", "textures"), exist_ok=True)
        
        # Content Textures2
        download = download_file(downloadVersionSite + versionHash + "-content-textures2.zip")
        unzip = unzip_file("textures2.zip", "ContentTextures")

        os.makedirs(os.path.join(temp_dir, "ExtraContent"), exist_ok=True)

        # ExtraContent luapackages
        download = download_file(downloadVersionSite + versionHash + "-extracontent-luapackages.zip")
        unzip = unzip_file("luapackages.zip", "ExtraContent")

        # ExtraContent models
        download = download_file(downloadVersionSite + versionHash + "-extracontent-models.zip")
        unzip = unzip_file("models.zip", "ExtraContent")
        
        # ExtraContent textures
        download = download_file(downloadVersionSite + versionHash + "-extracontent-textures.zip")
        unzip = unzip_file("textures.zip", "ExtraContent")

        # ExtraContent translations
        download = download_file(downloadVersionSite + versionHash + "-extracontent-translations.zip")
        unzip = unzip_file("translations.zip", "ExtraContent")

# List Downloader
if versionHash.lower() == "list":
    # RobloxApp
    download = download_extra("https://setup.rbxcdn.com/DeployHistory.txt")
    os.rename(os.path.join(extra_dir, "DeployHistory.txt"), os.path.join(extra_dir, "DeployHistory (Windows).txt"))
    download = download_extra("https://setup.rbxcdn.com/mac/DeployHistory.txt")
    os.rename(os.path.join(extra_dir, "DeployHistory.txt"), os.path.join(extra_dir, "DeployHistory (Mac OS).txt"))
    print("Downloaded the list and put it into the Extra's folder.")
    input("Done running, press Enter to exit.")
    exit()

# Here so the list downloader doesn't ask an useless question.
buildType = input("Studio or Player?: ").lower() 

# Windows
if platform == "windows":
    print("Starting downloads for Windows.")
    # Player
    if buildType == "player":
        # RobloxApp
        download = download_file(downloadVersionSite + versionHash + "-RobloxApp.zip")
        unzip = unzip_file(download, False)

        # redist
        download = download_file(downloadVersionSite + versionHash + "-redist.zip")
        unzip = unzip_file(download, False)

        # RobloxPlayerLauncher
        download = download_file(downloadVersionSite + versionHash + "-RobloxPlayerLauncher.exe")

        # RobloxPlayerInstaller
        download = download_file(downloadVersionSite + versionHash + "-RobloxPlayerInstaller.exe")

        # WebView2
        download = download_file(downloadVersionSite + versionHash + "-WebView2.zip")
        unzip = unzip_file(download, False)

        # WebView2RuntimeInstaller.zip
        download = download_file(downloadVersionSite + versionHash + "-WebView2RuntimeInstaller.zip")
        unzip = unzip_file(download, True)

        # ssl
        download = download_file(downloadVersionSite + versionHash + "-ssl.zip")
        unzip = unzip_file(download, True)

        # shaders
        download = download_file(downloadVersionSite + versionHash + "-shaders.zip")
        unzip = unzip_file(download, True)

    # Content
        download_engine(versionHash)
        
    # Platform Content
        os.makedirs(os.path.join(temp_dir, "PlatformContent", "pc"), exist_ok=True)

        # (Platform)Content Textures3
        download = download_file(downloadVersionSite + versionHash + "-content-textures3.zip")
        unzip = unzip_file("textures3.zip", "PlatformContent")
        os.rename(os.path.join(temp_dir, "PlatformContent", "pc", "textures3"), os.path.join(temp_dir, "PlatformContent", "pc", "textures")) # Otherwise the name isn't accurate.

        # PlatformContent Terrain
        download = download_file(downloadVersionSite + versionHash + "-content-terrain.zip")
        unzip = unzip_file("terrain.zip", "PlatformContent")

        # PlatformContent dictionaries
        download = download_file(downloadVersionSite + versionHash + "-content-platform-dictionaries.zip")
        unzip = unzip_file("dictionaries.zip", "PlatformContent-shared_compression_dictionaries")

        # PlatformContent fonts
        download = download_file(downloadVersionSite + versionHash + "-content-platform-fonts.zip")
        unzip = unzip_file("fonts.zip", "PlatformContent")

    # ExtraContent
        download_engine(versionHash)

        # ExtraContent places
        download = download_file(downloadVersionSite + versionHash + "-extracontent-places.zip")
        unzip = unzip_file("places.zip", "ExtraContent")

    # EXTRA'S
        # rbxManifest
        download = download_extra(downloadVersionSite + versionHash + "-rbxManifest.txt")

        # rbxPkgManifest
        download = download_extra(downloadVersionSite + versionHash + "-rbxPkgManifest.txt")

# Studio        
    elif buildType == "studio":
        # redist
        download = download_file(downloadVersionSite + versionHash + "-redist.zip")
        unzip = unzip_file(download, False)

        # RobloxStudio
        download = download_file(downloadVersionSite + versionHash + "-RobloxStudio.zip")
        unzip = unzip_file(download, False)

        # RibbonConfig
        download = download_file(downloadVersionSite + versionHash + "-RibbonConfig.zip")
        unzip = unzip_file(download, True)

        # ApplicationConfig
        download = download_file(downloadVersionSite + versionHash + "-ApplicationConfig.zip")
        unzip = unzip_file(download, True)

        # BuiltInPlugins
        download = download_file(downloadVersionSite + versionHash + "-BuiltInPlugins.zip")
        unzip = unzip_file(download, True)

        # BuiltInStandalonePlugins
        download = download_file(downloadVersionSite + versionHash + "-BuiltInStandalonePlugins.zip")
        unzip = unzip_file(download, True)

        # Libraries
        download = download_file(downloadVersionSite + versionHash + "-Libraries.zip")
        unzip = unzip_file(download, False)

        # LibrariesQt5
        download = download_file(downloadVersionSite + versionHash + "-LibrariesQt5.zip")
        unzip = unzip_file(download, False)

        # Plugins
        download = download_file(downloadVersionSite + versionHash + "-Plugins.zip")
        unzip = unzip_file(download, True)

        # RobloxStudioInstaller.exe
        download = download_file(downloadVersionSite + versionHash + "-RobloxStudioInstaller.exe")

        # StudioFonts
        download = download_file(downloadVersionSite + versionHash + "-StudioFonts.zip")
        unzip = unzip_file(download, True)

        # WebView2
        download = download_file(downloadVersionSite + versionHash + "-WebView2.zip")
        unzip = unzip_file(download, False)

        # WebView2RuntimeInstaller
        download = download_file(downloadVersionSite + versionHash + "-WebView2RuntimeInstaller.zip")
        unzip = unzip_file(download, True)

        # shaders
        download = download_file(downloadVersionSite + versionHash + "-shaders.zip")
        unzip = unzip_file(download, True)

        # ssl
        download = download_file(downloadVersionSite + versionHash + "-ssl.zip")
        unzip = unzip_file(download, True)

    # Content
        download_engine(versionHash)

        # Content api-docs
        download = download_file(downloadVersionSite + versionHash + "-content-api-docs.zip")
        unzip = unzip_file(download, "content-api_docs")

        # Content studio_svg_textures
        download = download_file(downloadVersionSite + versionHash + "-content-studio_svg_textures.zip")
        unzip = unzip_file(download, "Content")

        # Content qt_translations
        download = download_file(downloadVersionSite + versionHash + "-content-qt_translations.zip")
        unzip = unzip_file(download, "Content")

    # ExtraContent
        download_engine(versionHash)

        # ExtraContent scripts
        download = download_file(downloadVersionSite + versionHash + "-extracontent-scripts.zip")
        unzip = unzip_file(download, "ExtraContent")

    # Platform Content
        os.makedirs(os.path.join(temp_dir, "PlatformContent", "pc"), exist_ok=True)

        # (Platform)Content Textures3
        download = download_file(downloadVersionSite + versionHash + "-content-textures3.zip")
        unzip = unzip_file(download, "PlatformContent")
        os.rename(os.path.join(temp_dir, "PlatformContent", "pc", "textures3"), os.path.join(temp_dir, "PlatformContent", "pc", "textures")) # Otherwise the name isn't accurate.

        # PlatformContent Terrain
        download = download_file(downloadVersionSite + versionHash + "-content-terrain.zip")
        unzip = unzip_file(download, "PlatformContent")

        # PlatformContent dictionaries
        download = download_file(downloadVersionSite + versionHash + "-content-platform-dictionaries.zip")
        unzip = unzip_file(download, "PlatformContent-shared_compression_dictionaries")

        # PlatformContent fonts
        download = download_file(downloadVersionSite + versionHash + "-content-platform-fonts.zip")
        unzip = unzip_file(download, "PlatformContent")

    # EXTRA'S

        # API Dump
        download = download_extra(downloadVersionSite + versionHash + "-API-Dump.json")

        # Version.txt
        download = download_extra(downloadVersionSite + versionHash + "-API-Dump.json")

        # rbxManifest
        download = download_extra(downloadVersionSite + versionHash + "-rbxManifest.txt")

        # rbxPkgManifest
        download = download_extra(downloadVersionSite + versionHash + "-rbxPkgManifest.txt")

        # RobloxStudioLauncherBeta.exe
        download = download_extra(downloadVersionSite + versionHash + "-RobloxStudioLauncherBeta.exe")

# Mac OS
if platform == "mac os":
    print("Starting downloads for Mac OS.")
    
# RCCService
if platform == "rccservice":
    print("Starting downloads for RCCService.") 

# Extra's
if platform == "extra's":
    print("Starting downloads for Extra's.") 
    
input("Done running, press Enter to exit.")
# type: ignore
