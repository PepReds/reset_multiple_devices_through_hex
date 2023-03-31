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
    #stdin, stdout, stderr = ssh_client.exec_command("system identity print")
    #output = stdout.read().decode()
    #print(output)

    # Run command to establish mac-telnet connection
    print("Establishing mac-telnet connection...")
    stdin, stdout, stderr = ssh_client.exec_command("tool mac-telnet bc:e6:7c:72:3b:da\n")
    time.sleep(1)
    output = stdout.read().decode()
    print(output)

    # Enter telnet username and password
    print("Entering telnet username...")
    stdin.write("admin\n")
    stdin.flush()
    time.sleep(1)

    print("Entering telnet password...")
    stdin.write("admin\n")
    stdin.flush()
    time.sleep(1)

    # Print output of telnet session
    output = stdout.read().decode()
    print(output)

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
