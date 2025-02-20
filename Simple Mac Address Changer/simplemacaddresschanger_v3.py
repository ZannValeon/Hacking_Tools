import subprocess

# Added user input
interface = input("What interface? > ")
new_mac = input("What MAC Address? > ")

print("[+] Changing MAC address for " + interface + " to " + new_mac)

subprocess.call("ifconfig " + interface " down", shell=True)
subprocess.call("ifconfig " + interface " hw ether " + new_mac, shell=True)
subprocess.call("ifconfig " + interface " up", shell=True)
