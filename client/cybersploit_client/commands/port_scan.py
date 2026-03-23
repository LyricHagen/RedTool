from ..commands import Command # Required
from ..util.config import DEFAULT_IP
import socket 
import shlex
import argparse

import socket

def scan_ip(target: str, port_range: tuple[int, int], no_services: bool) -> list[tuple[int, str]]:
    results: list[tuple[int, str]] = []

    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        

        if s.connect_ex((target, port)) == 0:
            vstring = ""

            if not no_services:
                try:
                    vstring = s.recv(1024).decode(errors="ignore").strip()
                except socket.timeout:
                    try:
                        # Fall back to HTTP only if banner grab fails
                        s.sendall(b"GET / HTTP/1.0\r\n\r\n")
                        s.settimeout(1.0)
                        response = s.recv(4096).decode(errors="ignore")
                        for line in response.split("\r\n"):
                            if line.lower().startswith("server:"):
                                vstring = line
                                break
                    except:
                        vstring = ""


            results.append((port, vstring))

        s.close()

    return results



def pretty_print_scan(results: list[tuple[int, str]]) -> None:
    format_string = "{:<6} {}"
    print(format_string.format("Port", "Version String"))


    for port, vstring in results:
        print(format_string.format(port, vstring))


class Scan(Command): 
    """
    Scan ports on a target host.
    """

    def do_command(self, lines: str):
        parser = argparse.ArgumentParser(description="Scan ports on a target host.")
        parser.add_argument("--ip", "-i", type=str, default=DEFAULT_IP, help="The target IP address to scan (default: %(default)s).")
        parser.add_argument("--start_port", "-sp", type=int, default="0", help="Start of port range (default: %(default)s).")
        parser.add_argument("--end_port", "-ep", type=int, default="500", help="End of port range (default: %(default)s).")
        parser.add_argument("--no_services", "-ns", action="store_true", help="Don't attempt to grab service banners.")

        arguments = shlex.split(lines)
        args = parser.parse_args(arguments)

        target_ip = args.ip
        open_ports = scan_ip(target_ip, (args.start_port, args.end_port), args.no_services)
        print(f"Open ports on {target_ip}: {' '.join(str(p) for p in open_ports)}")
        pretty_print_scan(open_ports)
        

command = Scan # Assign the class you created to the variable called command for the system to find the command!


