import requests
import tarfile
import subprocess
import os
import sys
import argparse

def get_discord_download_path(args: Object) -> str:
    path = ""
    print(args.type)
    match args.type:
        case "canary":
            path = "https://discord.com/api/download/canary?platform=linux&format=tar.gz"
        case "ptb":
            path = "https://discord.com/api/download/ptb?platform=linux&format=tar.gz"
        case "stable":
            path = "https://discord.com/api/download?platform=linux&format=tar.gz"

    display_verbose_message(args.verbose, f"Downloading discord file with path: {path}")
    return path


def get_discord_launch_path(args: Object) -> str:
    path = ""
    match args.type:
        case "canary":
            path = "./DiscordCanary/discord-canary"
        case "ptb":
            path = "./DiscordPTB/discord-ptb"
        case "stable":
            path = "./Discord/Discord"

    display_verbose_message(args.verbose, f"Launching discord with path: {path}")
    return path


def download_discord(fileName: str, args: Object) -> None:
    print("Downloading Discord...")

    path = get_discord_download_path(args)
    download_file = requests.get(path)

    with open(f"{fileName}.tar.gz", "wb") as file:
        file.write(download_file.content)

        display_verbose_message(args.verbose,"File downloaded.  Unzipping...")
        with tarfile.open(f"{fileName}.tar.gz", "r") as tar:
            tar.extractall(filter="tar")
        os.remove(f"{fileName}.tar.gz")

        display_verbose_message(args.verbose,"File unzipped.")

def run_discord(args) -> None:
    print("Running Discord...")
    path = get_discord_launch_path(args)

    subprocess.run([path],shell=True)
    display_verbose_message(args.verbose,"Discord subprocess launched.")


def display_verbose_message(is_verbose: bool, msg: str) -> None:
    if is_verbose:
        print(msg)


if __name__ == "__main__":

    argParse = argparse.ArgumentParser(
        prog="Discord Updater",
        description="Program that can download/update and launch discord.  Assumes running on linux."
    )
    argParse.add_argument("-nl","--no-launch",help="Prevent Discord from launching when downloaded", action="store_true")
    argParse.add_argument("-nd","--no-update",help="Only launch discord and do not update", action="store_true")
    argParse.add_argument("-p","--path",help="Specifies download path of discord")
    argParse.add_argument("-v","--verbose",help="Enables verbose mode for updater", action="store_true")
    argParse.add_argument("-t","--type",help="Type of discord version to update.  Default is Canary",
                          choices=["canary","ptb","stable"], default="canary")
    argParse.add_argument("--version", help="Displays updater version",  action="version", version="%(prog)s 2.0")
    args = argParse.parse_args()


    dir_to_use = os.path.dirname(os.path.abspath(__file__))
    if args.path is not None:
        dir_to_use = args.path
    print(f"Using {dir_to_use}")
    os.chdir(dir_to_use)

    if not args.no_update:
        download_discord("discord_update_file",args)
    if not args.no_launch:
        run_discord(args)
