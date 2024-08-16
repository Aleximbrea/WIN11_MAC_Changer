import subprocess
import re
import ctypes
import sys
import winreg
import random

class Interface:
    def __init__(self, name, admin_state, state):
         self.name = name
         self.admin_state = admin_state
         self.state = state
         self.mac_address, self.driver_name = self._getmac()
         self.driver_id = self._get_driver_id()

    def disable_interface(self):
        result = subprocess.run(args=["netsh", "interface", "set", "interface", self.name, "admin=disable"], check=True)
        return result

    def enable_interface(self):
        result = subprocess.run(args=["netsh", "interface", "set", "interface", self.name, "admin=enable"], check=True)
        return result
    
    def _getmac(self):
        result = subprocess.run(args=['getmac', '/v', '/FO', 'csv'], text=True, capture_output=True)
        lines = result.stdout.splitlines()

        for line in lines:
            line = line.split(',')

            if line[0].replace('"', '') == self.name:
                # Returning the mac address and the driver name
                mac = line[2].replace('"', '')
                driver = line[1].replace('"', '')
                return mac, driver
            
    def _get_driver_id(self):
        cmd = f"wmic nic where \"NetConnectionID='{self.name}'\" get DeviceID"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        id = result.stdout.split('\n')[2].replace(' ', '')
        if int(id) < 10:
            id = f'000{id}'
        else:
            id = f'00{id}'
        return id

    def change_mac_address(self, new_mac_address=None):
        if new_mac_address:
            new_mac_address = new_mac_address.replace('-', '').replace(':', '')
            if not len(new_mac_address) == 12 or not re.fullmatch(r'[0-9A-Fa-f]{12}', new_mac_address):
                raise Exception('Invalid mac address')
        else:
            # If no mac address is set a random one is created
            new_mac_address = generate_mac_address()
        registry_path = "SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\\" + self.driver_id

        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "NetworkAddress", 0, winreg.REG_SZ, new_mac_address)
        self.mac_address = new_mac_address

def is_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else: 
        ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()


def get_interfaces():

    interfaces = []

    result = subprocess.run(args=["netsh", "interface", "show", "interface"], capture_output=True, text=True)
    # Splitting the lines into arrays and removing the first 3 rows
    lines = result.stdout.splitlines()[3:]

    for line in lines:

        # Regex to separate attributes
        regex = r'^(\S+)\s+(\S+)\s+(\S+)\s+(.*)$'
        pattern = re.compile(regex)

        # Pattern research
        match = pattern.search(line)
        if match:
            # Appending Interface object to the list of interfaces
            interfaces.append(Interface(name=match.group(4), admin_state=match.group(1), state=match.group(2)))
    return interfaces


def generate_mac_address():

    second_char = random.choice(['2', '6', 'A', 'E'])
    mac_address = f"{random.choice('0123456789ABCDEF')}{second_char}{''.join(random.choices('0123456789ABCDEF', k=10))}"
    return mac_address