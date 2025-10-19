import os
import requests
import zipfile

platform = input("Which platform? (Windows, Mac OS, RCCService, Extra's): ").lower()
versionHash = input("What version hash? Type list to get a list downloaded. (For example: 012239e64a274975): ")
buildtype = "" # buildtype is set somewhere else.
temp_dir = os.path.join(os.getcwd(), "Output")
extra_dir = os.path.join(os.getcwd(), "Extra's")
downloadVersionSite = "https://setup.rbxcdn.com/version-"
downloadVersionSiteMac = "https://setup.rbxcdn.com/mac/version-"

def download_file(url):
    print("Downloading " + url.split('/')[3])
    local_filename = url
    if local_filename.find("content-platform") != -1:
        local_filename = url.split('-')[4]
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
    elif OtherLocation == "StudioContent": 
        with zipfile.ZipFile(os.path.join(temp_dir, file), 'r') as zip_ref:
          zip_ref.extractall(os.path.join(temp_dir, "StudioContent", file.split('.')[0]))
    os.remove(os.path.join(temp_dir, file))
    print("Successfully unzipped: " + str(file))
    return file

def unzip_extra(file):
    with zipfile.ZipFile(os.path.join(extra_dir, file), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(extra_dir, file.split('.')[0]))
    os.remove(os.path.join(extra_dir, file))
    print("Successfully unzipped: " + str(file))
    return file

# List Downloader
if versionHash == "list":
    # RobloxApp
    download = download_extra("https://setup.rbxcdn.com/DeployHistory.txt")
    os.rename(os.path.join(extra_dir, "DeployHistory.txt"), os.path.join(extra_dir, "DeployHistory (Windows).txt"))
    download = download_extra("https://setup.rbxcdn.com/mac/DeployHistory.txt")
    os.rename(os.path.join(extra_dir, "DeployHistory.txt"), os.path.join(extra_dir, "DeployHistory (Mac OS).txt"))
    print("Downloaded the list and put it into the Extra's folder.")
    input("Done running, press Enter to exit.")
    exit()

# Windows
elif platform == "windows" or platform ==  "1":
    # Here so the other downloaders don't ask useless questions.
    buildType = input("Studio or Player?: ").lower()
    print("Starting downloads for Windows." + "\n" + "-" * 20)
    # Player
    if buildType == "player" or buildType ==  "2":
        # rbxPkgManifest download + list maker.
        download = download_extra(downloadVersionSite + versionHash + "-rbxPkgManifest.txt")
        with open(os.path.join(extra_dir, download), "r") as manifest_file:
            manifest = manifest_file.read()
        
        downloaded_files = [] # Part of the system that tells the user what folders are missing download support.

        # Folders that have to be made.
        os.makedirs(os.path.join(temp_dir, "content"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "content", "textures"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "PlatformContent", "pc"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "ExtraContent"), exist_ok=True)

        for line in manifest.splitlines():
            if line.endswith(".zip") or line.endswith(".exe"):
                print(line)
                if "RobloxApp.zip" in line: # RobloxApp.zip
                    download = download_file(downloadVersionSite + versionHash + "-RobloxApp.zip")
                    unzip = unzip_file(download, False)
                    downloaded_files.insert(1, "RobloxApp.zip") # Keeps track of downloaded files using a table.
                elif "RobloxPlayerInstaller.exe" in line: # RobloxPlayerInstaller.exe
                    download = download_file(downloadVersionSite + versionHash + "-RobloxPlayerInstaller.exe")
                    downloaded_files.insert(1, "RobloxPlayerInstaller.exe")
                elif "redist.zip" in line: # redist.zip
                    download = download_file(downloadVersionSite + versionHash + "-redist.zip")
                    unzip = unzip_file(download, False)
                    downloaded_files.insert(1, "redist.zip")
                elif "RobloxPlayerLauncher.exe" in line: # RobloxPlayerLauncher.exe
                    download = download_file(downloadVersionSite + versionHash + "-RobloxPlayerLauncher.exe")
                    downloaded_files.insert(1, "RobloxPlayerLauncher.exe")
                elif "WebView2.zip" in line: # WebView2.zip
                    download = download_file(downloadVersionSite + versionHash + "-WebView2.zip")
                    unzip = unzip_file(download, False)
                    downloaded_files.insert(1, "WebView2.zip")
                elif "WebView2RuntimeInstaller.zip" in line: # WebView2RuntimeInstaller.zip
                    download = download_file(downloadVersionSite + versionHash + "-WebView2RuntimeInstaller.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "WebView2RuntimeInstaller.zip")
                elif "ssl.zip" in line: # ssl.zip
                    download = download_file(downloadVersionSite + versionHash + "-ssl.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "ssl.zip")
                elif "shaders.zip" in line: # shaders.zip
                    download = download_file(downloadVersionSite + versionHash + "-shaders.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "shaders.zip")
                # Content
                elif "content-avatar.zip" in line: # content-avatar.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-avatar.zip")
                    unzip = unzip_file("avatar.zip", "Content")
                    downloaded_files.insert(1, "content-avatar.zip")
                elif "content-sky.zip" in line: # content-sky.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-sky.zip")
                    unzip = unzip_file("sky.zip", "Content")
                    downloaded_files.insert(1, "content-sky.zip")
                elif "content-sounds.zip" in line: # content-sounds.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-sounds.zip")
                    unzip = unzip_file("sounds.zip", "Content")
                    downloaded_files.insert(1, "content-sounds.zip")
                elif "content-models.zip" in line and not "extra" in line: # content-models.zip <-- With extra check to stop extracontent-models from glitching out.
                    download = download_file(downloadVersionSite + versionHash + "-content-models.zip")
                    unzip = unzip_file("models.zip", "Content")
                    downloaded_files.insert(1, "content-models.zip")
                elif "content-configs.zip" in line: # content-configs.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-configs.zip")
                    unzip = unzip_file("configs.zip", "Content")
                    downloaded_files.insert(1, "content-configs.zip")
                elif "content-fonts.zip" in line: # content-fonts.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-fonts.zip")
                    unzip = unzip_file("fonts.zip", "Content")
                    downloaded_files.insert(1, "content-fonts.zip")
                elif "content-textures2.zip" in line: # content-textures2.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-textures2.zip")
                    unzip = unzip_file("textures2.zip", "ContentTextures")
                    downloaded_files.insert(1, "content-textures2.zip")
                # PlatformContent
                elif "content-textures3.zip" in line: # content-textures3.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-textures3.zip")
                    unzip = unzip_file("textures3.zip", "PlatformContent")
                    os.rename(os.path.join(temp_dir, "PlatformContent", "pc", "textures3"), os.path.join(temp_dir, "PlatformContent", "pc", "textures")) # Otherwise the name isn't accurate.
                    downloaded_files.insert(1, "content-textures3.zip")
                elif "content-terrain.zip" in line: # content-terrain.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-terrain.zip")
                    unzip = unzip_file("terrain.zip", "PlatformContent")
                    downloaded_files.insert(1, "content-terrain.zip")
                elif "content-platform-dictionaries.zip" in line: # content-platform-dictionaries.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-platform-dictionaries.zip")
                    unzip = unzip_file("dictionaries.zip", "PlatformContent")
                    downloaded_files.insert(1, "content-platform-dictionaries.zip")
                elif "content-platform-fonts.zip" in line: # content-platform-fonts.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-platform-fonts.zip")
                    unzip = unzip_file("fonts.zip", "PlatformContent")
                    downloaded_files.insert(1, "content-platform-fonts.zip")
                # ExtraContent
                elif "extracontent-luapackages.zip" in line: # extracontent-luapackages.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-luapackages.zip")
                    unzip = unzip_file("luapackages.zip", "ExtraContent")
                    downloaded_files.insert(1, "extracontent-luapackages.zip")
                elif "extracontent-models.zip" in line: # extracontent-models.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-models.zip")
                    unzip = unzip_file("models.zip", "ExtraContent")
                    downloaded_files.insert(1, "extracontent-models.zip")
                elif "extracontent-places.zip" in line: # extracontent-places.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-places.zip")
                    unzip = unzip_file("places.zip", "ExtraContent")
                    downloaded_files.insert(1, "extracontent-places.zip")
                elif "extracontent-textures.zip" in line: # extracontent-textures.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-textures.zip")
                    unzip = unzip_file("textures.zip", "ExtraContent")
                    downloaded_files.insert(1, "extracontent-textures.zip")
                elif "extracontent-translations.zip" in line: # extracontent-translations.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-translations.zip")
                    unzip = unzip_file("translations.zip", "ExtraContent")
                    downloaded_files.insert(1, "extracontent-translations.zip")
        # EXTRA's
        download = download_extra(downloadVersionSite + versionHash + "-rbxManifest.txt") # rbxManifest

        # File Check
        print("-" * 20)
        fileCheckTable = []
        for entry in manifest.splitlines(): # Go through each documented downloaded file.
            if entry not in downloaded_files and (entry.endswith(".zip") or entry.endswith(".exe")):
                fileCheckTable.insert(1, entry)
           
        for entry in fileCheckTable:
            print(entry + " not downloaded.")

    # Studio
    elif buildType == "studio" or buildType == "1":
        # rbxPkgManifest download + list maker.
        download = download_extra(downloadVersionSite + versionHash + "-rbxPkgManifest.txt")
        with open(os.path.join(extra_dir, download), "r") as manifest_file:
            manifest = manifest_file.read()
        
        downloaded_files = [] # Part of the system that tells the user what folders are missing download support.

        # Folders that have to be made.
        os.makedirs(os.path.join(temp_dir, "content"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "content", "textures"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "PlatformContent", "pc"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "ExtraContent"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "StudioContent"), exist_ok=True)

        for line in manifest.splitlines():
            if line.endswith(".zip") or line.endswith(".exe"):
                print(line)
                if "ApplicationConfig.zip" in line: # ApplicationConfig.zip
                    download = download_file(downloadVersionSite + versionHash + "-ApplicationConfig.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "ApplicationConfig.zip") # Keeps track of downloaded files using a table.
                elif "redist.zip" in line: # redist.zip
                    download = download_file(downloadVersionSite + versionHash + "-redist.zip")
                    unzip = unzip_file(download, False)
                    downloaded_files.insert(1, "redist.zip")
                elif "RobloxStudio.zip" in line: # RobloxStudio.zip
                    download = download_file(downloadVersionSite + versionHash + "-RobloxStudio.zip")
                    unzip = unzip_file(download, False)
                    downloaded_files.insert(1, "RobloxStudio.zip")
                    # RobloxStudioInstaller.exe <-- Doing this, cuz the .exe is missing from the manifest files.
                    download = download_file(downloadVersionSite + versionHash + "-RobloxStudioInstaller.exe")
                    downloaded_files.insert(1, "RobloxStudioInstaller.exe")
                elif "RibbonConfig.zip" in line: # RibbonConfig.zip
                    download = download_file(downloadVersionSite + versionHash + "-RibbonConfig.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "RibbonConfig.zip")
                elif "BuiltInPlugins.zip" in line: # BuiltInPlugins.zip
                    download = download_file(downloadVersionSite + versionHash + "-BuiltInPlugins.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "BuiltInPlugins.zip")
                elif "BuiltInStandalonePlugins.zip" in line: # BuiltInStandalonePlugins.zip
                    download = download_file(downloadVersionSite + versionHash + "-BuiltInStandalonePlugins.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "BuiltInStandalonePlugins.zip")
                elif "Libraries.zip" in line: # Libraries.zip
                    download = download_file(downloadVersionSite + versionHash + "-Libraries.zip")
                    unzip = unzip_file(download, False)
                    downloaded_files.insert(1, "Libraries.zip")
                elif "LibrariesQt5.zip" in line: # LibrariesQt5.zip
                    download = download_file(downloadVersionSite + versionHash + "-LibrariesQt5.zip")
                    unzip = unzip_file(download, False)
                    downloaded_files.insert(1, "LibrariesQt5.zip")
                elif "Plugins.zip" in line: # Plugins.zip
                    download = download_file(downloadVersionSite + versionHash + "-Plugins.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "Plugins.zip")
                elif "StudioFonts.zip" in line: # StudioFonts.zip
                    download = download_file(downloadVersionSite + versionHash + "-StudioFonts.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "StudioFonts.zip")
                elif "WebView2.zip" in line: # WebView2.zip
                    download = download_file(downloadVersionSite + versionHash + "-WebView2.zip")
                    unzip = unzip_file(download, False)
                    downloaded_files.insert(1, "WebView2.zip")
                elif "WebView2RuntimeInstaller.zip" in line: # WebView2RuntimeInstaller.zip
                    download = download_file(downloadVersionSite + versionHash + "-WebView2RuntimeInstaller.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "WebView2RuntimeInstaller.zip")
                elif "shaders.zip" in line: # shaders.zip
                    download = download_file(downloadVersionSite + versionHash + "-shaders.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "shaders.zip")
                elif "ssl.zip" in line: # ssl.zip
                    download = download_file(downloadVersionSite + versionHash + "-ssl.zip")
                    unzip = unzip_file(download, True)
                    downloaded_files.insert(1, "ssl.zip")
                # Content
                elif "content-api-docs.zip" in line: # content-api-docs.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-api-docs.zip")
                    unzip = unzip_file(download, "Content")
                    downloaded_files.insert(1, "content-api-docs.zip")
                    os.rename(os.path.join(temp_dir, "Content", "api"), os.path.join(temp_dir, temp_dir, "Content", "api_docs")) # Otherwise the name isn't accurate.
                elif "content-avatar.zip" in line: # content-avatar.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-avatar.zip")
                    unzip = unzip_file(download, "Content")
                    downloaded_files.insert(1, "content-avatar.zip")
                elif "content-sky.zip" in line: # content-sky.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-sky.zip")
                    unzip = unzip_file(download, "Content")
                    downloaded_files.insert(1, "content-sky.zip")
                elif "content-sounds.zip" in line: # content-sounds.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-sounds.zip")
                    unzip = unzip_file(download, "Content")
                    downloaded_files.insert(1, "content-sounds.zip")
                elif "content-models.zip" in line and not "extra" in line and not "studio" in line: # content-models.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-models.zip")
                    unzip = unzip_file(download, "Content")
                    downloaded_files.insert(1, "content-models.zip")
                elif "content-configs.zip" in line: # content-configs.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-configs.zip")
                    unzip = unzip_file(download, "Content")
                    downloaded_files.insert(1, "content-configs.zip")
                elif "content-fonts.zip" in line: # content-fonts.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-fonts.zip")
                    unzip = unzip_file(download, "Content")
                    downloaded_files.insert(1, "content-fonts.zip")
                elif "content-studio_svg_textures.zip" in line: # content-studio_svg_textures.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-studio_svg_textures.zip")
                    unzip = unzip_file(download, "Content")
                    downloaded_files.insert(1, "content-studio_svg_textures.zip")
                elif "content-qt_translations.zip" in line: # content-qt_translations.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-qt_translations.zip")
                    unzip = unzip_file(download, "Content")
                    downloaded_files.insert(1, "content-qt_translations.zip")
                elif "content-textures2.zip" in line: # content-textures2.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-textures2.zip")
                    unzip = unzip_file(download, "ContentTextures")
                    downloaded_files.insert(1, "content-textures2.zip")
                # ExtraContent
                elif "extracontent-luapackages.zip" in line: # extracontent-luapackages.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-luapackages.zip")
                    unzip = unzip_file(download, "ExtraContent")
                    downloaded_files.insert(1, "extracontent-luapackages.zip")
                elif "extracontent-models.zip" in line: # extracontent-models.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-models.zip")
                    unzip = unzip_file(download, "ExtraContent")
                    downloaded_files.insert(1, "extracontent-models.zip")
                elif "extracontent-scripts.zip" in line: # extracontent-scripts.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-scripts.zip")
                    unzip = unzip_file(download, "ExtraContent")
                    downloaded_files.insert(1, "extracontent-scripts.zip")
                elif "extracontent-textures.zip" in line: # extracontent-textures.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-textures.zip")
                    unzip = unzip_file(download, "ExtraContent")
                    downloaded_files.insert(1, "extracontent-textures.zip")
                elif "extracontent-translations.zip" in line: # extracontent-translations.zip
                    download = download_file(downloadVersionSite + versionHash + "-extracontent-translations.zip")
                    unzip = unzip_file(download, "ExtraContent")
                    downloaded_files.insert(1, "extracontent-translations.zip")
                # PlatformContent
                elif "content-textures3.zip" in line: # content-textures3.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-textures3.zip")
                    unzip = unzip_file(download, "PlatformContent")
                    downloaded_files.insert(1, "content-textures3.zip")
                    os.rename(os.path.join(temp_dir, "PlatformContent", "pc", "textures3"), os.path.join(temp_dir, "PlatformContent", "pc", "textures")) # Otherwise the name isn't accurate.
                elif "content-terrain.zip" in line: # content-terrain.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-terrain.zip")
                    unzip = unzip_file(download, "PlatformContent")
                    downloaded_files.insert(1, "content-terrain.zip")
                elif "content-platform-dictionaries.zip" in line: # content-platform-dictionaries.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-platform-dictionaries.zip")
                    unzip = unzip_file(download, "PlatformContent")
                    downloaded_files.insert(1, "content-platform-dictionaries.zip")
                    os.rename(os.path.join(temp_dir, "PlatformContent", "pc", "dictionaries"), os.path.join(temp_dir, "PlatformContent", "pc", "shared_compression_dictionaries")) # Otherwise the name isn't accurate.
                elif "content-platform-fonts.zip" in line: # content-platform-fonts.zip
                    download = download_file(downloadVersionSite + versionHash + "-content-platform-fonts.zip")
                    unzip = unzip_file(download, "PlatformContent")
                    downloaded_files.insert(1, "content-platform-fonts.zip")
                # StudioContent
                elif "studiocontent-textures.zip" in line: # studiocontent-textures.zip
                    download = download_file(downloadVersionSite + versionHash + "-studiocontent-textures.zip")
                    unzip = unzip_file(download, "StudioContent")
                    downloaded_files.insert(1, "studiocontent-textures.zip")
                elif "studiocontent-models.zip" in line: # studiocontent-models.zip
                    download = download_file(downloadVersionSite + versionHash + "-studiocontent-models.zip")
                    unzip = unzip_file(download, "StudioContent")
                    downloaded_files.insert(1, "studiocontent-models.zip")
        # EXTRA'S
        # API Dump
        download = download_extra(downloadVersionSite + versionHash + "-API-Dump.json")
        # rbxManifest
        download = download_extra(downloadVersionSite + versionHash + "-rbxManifest.txt")
        # rbxPkgManifest
        download = download_extra(downloadVersionSite + versionHash + "-rbxPkgManifest.txt")

        # File Check
        print("-" * 20)
        fileCheckTable = []
        for entry in manifest.splitlines(): # Go through each documented downloaded file.
            if entry not in downloaded_files and (entry.endswith(".zip") or entry.endswith(".exe")):
                fileCheckTable.insert(1, entry)
           
        for entry in fileCheckTable:
            print(entry + " not downloaded.")

# Mac OS
elif platform == "mac os" or platform ==  "2":
    # Here so the other downloaders don't ask useless questions.
    buildType = input("Studio or Player?: ").lower()
    print("Starting downloads for Mac OS.")

    # Player
    if buildType == "player" or buildType ==  "2":
    # Main
        # Roblox.dmg
        download = download_file(downloadVersionSiteMac + versionHash + "-Roblox.dmg")
        unzip = unzip_file(download, False)
        
        # Roblox
        download = download_file(downloadVersionSiteMac + versionHash + "-Roblox.zip")
        unzip = unzip_file(download, False)
        
        # RobloxPlayer
        download = download_file(downloadVersionSiteMac + versionHash + "-RobloxPlayer.zip")
        unzip = unzip_file(download, False)

    # Studio        
    elif buildType == "studio" or buildType ==  "1":
    # Main
        # Roblox.dmg
        download = download_file(downloadVersionSiteMac + versionHash + "-RobloxStudio.dmg")
        unzip = unzip_file(download, False)
        
        # Roblox
        download = download_file(downloadVersionSiteMac + versionHash + "-RobloxStudio.zip")
        unzip = unzip_file(download, False)
        
        # RobloxPlayer
        download = download_file(downloadVersionSiteMac + versionHash + "-RobloxStudioApp.zip")
        unzip = unzip_file(download, False)
        
# RCCService
elif platform == "rccservice" or platform ==  "3":
    print("Starting downloads for RCCService.") 
    # RCCService
    download = download_file(downloadVersionSite + versionHash + "-RCCServiceR7Z9CYTW7WBR95VW.zip")
    unzip = unzip_file(download, False)

    # content
    download = download_file(downloadVersionSite + versionHash + "-RCC-contentXGTFDE2U040VW06D.zip")
    unzip = unzip_file(download, False)
 
    # extracontent
    download = download_file(downloadVersionSite + versionHash + "-RCC-extracontentXGTFDE2U040VW06D.zip")
    unzip = unzip_file(download, False)

    # Libraries
    download = download_file(downloadVersionSite + versionHash + "-RCC-LibrariesXGTFDE2U040VW06D.zip")
    unzip = unzip_file(download, False)

    # Libraries
    download = download_file(downloadVersionSite + versionHash + "-RCC-LibrariesXGTFDE2U040VW06D.zip")
    unzip = unzip_file(download, False)

    # platformcontent
    download = download_file(downloadVersionSite + versionHash + "-RCC-platformcontentXGTFDE2U040VW06D.zip")
    unzip = unzip_file(download, False)

    # redist
    download = download_file(downloadVersionSite + versionHash + "-RCC-redistXGTFDE2U040VW06D.zip")
    unzip = unzip_file(download, False)

    # RobloxA5XGEOZ35LAFQUL2.exe
    download = download_file(downloadVersionSite + versionHash + "-RCC-RobloxA5XGEOZ35LAFQUL2.exe")

    # shaders
    download = download_file(downloadVersionSite + versionHash + "-RCC-shadersXGTFDE2U040VW06D.zip")
    unzip = unzip_file(download, False)

    # ssl
    download = download_file(downloadVersionSite + versionHash + "-RCC-sslXGTFDE2U040VW06D.zip")
    unzip = unzip_file(download, False)

# Extra's
elif platform == "extra's" or platform ==  "4":
    print("Starting downloads for Extra's.") 
    
input("Done running, press Enter to exit.") # type: ignore
