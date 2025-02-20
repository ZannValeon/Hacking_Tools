import subprocess

interface = input("What interface? > ")
new_mac = input("What MAC Address? > ")

print("[+] Changing MAC address for " + interface + " to " + new_mac)

# Added more security by making sure user input is sanitized
subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw ether " + new_mac])
subprocess.call(["ifconfig", interface, "up"])