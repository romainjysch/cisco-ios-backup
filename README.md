# Cisco IOS Backup

## Context

As a network engineer who is learning Python programming, I have developed a script that performs backups of Cisco IOS switches. The script utilizes the Netmiko library to establish SSH connections with the switches and retrieve the configuration using three different commands: 'show run', 'show vlan', and 'show ver'. The collected  information is then saved in separate text files for each switch.

### Backup Process

The script performs the following backup process:

1. Establishes an SSH connection with each switch specified in the YAML configuration
2. Retrieves the switch hostname from the prompt
3. Creates a backup directory for the current date
4. Executes the 'show run', 'show vlan', and 'show ver' commands to collect the switch configuration
5. Writes the configuration to a text file named with the current date and switch name

Please note that each backup file will contain the following sections:

- **RUNNING CONFIGURATION (sh run):** contains the output of the 'show run' command
- **VLAN CONFIGURATION (sh vlan):** contains the output of the 'show vlan' command
- **CURRENT VERSION (sh ver):** contains the output of the 'show ver' command

## Installation

To run the script, please install the following dependencies unsing pip :

```
pip install netmiko
pip install pyyaml
```

## Usage

Before running the script, make sure to replace the following placeholders :

### YAML Configuration (car.yaml)

- 'insert_switch_name' : replace with the name of the switch
- 'insert_ip' : replace with the IP address or FQDN

### Python Script (main.py)

- 'insert_username' : replace with the username of an account with privileged EXEC mode access
- 'insert_password' : replace with the username's password

## Conclucion

Please feel free to use and modify this script according to your specific needs. As I'm a beginner in Python, if you encounter any issues or have suggestions for improvements, please don't hesitate to reach out.
