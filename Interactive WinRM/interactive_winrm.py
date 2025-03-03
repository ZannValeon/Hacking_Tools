#!/usr/bin/env python3

import winrm
import getpass

#Get connection details from user
ip_addr = input("Enter the target IP address ")
username = input("Enter username ")
password = getpass.getpass("Enter password ")

#Create a session for WinRM with SSL
session = winrm.Sesssion(
    f'https://{ip_addr}:5986/wsman', #Dynamic hostname or IP addr
    auth=(username, password),
    transport='ntlm', #Using NTLM autn
    server_cert_validation='ignore' #Skip certificate validation
)

def interactive_shell():
    print("WinRM Interactive Shell")
    print("Type 'exit' to quit the shell.")

    while True:
        command = input("winrm> ")

        if command.lower() == 'exit':
            print("Exiting the shell.")
            break

        #Run the command remotely
        result = session.run_cmd(command)

        #Print the result
        if result.std_out:
            print(result.std_out.decode())
        if result.std_err:
            print("Error ", result.std_err.decode())

#Run the interactive shell
interactive_shell()