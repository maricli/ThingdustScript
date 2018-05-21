import paramiko, time, os, subprocess

import paramiko

location = "123N00192S"
city = "lucerne"
country = "swiss"
floor = "2og"
room = "310"
simtype = None
simcmd = None
ttnKey = "ttn-account-v2.V9b-sSRhL3U5BKD0T6FDOZPhWp_OQDHVeUegg3nWBJ-BzWhd2MM1pNR3IKbSdKqW16-JNLanlqr2zFTDv-vuPg"
ttnEmail = "admin@thingdust.com"
ttnID =  "sandronc63samg"
simtype = "doesnt matter its manually"
BEG_GCOLOR = "\x1b[6;30;41m"
END_GCOLOR = "\x1b[0m"
BEG_ICOLOR = "\x1b[6;30;42m"
END_ICOLOR = "\x1b[0m"
BEG_ACOLOR = "\x1b[6;30;43m"
END_ACOLOR = "\x1b[0m"
asset_reverse_port = None



# ----------------------------------------------------------------------
def setGlobalVariable():
    global location
    global city
    global country
    global floor
    global room
    global simtype
    global ttnKey
    global ttnEmail
    global ttnID
    global simtype
    global simcmd

    location = raw_input(BEG_ACOLOR + "Please enter the location of the gateway and press Enter: " + END_ACOLOR)
    print("")
    city = raw_input(BEG_ACOLOR + "Please enter the city of the gateway and press Enter: " + END_ACOLOR)
    print("")
    country = raw_input( BEG_ACOLOR + "Please enter the country of the gateway and press Enter: " + END_ACOLOR)
    print("")
    floor = raw_input(BEG_ACOLOR + "Please enter the floor of the gateway and press Enter: " + END_ACOLOR)
    print("")
    room = raw_input(BEG_ACOLOR + "Please enter the room of the gateway and press Enter: " + END_ACOLOR)
    print("")
    ttnKey = raw_input(BEG_ACOLOR + "Please enter the ttnkey of the gateway and press Enter: " + END_ACOLOR)
    print("")
    ttnEmail = raw_input(BEG_ACOLOR + "Please enter the ttnEmail of the gateway and press Enter: " + END_ACOLOR)
    print("")
    ttnID = raw_input(BEG_ACOLOR + "Please enter the ttnID of the gateway and press Enter: " + END_ACOLOR)
    print("")

    while True:
        simtypeLocal = raw_input(BEG_GCOLOR + "Please enter for simcard-type infisim or emnify: " + END_GCOLOR)
        if simtypeLocal == "emnify":
            simcmd = "mlinux-set-apn em"
            simtype = simtypeLocal
            break
        if simtypeLocal == "infisim":
            simcmd = "mlinux-set-apn 0n02.tmgs"
            simtype = simtypeLocal
            break
        else:
            print("You enterred a wrong simtype - Please try again")
            print("")



# ----------------------------------------------------------------------
def printOutGlobal():
    print(BEG_GCOLOR + "you setted location to: " + location + END_GCOLOR)
    print(BEG_GCOLOR + "you setted city to: " + city + END_GCOLOR)
    print(BEG_GCOLOR + "you setted country to: " + country + END_GCOLOR)
    print(BEG_GCOLOR + "you setted floor to: " + floor + END_GCOLOR)
    print(BEG_GCOLOR + "you setted room to: " + room + END_GCOLOR)
    print(BEG_ICOLOR + "you setted simtype to: " + simtype + END_ICOLOR)
    print(BEG_ACOLOR + "you setted ttnkey to: " + ttnKey + END_ACOLOR)
    print(BEG_ACOLOR + "you setted ttnEmail to: " + ttnEmail + END_ACOLOR)
    print(BEG_ACOLOR + "you setted ttnID to: " + ttnID + END_ACOLOR)
    print(BEG_ACOLOR + "the assetport for this gateway is: " + asset_reverse_port + END_ACOLOR)

#----------------------------------------------------------------------
def getportfromassetserver():
    global asset_reverse_port
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("51.144.74.79", username="thingdust", key_filename="remotekey")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python /home/asset_thingdust/assetserver/getgatewayport.py")
    asset_reverse_port = ssh_stdout.read()[:-1]
    ssh.close()


# ----------------------------------------------------------------------
def sendcomandtogateway(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.2.1", username="root", password="root", port=22)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    print ssh_stdout.read()
    print("command: " + command + " successfully executed")
    ssh.close()


# ----------------------------------------------------------------------
def sendcommandtoassetserver(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("51.144.74.79", username="thingdust", key_filename="remotekey")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    print ssh_stdout.read()
    print("command: " + command + " successfully executed")
    ssh.close()


# ----------------------------------------------------------------------
def sendcomandtolocal(command):
    os.system(command)
    print("command: " + command + " Successfully executed")


# ----------------------------------------------------------------------
def tryToConnectFactory():
    time.sleep(80)
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    retry_interval = 1
    timeout = 20
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        time.sleep(retry_interval)
        try:
            ssh.connect("192.168.2.1", username="root", password="root", port=22)
        except paramiko.ssh_exception.SSHException as e:
            # socket is open, but not SSH service responded
            if e.message == 'Error reading SSH protocol banner':
                print(e)
                continue
            print('SSH transport is available!')
            break
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print('SSH transport is not ready...')
            continue


# ----------------------------------------------------------------------
def tryToConnect():
    time.sleep(70)
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    retry_interval = 1
    timeout = 20
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        time.sleep(retry_interval)
        try:
            ssh.connect("192.168.2.1", username="root", password="root", port=22)
        except paramiko.ssh_exception.SSHException as e:
            # socket is open, but not SSH service responded
            if e.message == 'Error reading SSH protocol banner':
                print(e)
                continue
                print('SSH transport is available!')
                break
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print('SSH transport is not ready...')
            continue

def insertintodatabase():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("51.144.74.79", username="thingdust", key_filename="remotekey")
    command = "python /home/asset_thingdust/assetserver/insertnewgatewaydata.py " + location + " " + city + " " + country + " " + floor + " " + room + " " + asset_reverse_port
    print(command)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    print("added whole data to datebase")
    ssh.close()


def createreconnectfile():
    print("create temp reconnect file")
    os.system("cp /home/pi/reconnect.sh /home/pi/reconnect.sh.temp")
    print("add line with port to reconnect script")
    line = "ssh -i /home/asset_thingdust/.ssh/sshtunel_key -Nf -R " + asset_reverse_port + ":localhost:22 asset_thingdust@51.144.74.79 -o 'StrictHostKeyChecking no';"
    file = open("/home/pi/reconnect.sh.temp", "a")
    file.write(line)
    file.close()
    print("copy reconnect file to gateway")
    os.system("sshpass -p 'root' scp -o StrictHostKeyChecking=no /home/pi/reconnect.sh.temp root@192.168.2.1:/home/asset_thingdust/reconnect.sh")


# ----------------------------------------------------------------------
def installTTN(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.2.1", username="root", password="root", port=22)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        "cd /tmp && wget https://github.com/kersing/multitech-installer/raw/master/installer.sh && chmod +x installer.sh && ./installer.sh -f")

    output = ""

    while True:
        char = ssh_stdout.read(1)
        output += char
        if char == "\n":
            print output
            if "update confi" in output:
                ssh_stdin.write("2" + "\n")
                ssh_stdin.flush()
            if "Please enter gateway informtion" in output:
                ssh_stdin.write(ttnID + "\n")
                ssh_stdin.flush()
                ssh_stdin.write(ttnKey + "\n")
                ssh_stdin.flush()
            if "correct?" in output:
                ssh_stdin.write("1" + "\n")
                ssh_stdin.flush()
            if "SETUP LORA GATEWAY CONFIGURATION" in output:
                ssh_stdin.write("admin@thingdust.com" + "\n")
                ssh_stdin.flush()
            if "It might" in output:
                break
            output = ""
    ssh.close()


# ----------------------------------------------------------------------

if __name__ == "__main__":

    getportfromassetserver()
    setGlobalVariable()
    printOutGlobal()
    print(simcmd)
    # 1. Remove Keys
    sendcomandtolocal("rm -f  /home/pi/.ssh/known_hosts")

    # 2. Factory Reset of Gateway
    sendcomandtogateway("rm -rf /var/config/* && touch /var/config/force_defaults && reboot")

    # 3. Try to connect after factory reset of Gateway
    tryToConnectFactory()

    # 4. Create directory on Gateway
    sendcomandtogateway("mkdir -p /var/volatile/flash-upgrade")

    # 5. Upload rootfs.jffs2 and uImage.bin from Installserver to Gateway - os.system() cmd choosed cause there were connection problems with paramiko
    sendcomandtolocal("sshpass -p 'root' scp -o StrictHostKeyChecking=no /home/pi/rootfs.jffs2 root@192.168.2.1:/var/volatile/flash-upgrade")
    sendcomandtolocal("sshpass -p 'root' scp -o StrictHostKeyChecking=no /home/pi/uImage.bin root@192.168.2.1:/var/volatile/flash-upgrade")

    # 6. Do touch of dir flash-upgrade
    sendcomandtogateway("touch /var/volatile/do_flash_upgrade")

    # 7. Do reboot of gateway
    sendcomandtolocal("sshpass -p 'root' ssh root@192.168.2.1 reboot")
    sendcomandtogateway("reboot")

    # 8. Try to connect during reboot --> Be careful, there is a method ti reconnect after reboot and after factory reset
    tryToConnect()

    # 9. Set up the cell connectivity according users input at the beginning (infisim or emnisim)
    sendcomandtogateway(simcmd)

    # 10. Update the PPP file with correct Params
    sendcomandtolocal("sshpass -p 'root' scp /home/pi/thingdust/etc1/default1/ppp root@192.168.2.1:/etc/default")

    # 12. Upodate PPP_ON_BOOT File
    sendcomandtolocal("sshpass -p 'root' scp /home/pi/thingdust/etc1/ppp/ppp_on_boot root@192.168.2.1:/etc/ppp")

    # 13. Set the ppp_start command for automatic start on boot
    sendcomandtogateway("/etc/init.d/ppp start")
    print("going to sleep manually for 45 sec")
    time.sleep(45)

    # 14. Set init file to autobood
    sendcomandtogateway("update-rc.d ppp defaults")

    # 15. Update and install node.js
    sendcomandtogateway("/etc/init.d/ppp start")
    print("going again to sleep for 45 sec")
    time.sleep(45)
    sendcomandtogateway("update-rc.d ppp defaults")
    sendcomandtogateway("opkg update && opkg install node")

    # 16. Set up time zone
    sendcomandtogateway("ln -fs /usr/share/zoneinfo/Europe/Zurich /etc/localtime")

    # 17. Update the hardware clock of the gateway
    sendcomandtogateway("hwclock -u -w")

    # 18. Install monit
    sendcomandtogateway("opkg update && opkg install monit")

    # 19. Update monit file to autostart on boot
    sendcomandtolocal("sshpass -p 'root' scp /home/pi/thingdust/etc1/default1/monit root@192.168.2.1:/etc/default")

    # 20. Configure Status monitor and echo
    sendcomandtogateway("echo 192.168.2.1  $(uname -n) >>/etc/hosts")

    # 21. Create dir for monit
    sendcomandtogateway("mkdir -p /etc/monit.d")

    # 22. Update the monit file with params
    sendcomandtolocal("sshpass -p 'root' scp /home/pi/thingdust/etc1/monit.d/ppp root@192.168.2.1:/etc/monit.d")

    # 23. Test monit
    sendcomandtogateway("monit -t")

    # 24. Test if ipdown
    sendcomandtogateway("ifdown eth0 && ifup eth0")

    # 25. Install TTN for the gateway
    installTTN("cd /tmp && wget https://github.com/kersing/multitech-installer/raw/master/installer.sh && chmod +x installer.sh && ./installer.sh -f")

    # 26. Install TTN for the gateway
    #getportfromassetserver()

    # 27. Install TTN for the gateway
    #printOutGlobal()

    # 28. Create user on gateway
    sendcomandtogateway("adduser asset_thingdust -D && mkdir /home/asset_thingdust/.ssh && chown -R asset_thingdust:asset_thingdust /home/asset_thingdust/.ssh && chmod 0700 /home/asset_thingdust/.ssh")

    # 29. Upload key_pub to gateway
    sendcomandtolocal("sshpass -p 'root' scp -o StrictHostKeyChecking=no /home/pi/asset_key.pub root@192.168.2.1:/home/asset_thingdust/.ssh")

    # 30. Generate key with asset_reverse_port
    sendcomandtolocal("echo -e 'y\n'|ssh-keygen -t rsa -b 4096 -C " + asset_reverse_port + " -f /home/pi/sshtunel_key -N ''")

    # 31. Upload sshtunnel_key to gateway
    sendcomandtolocal("sshpass -p 'root' scp -o StrictHostKeyChecking=no /home/pi/sshtunel_key root@192.168.2.1:/home/asset_thingdust/.ssh")

    # 32. Give permissions to dir
    sendcomandtogateway("chmod 0600 /home/asset_thingdust/.ssh/sshtunel_key")

    # 33. Copy authorized_keys to tmp folder
    sendcommandtoassetserver("sudo cp /home/asset_thingdust/.ssh/authorized_keys /tmp/authorized_keys && sudo chmod 0777 /tmp/authorized_keys")

    # 34. Upload from assetserver the authorized_key file to dir
    sendcomandtolocal("scp -i remotekey thingdust@51.144.74.79:/tmp/authorized_keys /home/pi")

    # 35. Upload from assetserver the authorized_key file to dir
    sendcomandtolocal("scp -i remotekey thingdust@51.144.74.79:/tmp/authorized_keys /home/pi/Script")

    # 36. Insert line inte key pub
    sendcomandtolocal("cat /home/pi/sshtunel_key.pub >> /home/pi/authorized_keys")

    # 37. Send authorized_keys from gateway to asset
    sendcomandtolocal("scp -i remotekey /home/pi/authorized_keys thingdust@51.144.74.79:/tmp")

    # 38. Give permissions on asset server, copy auth_key file to correct dir
    sendcommandtoassetserver("sudo chmod 0700 /tmp/authorized_keys && sudo cp /tmp/authorized_keys /home/asset_thingdust/.ssh/authorized_keys")

    # 39. Create the Reconnect File
    createreconnectfile()

    # 40. Insert the global vars into the mongo db
    insertintodatabase()

