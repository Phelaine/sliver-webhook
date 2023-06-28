__author__ = 'mediocrity'

import os
import json
import requests
import subprocess

# your dingtalk url, verify keyword is sliver
webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxx"

def dingtalk(markdown):
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "sliver有新用户上线",
            "text": markdown
        }
    }
    r = requests.post(url=webhook_url, headers=headers, data=json.dumps(data))
    return r.json()


def is_tail_exists():
    try:
        subprocess.check_output(["tail", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False

def is_sliver_server():

    filename = ".sliver/logs/audit.json"
    home_dir = os.path.expanduser("~")
    file_path = os.path.join(home_dir, filename)

    if os.path.exists(file_path):
        return True,file_path
    else:
        return False,file_path


if __name__ == '__main__':
    is_sliver_server, logpath = is_sliver_server()
    if is_tail_exists() and is_sliver_server:
        
        command = 'tail -n0 -f ' + logpath
        popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        try:
            print("[+] it works")
            while True:
                byte_line = popen.stdout.readline().strip()
                line = bytes.decode(byte_line)
                if "Session" in line and "Register" in line:
                    data = json.loads(line)
                    register_time = data['time']
                    msg = json.loads(data['msg'])
                    hostname = msg['Session']['Hostname']
                    ip = msg['Session']['RemoteAddress']
                    username = msg['Session']['Username']
                    arch = msg['Session']['Arch']
                    os = msg['Session']['OS']
                    version = msg['Session']['Version']
                    print("[+]",register_time,hostname,ip,username,os,arch,version)
                    markdown = "- 机器名称：{}\n\n- 机器IP：{}\n\n- 上线时间：{}\n\n- 用户名：{}\n\n- 机器架构：{}/{}\n\n- 系统版本：{}\n\n".format(hostname,ip,register_time,username,os,arch,version)
                    dingtalk(markdown)
        except:pass
    else:
        print("[!] there is not sliver server or no tail command")