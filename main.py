import paramiko
import time

# Set up SSH connection parameters
router_ip = "169.254.1.5" # replace with your Mikrotik router IP
username = "admin" # replace with your router login credentials
password = "admin"

# Connect to router using SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

mac_address = "BC:E6:7C:72:3B:DA"

try:
    ssh_client.connect(router_ip, username=username, password=password, timeout=10)
    print("Connected to router successfully")

    # Run command to test SSH connection
    stdin, stdout, stderr = ssh_client.exec_command("system identity print")
    output = stdout.read().decode()
    print(output)

    # Run command to log in to device via mac-telnet
    print("Establishing mac-telnet connection...")
    stdin, stdout, stderr = ssh_client.exec_command(f"tool mac-telnet bc:e6:7c:72:3b:da", timeout=10)
    time.sleep(1)
    stdin.write(f"{username}\n")
    time.sleep(1)
    stdin.write(f"{password}\n")
    stdin.flush()
    output = stdout.read().decode()
    print(f"stdout: {output}")
    error = stderr.read().decode()
    print(f"stderr: {error}")
    if error:
        raise Exception(error)

except paramiko.AuthenticationException as e:
    print(f"Error: Authentication failed - {str(e)}")
except paramiko.SSHException as e:
    print(f"Error: Unable to establish SSH connection - {str(e)}")
except paramiko.SFTPError as e:
    print(f"Error: SFTP error - {str(e)}")
except Exception as e:
    print(f"Error connecting to router: {str(e)}")

finally:
    # Close SSH connection
    ssh_client.close()
