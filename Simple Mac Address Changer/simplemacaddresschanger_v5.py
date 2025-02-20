import subprocess
import optparse

# Added arguements using optparse
parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
parser.parse_args()

interface = input("What interface? > ")
new_mac = input("What MAC Address? > ")

print("[+] Changing MAC address for " + interface + " to " + new_mac)

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw ether " + new_mac])
subprocess.call(["ifconfig", interface, "up"])