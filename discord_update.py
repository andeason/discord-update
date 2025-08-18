import requests
import tarfile
import subprocess
import os

fileName = "discord_update_file"
currentDir = os.path.dirname(os.path.abspath(__file__))
print(f"Using {currentDir}")
os.chdir(currentDir)

print("Downloading file...")
downloadFile = requests.get("https://discord.com/api/download/canary?platform=linux&format=tar.gz")

try:
    with open(f"{fileName}.tar.gz", "wb") as file:
        file.write(downloadFile.content)

        print("File downloaded.  Unzipping...")
        with tarfile.open(f"{fileName}.tar.gz", "r:gz") as tar:
            tar.extractall(filter="tar")

    os.remove(f"{fileName}.tar.gz")
    print("File unzipped.  Launching Discord...")


    subprocess.run(["./DiscordCanary/DiscordCanary"],shell=True)
    print("Done.")


except Exception as e:
    print(f"An Error occurred while downloading/unzipping: {e}")

