import argparse
import subprocess
import re
import random
import string

"""
    Do not modify these variables or functions. They will not need to be modified in order to fix the script.
"""

# the registry path of network interfaces
network_interface_reg_path = r"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}"
# the transport name regular expression, looks like {AF1B45DB-B5D4-46D0-B4EA-3E18FA49BF5F}
transport_name_regex = re.compile("{.+}")
# the MAC address regular expression
mac_address_regex = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")


def get_random_mac_address():
    """Generate and return a MAC address in the format of Linux"""
    # get the hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    # 2nd character must be 0, 2, 4, 6, 8, A, C, or E
    mac = ""
    for i in range(6):
        for _ in range(2):
            if i == 0:
                mac += random.choice("02468ACE")
            else:
                mac += random.choice(uppercased_hexdigits)
        mac += ":"
    return mac.strip(":")

def get_random_mac_address_win():
    """Generate and return a MAC address in the format of WINDOWS"""
    # get the hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    # 2nd character must be 2, 4, A, or E
    return random.choice(uppercased_hexdigits) + random.choice("24AE") + "".join(random.sample(uppercased_hexdigits, k=10))
    
def get_connected_adapters_mac_address_win():
    # make a list to collect connected adapter's MAC addresses along with the transport name
    connected_adapters_mac = []
    # use the getmac command to extract 
    for potential_mac in subprocess.check_output("getmac").decode().splitlines():
        # parse the MAC address from the line
        mac_address = mac_address_regex.search(potential_mac)
        # parse the transport name from the line
        transport_name = transport_name_regex.search(potential_mac)
        if mac_address and transport_name:
            # if a MAC and transport name are found, add them to our list
            connected_adapters_mac.append((mac_address.group(), transport_name.group()))
    return connected_adapters_mac

def get_user_adapter_choice(connected_adapters_mac):
    # print the available adapters
    for i, option in enumerate(connected_adapters_mac):
        print(f"#{i}: {option[0]}, {option[1]}")
    if len(connected_adapters_mac) <= 1:
        # when there is only one adapter, choose it immediately
        return connected_adapters_mac[0]
    # prompt the user to choose a network adapter index
    try:
        choice = int(input("Please choose the interface you want to change the MAC address:"))
        # return the target chosen adapter's MAC and transport name that we'll use later to search for our adapter
        # using the reg QUERY command
        return connected_adapters_mac[choice]
    except:
        # if -for whatever reason- an error is raised, just quit the script
        print("Not a valid choice, quitting...")
        exit()

def clean_mac(mac):
    """Simple function to clean non hexadecimal characters from a MAC address
    mostly used to remove '-' and ':' from MAC addresses and also uppercase it"""
    return "".join(c for c in mac if c in string.hexdigits).upper()  

def change_mac_address_win(adapter_transport_name, new_mac_address):
    # use reg QUERY command to get available adapters from the registry
    output = subprocess.check_output("reg QUERY " + network_interface_reg_path.replace("\\\\", "\\")).decode()

    for interface in re.findall(rf"{network_interface_reg_path}\\\d+", output):
        # get the adapter index
        adapter_index = int(interface.split("\\")[-1])
        interface_content = subprocess.check_output(f"reg QUERY {interface.strip()}").decode()
        if adapter_transport_name in interface_content:
            # if the transport name of the adapter is found on the output of the reg QUERY command
            # then this is the adapter we're looking for
            # change the MAC address using reg ADD command
            changing_mac_output = subprocess.check_output(f"reg add {interface} /v NetworkAddress /d {new_mac_address} /f").decode()
            # print the command output
            print(changing_mac_output)
            # break out of the loop as we're done
            break
    # return the index of the changed adapter's MAC address
    return adapter_index

def disable_adapter_win(adapter_index):
    return subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call disable").decode()

def enable_adapter_win(adapter_index):
    return subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call enable").decode()

def get_current_mac_address(iface):
    # use the ifconfig command to get the interface details, including the MAC address
    output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()
    return re.search("ether (.+) ", output).group().split()[1].strip()

def change_mac_address(iface, new_mac_address):
    # disable the network interface
    subprocess.check_output(f"sudo /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -z", shell=True)

    subprocess.check_output(f"sudo ifconfig {iface} down", shell=True)
    # change the MAC
    subprocess.check_output(f"sudo ifconfig {iface} lladdr {new_mac_address}", shell=True)
    # enable the network interface again
    subprocess.check_output(f"sudo ifconfig {iface} up", shell=True)


# Modifications go within the main section.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Mac Changer on Linux")

    args = parser.parse_args()
    iface = args.interface
    if args.os == 'windows':
        if args.random:
            # if random parameter is set, generate a random MAC
            new_mac_address = get_random_mac_address()
        elif args.mac:
            # if mac is set, use it instead
            new_mac_address = args.mac
        # get the current MAC address
        old_mac_address = get_current_mac_address(iface)
        print("[*] Old MAC address: ", old_mac_address)
        print(new_mac_address)
        # change the MAC address
        change_mac_address(iface, new_mac_address)
        # check if it's really changed
        new_mac_address = get_current_mac_address(iface)
        print("[+] New MAC address: ", new_mac_address)
    else:
        if args.random:
            new_mac_address = get_random_mac_address_win()
        elif args.mac:
            new_mac_address = clean_mac(args.mac)

        connected_adapters_mac = get_connected_adapters_mac_address_win()
        old_mac_address, target_transport_name = get_user_adapter_choice(connected_adapters_mac)
        print("[*] Old MAC address: ", old_mac_address)
        adapter_index = change_mac_address(target_transport_name, new_mac_address)
        print("[+] Changed to: ", new_mac_address)
        disable_adapter_win(adapter_index)
        print("[+] Adapter is disabled")
        enable_adapter_win(adapter_index)
        print("[+] Adapter is enabled again")