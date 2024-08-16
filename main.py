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

    # Changing MAC address
    print(f'Changing MAC address...')
    interface.change_mac_address()
    print(f'MAC address changed to {interface.mac_address}')

    # Enabling interface
    print(f"Enabling interface {interface.name}...")
    result = interface.enable_interface()
    print(f'Interface {interface.name} enabled.')

    input("Press any key to close window")