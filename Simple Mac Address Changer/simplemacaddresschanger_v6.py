import subprocess
import optparse

# Added arguements using optparse for new mac address
parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

(options, arguements) = parser.parse_args()

# Changed input to options. for cleaner code
interface = options.interface
new_mac = options.new_mac

print("[+] Changing MAC address for " + interface + " to " + new_mac)

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw ether " + new_mac])
subprocess.call(["ifconfig", interface, "up"])