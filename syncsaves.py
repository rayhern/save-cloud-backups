#
# Sync all my save games with all my devices, including Google Drive.
# Starting with Diablo.
# By Ray Hernandez
#
#

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# For using listdir() 
import os 
import time
import sys
import shutil
import sys
    
# Credentials for linux handheld / raspberry pi / rg350 / rg351
SSH_IP_ADDRESS = config['connection']['DEVICE_IP']
SSH_USER = config['connection']['DEVICE_USER']
SSH_PASSWORD = config['connection']['DEVICE_PASS']

# Save file paths
REMOTE_PSP_PATH = config['remote']['PSP_SAVE_PATH']
REMOTE_GBA_PATH = config['remote']['GBA_SAVE_PATH']
REMOTE_GBC_PATH = config['remote']['GBC_SAVE_PATH']
REMOTE_GB_PATH = config['remote']['GB_SAVE_PATH']
REMOTE_PSX_PATH= config['remote']['PSX_SAVE_PATH']
REMOTE_DIABLO_PATH = config['remote']['DIABLO_PATH']

DEVILUTION_SAVE_PATH = config['local']['DEVILUTION_SAVE_PATH']
LOCAL_PSP_PATH = config['local']['PSP_SAVE_PATH']

# Make sure that you install the google drive client on your mac/pc.
LOCAL_GOOGLE_DRIVE_PATH = config['local']['GOOGLE_DRIVE_PATH']
TEMP_SAVE_PATH = os.getcwd() + "/saves"

def main():
    if not os.path.exists(os.getcwd() + "/saves"):
        print('trying to create folder')
        os.mkdir(os.getcwd() + "/saves/")
        os.mkdir(os.getcwd() + "/saves/diablo")
        os.mkdir(os.getcwd() + "/saves/PSP/")
        os.mkdir(os.getcwd() + "/saves/gba/")
        os.mkdir(os.getcwd() + "/saves/psx/")
    global RSYNC_DIABLO_PATH,RSYNC_PSX_PATH,RSYNC_GBA_PATH, MAC_DIABLO_PATH, GOOGLE_DRIVE_SAVE_DIR
    global TEMP_SAVE_PATH
    os.system('clear')
    print("EmulationStation/RetroArch/RetroPie Save File Sync has started.\n")
    print("All Systems Cloud Save v1.0.0")
    print("By Ray Hernandez")
    print("    WARNING: Edit config.ini before running this   ")
    print("Backup save files from which location?")
    print("------------------------------------------")
    print("")
    print("Press ENTER if you are ready to backup to the cloud.")
    raw_input = input()
    os.system('clear')

def send_rsync(source, destination):
    global SSH_USER, SSH_PASSWORD, SSH_IP_ADDRESS
    os.system('sshpass -p "%s" rsync -a %s@%s:%s "%s"' % (
        SSH_PASSWORD, SSH_USER, SSH_IP_ADDRESS, source, destination
    ))

def send_rsync2(source, destination, extension):
    global SSH_USER, SSH_PASSWORD, SSH_IP_ADDRESS
    os.system('sshpass -p "%s" rsync -a --include "*.%s" --exclude "*" %s@%s:%s "%s"' % (
        SSH_PASSWORD, extension, SSH_USER, SSH_IP_ADDRESS, source, destination
    ))

def send_rsync3(source, destination, extension):
    global SSH_USER, SSH_PASSWORD, SSH_IP_ADDRESS
    os.system('sshpass -p "%s" rsync -a --include "*/" --include "*.%s" --exclude "*" %s@%s:%s "%s"' % (
        SSH_PASSWORD, extension, SSH_USER, SSH_IP_ADDRESS, source, destination
    ))
    
def sync_saves():

    # Check to see if any previous diablo saves exist.
    mac_diablo_dir = TEMP_SAVE_PATH + '/diablo'

    # TODO : Compare sizes and give warnings if smaller than whats getting replaced.
    # User has chosen to get all of the save games from the device, and udpate the cloud.
    if os.path.exists(mac_diablo_dir):
        print('Removing old diablo save files from: %s...' % mac_diablo_dir);
        os.system('chmod +rw %s' % mac_diablo_dir)
        shutil.rmtree(mac_diablo_dir)
        os.mkdir(mac_diablo_dir)
        
        # Copy all of diablo/devilutionX files. Also save the save files for local play.
        mac_diablo_dir = TEMP_SAVE_PATH + '/diablo'
        print("Copying Diablo save files from remote %s..." % REMOTE_DIABLO_PATH)
        send_rsync2(REMOTE_DIABLO_PATH, mac_diablo_dir, 'sv')
        # Copy updated save files to local diablo directory.
        print("Copying save files to local devilution directory...")
        os.system("cp -R %s %s" % (mac_diablo_dir + '/', DEVILUTION_SAVE_PATH))

        # Copying all PSP save files.
        print("Copying PSP save files from device...")
        send_rsync(REMOTE_PSP_PATH, TEMP_SAVE_PATH + "/PSP/")

        # Copying all GBA save files.
        print("Copying GBA save files from device...")
        send_rsync2(REMOTE_GBA_PATH, TEMP_SAVE_PATH + "/gba/", "srm")

        # Copying all GBC save files.
        print("Copying GBC save files from device...")
        send_rsync2(REMOTE_GBC_PATH, TEMP_SAVE_PATH + "/gbc/", "srm")

        # Copying all GB save files.
        print("Copying GB save files from device...")
        send_rsync2(REMOTE_GB_PATH, TEMP_SAVE_PATH + "/gb/", "srm")

        # Copying all GBA save files.
        print("Copying PSX save files from device...")
        # We use send rsync3 here incase discs/saves are in separate folders.
        send_rsync3(REMOTE_PSX_PATH, TEMP_SAVE_PATH + "/psx/", "srm")

        if LOCAL_GOOGLE_DRIVE_PATH != "":

            if os.path.exists(LOCAL_GOOGLE_DRIVE_PATH) is False:
                os.system('mkdir %s' % LOCAL_GOOGLE_DRIVE_PATH)

            print("Copying all save files to Google Drive...")
            os.system("rsync -a %s %s" % (mac_diablo_dir + '/', LOCAL_GOOGLE_DRIVE_PATH + '/diablo'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/gba/', LOCAL_GOOGLE_DRIVE_PATH + '/gba'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/gbc/', LOCAL_GOOGLE_DRIVE_PATH + '/gbc'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/gb/', LOCAL_GOOGLE_DRIVE_PATH + '/gb'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/psp/', LOCAL_GOOGLE_DRIVE_PATH + '/psp'))
            os.system("rsync -a %s %s" % (TEMP_SAVE_PATH + '/psx/', LOCAL_GOOGLE_DRIVE_PATH + '/psx'))


if __name__ == "__main__":
    main()
