import functions


if __name__ == "__main__":

    # Checking for admin privileges
    functions.is_admin()


    # Getting running interfaces
    interfaces = functions.get_interfaces()
    print('\n---- INTERFACES ----')
    for i in interfaces:
        print(f'{i.name}: {i.mac_address}')
    interface_name = input('\nType interface name: ')
    
    # Retriving interface object
    for i in interfaces:
        if i.name == interface_name:
            interface = i
    if not interface:
        raise Exception('Invalid interface name')
    

    # Disabling the interface
    print(f"Disabling interface {interface.name}...")
    result = interface.disable_interface()
    print(f'Interface {interface.name} disabled.')

    new_mac = input("Write new MAC address (Leave blank for a random one): ")

    # Changing MAC address
    print(f'Changing MAC address...')
    new_mac = interface.change_mac_address(new_mac)

    # Enabling interface
    print(f"Enabling interface {interface.name}...")
    result = interface.enable_interface()
    print(f'Interface {interface.name} enabled.')

    # Cheking if the address changed correctly
    # Updating interface mac
    interface.mac_address, _ = interface._getmac()
    if functions.format_mac(interface.mac_address) == new_mac:
        print("MAC address changed successfully.")
    else:
        print("Something went wrong.")
    

    input("Press any key to close window.")