import subprocess
import optparse

# Added subprocess.call and print statement to a function named change_mac
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw ether " + new_mac])
    subprocess.call(["ifconfig", interface, "up"])

parser = optparse.OptionParser()

parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

(options, arguements) = parser.parse_args()


change_mac(options.interface, options.new_mac)


