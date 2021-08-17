import paramiko, os, requests, json, datetime, socket, pandas as pd

### Timestamp with time ###
dtimestamp = datetime.datetime.now().strftime("%b-%d-%Y_%H:%M:%S")

### Timestamp date only ###
timestamp = datetime.datetime.now().strftime("%m-%d-%Y_%H:%M:%S").split("_")[0]

### Main directory for files. Currently setup for linux machines ###
main_dir = "/home/scripts/Backups/"

### Netbox information: Replace token with your Netbox API token and replace YOURNETBOXURL.COM with the url to your instance of Netbox###
token = 'Token tokentokentokentokentokentokentokentoken'
nbox_url = 'https://YOURNETBOXURL.COM/api/'

### Mikrotik credentials: Enter your username and password for your MikroTike devices ###
username = "YOURUSERNAME"
password = "YOURPASSWORD"

### Function to create log file item ###
def log_msg(msg):
    dev_log.append({"Timestamp":dtimestamp,
                    "Address":d['primary_ip']['address'],
                    "Serial Number": srl_num,
                    "Model":model, 
                    "Firmware":fw_ver, 
                    "Device Name":d['name'],
                    "Role":d['device_role']['name'],
                    "Backup":msg})
    
### Function to get Netbox infromation ###
def get_netbox(item, token):
    headers = {'Authorization':token}
    url = f"{nbox_url}{item}"
    results = json.loads(requests.get(url=url, headers=headers).content)
    results = results['results']
    return results

### List of dictionaries for log file ###
dev_log = []

### Netbox information for all active MikroTik devices ###
devices = get_netbox("dcim/devices/?status=active&manufacturer=mikrotik", token=token)

### Loop to log into all Mikrotik devices and to get "compat" configuration ###
for d in devices:
    srl_num = 'null'
    model = 'null'
    fw_ver = 'null'
    try:                 
        host = d['primary_ip']['address'].split("/")[0]
        port = 22
        command = "export compact"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password, look_for_keys=False, timeout=2)
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()

        role_dir = f"{main_dir}{d['device_role']['name']}"
        name_dir =f"{role_dir}/{d['name']}"
        if not os.path.exists(name_dir):
            os.makedirs(name_dir)
            
        ### List of all the files in name_dir ###
        dir_list = os.listdir(name_dir)
        
        ### Checks to see how many files are in name_dir and removes first file if there are >= 30 files ###
        if len(dir_list) >= 30:
            os.remove(f"{name_dir}/{dir_list[0]}")
        
        ### Creates .rsc files for each MikroTik device ###
        with open(f"{name_dir}/{timestamp}-{d['name']}.rsc","w") as file:
            for l in lines:
                if l.find("serial number") >= 0:
                    srl_num = l.split("=")[1].strip()
                if l.find("model") >= 0:
                    model = l.split("=")[1].strip()
                if l.find("RouterOS") >= 0:
                    fw_ver = l.split(" ")[-1].strip()
                file.write(l)
        log_msg("Successful")
    except TimeoutError:
        log_msg("Timed Out")
    except socket.timeout:
        log_msg("Timed Out")
    except socket.error:
        log_msg("Socket Error")
    except TypeError:
        log_msg("Missing Data")
    except:
        log_msg("Unknown Error")

### Creates backup_log.csv for all log_msg ###
df = pd.DataFrame(dev_log)
path = f"{main_dir}backup_log.csv"
if os.path.exists(f"{main_dir}backup_log.csv"):
    df.to_csv(path,mode="a",index=False,header=False)
else:
    df.to_csv(path,index=False)
