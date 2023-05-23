import os
import sys
import yaml
import netmiko
import logging
import datetime

USER = "insert_username"
PASSWORD = "insert_password"


def logs_configuration():
    # Get the absolut path to the logs folder :
    log_directory = os.path.abspath("logs")
    # If logs folder does not exist, create it :
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    # Get the absolut path to the log file of the day :
    log_file_path = os.path.join(log_directory,
                                 datetime.date.today()
                                 .strftime("%Y-%m-%d") + "_SwitchesBackups.log")
    # Logs configuration :
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename=log_file_path)


def get_csr_devices(user, password):
    try:
        # Read the YAML config file :
        with open("csr.yaml") as file:
            content = file.read()
        # Replace constants with username and password :
        content = content.replace("USER_CONSTANT", user).replace("PASSWORD_CONSTANT", password)
        # Load CSR from the YAML config file :
        config = yaml.safe_load(content)
        # Return all CSR devices :
        return config["devices"]
    except FileNotFoundError:
        logging.error("CSR devices file not found.")
        sys.exit()
    except Exception as e:
        logging.error(f"A problem has occured : {e}")
        sys.exit()


def launch_backups(devices):
    print("Script starting...")
    # Loop through the CSR devices and perform backup :
    for device in devices:
        create_backup(device["ip"], device["username"], device["password"])
    print("Script ending...")


def create_backup(ip, user, password):
    try:
        # Create the CSR object using the dictionnary :
        csr = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': user,
            'password': password,
        }
        # Establish the SSH connection :
        connection = netmiko.ConnectHandler(**csr)
        # Discover the hostname from the prompt :
        hostname = connection.send_command("sh run | i hostname")
        hostname, device = hostname.split(" ")
        print(f"Backing up configuration for {device}")
        # Build the filename for the backup :
        filename = create_filename(device)
        # Send differents commands to retrieve configuration :
        show_run = connection.send_command("sh run")
        show_vlan = connection.send_command("sh vlan")
        show_version = connection.send_command("sh ver")
        # Write the configuration to the backup file :
        with open(filename, "a") as file:
            file.write("\nRUNNING CONFIGURATION (sh run) :\n" + show_run)
            file.write("\nVLAN CONFIGURATION (sh vlan) :\n" + show_vlan)
            file.write("\nCURRENT VERSION (sh ver) :\n" + show_version)
        # Close the connection :
        connection.disconnect()
    except Exception as e:
        logging.error(f"A problem has occured : {e}")


def create_filename(device):
    # Get the absolut path to the current file :
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Alter the path in order to include the backups folder :
    backup_directory = os.path.join(current_directory, "backups")
    # If backups folder does not exist, create it :
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
    # Add a new directory with the current date :
    today = datetime.date.today().strftime("%Y-%m-%d")
    today_backup_directory = os.path.join(backup_directory, today)
    # If today_backup_directory does not exist, create it :
    if not os.path.exists(today_backup_directory):
        os.makedirs(today_backup_directory)
    # Return the filename for a specific switch for a specific date :
    return os.path.join(today_backup_directory, f"{today}_{device}.txt")


def main():
    logs_configuration()
    devices = get_csr_devices(user=USER, password=PASSWORD)
    launch_backups(devices)


if __name__ == "__main__":
    main()
