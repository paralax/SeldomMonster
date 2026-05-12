import ipaddress
import socket
import subprocess

from mcp.server.fastmcp import FastMCP
from typing import Dict, List, Any

mcp = FastMCP(
    name="LocalHacker",
    instructions="Uses a bunch of OSX tools to discover and hack devices on the local network.",
    dependencies=[],
)


@mcp.tool()
async def port_scan_nmap(ip_address: str, args: List[str] = ["-A"]) -> str:
    """
    Gets the ports open on an IP address using the Nmap tool, returns a bunch of information about it.

    Nmap 7.98 ( https://nmap.org )
    Usage: nmap [Scan Type(s)] [Options] {target specification}
    TARGET SPECIFICATION:
    Can pass hostnames, IP addresses, networks, etc.
    Ex: scanme.nmap.org, microsoft.com/24, 192.168.0.1; 10.0.0-255.1-254
    -iL <inputfilename>: Input from list of hosts/networks
    -iR <num hosts>: Choose random targets
    --exclude <host1[,host2][,host3],...>: Exclude hosts/networks
    --excludefile <exclude_file>: Exclude list from file
    HOST DISCOVERY:
    -sL: List Scan - simply list targets to scan
    -sn: Ping Scan - disable port scan
    -Pn: Treat all hosts as online -- skip host discovery
    -PS/PA/PU/PY[portlist]: TCP SYN, TCP ACK, UDP or SCTP discovery to given ports
    -PE/PP/PM: ICMP echo, timestamp, and netmask request discovery probes
    -PO[protocol list]: IP Protocol Ping
    -n/-R: Never do DNS resolution/Always resolve [default: sometimes]
    --dns-servers <serv1[,serv2],...>: Specify custom DNS servers
    --system-dns: Use OS's DNS resolver
    --traceroute: Trace hop path to each host
    SCAN TECHNIQUES:
    -sS/sT/sA/sW/sM: TCP SYN/Connect()/ACK/Window/Maimon scans
    -sU: UDP Scan
    -sN/sF/sX: TCP Null, FIN, and Xmas scans
    --scanflags <flags>: Customize TCP scan flags
    -sI <zombie host[:probeport]>: Idle scan
    -sY/sZ: SCTP INIT/COOKIE-ECHO scans
    -sO: IP protocol scan
    -b <FTP relay host>: FTP bounce scan
    PORT SPECIFICATION AND SCAN ORDER:
    -p <port ranges>: Only scan specified ports
        Ex: -p22; -p1-65535; -p U:53,111,137,T:21-25,80,139,8080,S:9
    --exclude-ports <port ranges>: Exclude the specified ports from scanning
    -F: Fast mode - Scan fewer ports than the default scan
    -r: Scan ports sequentially - don't randomize
    --top-ports <number>: Scan <number> most common ports
    --port-ratio <ratio>: Scan ports more common than <ratio>
    SERVICE/VERSION DETECTION:
    -sV: Probe open ports to determine service/version info
    --version-intensity <level>: Set from 0 (light) to 9 (try all probes)
    --version-light: Limit to most likely probes (intensity 2)
    --version-all: Try every single probe (intensity 9)
    --version-trace: Show detailed version scan activity (for debugging)
    SCRIPT SCAN:
    -sC: equivalent to --script=default
    --script=<Lua scripts>: <Lua scripts> is a comma separated list of
            directories, script-files or script-categories
    --script-args=<n1=v1,[n2=v2,...]>: provide arguments to scripts
    --script-args-file=filename: provide NSE script args in a file
    --script-trace: Show all data sent and received
    --script-updatedb: Update the script database.
    --script-help=<Lua scripts>: Show help about scripts.
            <Lua scripts> is a comma-separated list of script-files or
            script-categories.
    OS DETECTION:
    -O: Enable OS detection
    --osscan-limit: Limit OS detection to promising targets
    --osscan-guess: Guess OS more aggressively
    TIMING AND PERFORMANCE:
    Options which take <time> are in seconds, or append 'ms' (milliseconds),
    's' (seconds), 'm' (minutes), or 'h' (hours) to the value (e.g. 30m).
    -T<0-5>: Set timing template (higher is faster)
    --min-hostgroup/max-hostgroup <size>: Parallel host scan group sizes
    --min-parallelism/max-parallelism <numprobes>: Probe parallelization
    --min-rtt-timeout/max-rtt-timeout/initial-rtt-timeout <time>: Specifies
        probe round trip time.
    --max-retries <tries>: Caps number of port scan probe retransmissions.
    --host-timeout <time>: Give up on target after this long
    --scan-delay/--max-scan-delay <time>: Adjust delay between probes
    --min-rate <number>: Send packets no slower than <number> per second
    --max-rate <number>: Send packets no faster than <number> per second
    FIREWALL/IDS EVASION AND SPOOFING:
    -f; --mtu <val>: fragment packets (optionally w/given MTU)
    -D <decoy1,decoy2[,ME],...>: Cloak a scan with decoys
    -S <IP_Address>: Spoof source address
    -e <iface>: Use specified interface
    -g/--source-port <portnum>: Use given port number
    --proxies <url1,[url2],...>: Relay connections through HTTP/SOCKS4 proxies
    --data <hex string>: Append a custom payload to sent packets
    --data-string <string>: Append a custom ASCII string to sent packets
    --data-length <num>: Append random data to sent packets
    --ip-options <options>: Send packets with specified ip options
    --ttl <val>: Set IP time-to-live field
    --spoof-mac <mac address/prefix/vendor name>: Spoof your MAC address
    --badsum: Send packets with a bogus TCP/UDP/SCTP checksum
    OUTPUT:
    -oN/-oX/-oS/-oG <file>: Output scan in normal, XML, s|<rIpt kIddi3,
        and Grepable format, respectively, to the given filename.
    -oA <basename>: Output in the three major formats at once
    -v: Increase verbosity level (use -vv or more for greater effect)
    -d: Increase debugging level (use -dd or more for greater effect)
    --reason: Display the reason a port is in a particular state
    --open: Only show open (or possibly open) ports
    --packet-trace: Show all packets sent and received
    --iflist: Print host interfaces and routes (for debugging)
    --append-output: Append to rather than clobber specified output files
    --resume <filename>: Resume an aborted scan
    --noninteractive: Disable runtime interactions via keyboard
    --stylesheet <path/URL>: XSL stylesheet to transform XML output to HTML
    --webxml: Reference stylesheet from Nmap.Org for more portable XML
    --no-stylesheet: Prevent associating of XSL stylesheet w/XML output
    MISC:
    -6: Enable IPv6 scanning
    -A: Enable OS detection, version detection, script scanning, and traceroute
    --datadir <dirname>: Specify custom Nmap data file location
    --send-eth/--send-ip: Send using raw ethernet frames or IP packets
    --privileged: Assume that the user is fully privileged
    --unprivileged: Assume the user lacks raw socket privileges
    -V: Print version number
    -h: Print this help summary page.
    EXAMPLES:
    nmap -v -A scanme.nmap.org
    nmap -v -sn 192.168.0.0/16 10.0.0.0/8
    nmap -v -iR 10000 -Pn -p 80

    Args:
        ip_address: The IPv4 or IPv6 address to check (e.g., "8.8.8.8")
        args: The Nmap flags to use (e.g., ["-A"])

    Returns:
        Text output showing open ports and protocols
    """

    if "-A" not in args:
        args.append("-A")
    if ip_address not in args:
        args.append(ip_address)

    result = subprocess.run(
        ["/opt/homebrew/bin/nmap"] + args,
        capture_output=True,  # Redirects stdout/stderr
        text=True,  # Decodes output as a string (Python 3.5+)
    )
    return result.stdout


@mcp.tool()
async def lookup_service_mdns(
    instance_name: str, service_type: str, domain: str = "local."
) -> str:
    """
    Looks up more about the device and its services using the dns-sd tool over the mDNS protocol.

    dns-sd -L <Name> <Type> <Domain>        (Resolve (‘lookup’) a service instance)

    A full list of dns-sd service types is available at https://www.dns-sd.org/servicetypes.html

    Args:
        instance_name: The name of the service to interrogate (e.g., "doce").
        service_type: The type of the service to interrogate (e.g., "_http._tcp").
        domain: The domain to interrogate (e.g., "local.").

    Returns:
        Text output showing more about the device and its services
    """
    result = subprocess.run(
        ["/usr/bin/dns-sd", "-L", instance_name, service_type, domain],
        capture_output=True,  # Redirects stdout
        text=True,
        timeout=15,
    )
    return result.stdout


@mcp.tool()
async def discover_services_mdns() -> str:
    """
    Discovers devices on the local network using the dns-sd tool over the mDNS protocol.

    Takes about 15 seconds to run.

    dns-sd -B        <Type> <Domain>                 (Browse for service instances)
    dns-sd -Z        <Type> <Domain>           (Output results in Zone File format)

    Returns:
        Text output from the process showing

    """
    output = ""

    Bs = (
        "_smb._tcp",
        "_printer._tcp.",
        "_services._dns-sd._udp.",
        "_daap._tcp",
        "_nfs._tcp",
        "_dns-sd._udp",
        "_vnc._tcp",
        "_https._tcp",
        "_googlecast._tcp.",
        "_iscsi._tcp",
        "_middleware-ssl._tcp",
        "_ssh._tcp",
        "_apple-mdns-discovery._tcp",
        "_afpovertcp._tcp",
        "_webdav._tcp",
        "_raop._tcp",
        "_lpd._tcp",
        "_ipp._tcp",
        "_airplay._tcp",
        "_http._tcp.",
    )
    for B in Bs:
        result = subprocess.run(
            ["/usr/bin/dns-sd", "-B", B],
            capture_output=True,  # Redirects stdout/stderr
            text=True,  # Decodes output as a string (Python 3.5+),
            timeout=15,
        )
        output += result.stdout

    result = subprocess.run(
        ["/usr/bin/dns-sd", "-Z"],
        capture_output=True,  # Redirects stdout/stderr
        text=True,  # Decodes output as a string (Python 3.5+),
        timeout=15,
    )
    return output + result.stdout


@mcp.tool()
async def discover_neighbors_ssdp() -> List[str]:
    """
    Uses the SSDP protocol to discover devices and services on the local network

    Returns:
        List of responses from the network containing device information and links to more details 
    """
    msg = """M-SEARCH * HTTP/1.1
Host: 239.255.255.250:1900
Man: "ssdp:discover"
ST: ssdp:all
MX: 1


"""
    socket.setdefaulttimeout(120)
    responses = []
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
        socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(msg.encode(), ("239.255.255.250", 1900))
    while True:
        try:
            response, _ = sock.recvfrom(1500)
            if response:
                responses.append(response.decode())
        except:
            break
    sock.close()
    return responses

@mcp.tool()
async def discover_neighbors_arp() -> str:
    """
    Discovers IP addresses on the local network using the arp tool. Primes the pump by first ping sweeping any locally connected networks.

    Returns:
        Text
    """
    networks = []
    result = subprocess.run(
        [
            "/sbin/ifconfig",
            "-a",
            "|",
            "grep",
            "netmask",
            "|",
            "grep",
            "-v",
            "inet 127.",
        ],
        capture_output=True,  # Redirects stdout/stderr
        text=True,  # Decodes output as a string (Python 3.5+)
    )
    ifconfigs = result.stdout.splitlines()
    for ifconfig in ifconfigs:
        # 	inet 192.168.1.103 netmask 0xffffff00 broadcast 192.168.1.255
        _, ip_address, _, netmask, _, broadcast = ifconfig.split()
        subnet_mask = str(ipaddress.ip_address(netmask))
        network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
        networks.append(network)

    # prime the ARP pump
    for network in networks:
        subprocess.run(["/opt/homebrew/bin/nmap", "-n", "-sn", network], capture_output=False)

    result = subprocess.run(
        ["/usr/sbin/arp", "-na", "|", "grep", "-v", "incomplete"],
        capture_output=True,  # Redirects stdout/stderr
        text=True,  # Decodes output as a string (Python 3.5+)
    )
    return result.stdout


@mcp.tool()
async def list_wifi_networks() -> str:
    """
    Discovers locally visible wifi networks

    Returns:
        Text    
    """
    result = subprocess.run(
        ["/usr/sbin/system_profiler", "SPAirPortDataType"],
        capture_output=True,  # Redirects stdout/stderr
        text=True,  # Decodes output as a string (Python 3.5+)
    )
    return result.stdout

@mcp.tool()
async def list_bluetooth_devices() -> str:
    """
    Discovers locally visible Bluetooth devices

    Returns:
        Text    
    """
    result = subprocess.run(
        ["/usr/sbin/system_profiler", "SPBluetoothDataType"],
        capture_output=True,  # Redirects stdout/stderr
        text=True,  # Decodes output as a string (Python 3.5+)
    )
    return result.stdout

@mcp.tool()
async def fetch_web_page_curl(
    ip_address: str, scheme: str = "http", port: int = 80, path: str = "/"
) -> str:
    """
    Requests a web page using 'curl' and the given parameters. 

    Returns the HTML from a web page at the given IP address, port, and path

    Args:
        ip_address: The IPv4 or IPv6 address to check (e.g., "8.8.8.8")
        scheme: The scheme to use (default="http")
        port: The port to view (default=80)
        path: The path to view (default="/")

    Returns:
        HTML page at the IP address
    """
    result = subprocess.run(
        ["/usr/bin/curl", "-L", f"{scheme}://{ip_address}:{port}{path}"],
        capture_output=True,  # Redirects stdout/stderr
        text=True,  # Decodes output as a string (Python 3.5+),
        timeout=15,
    )
    return result.stdout


@mcp.tool()
async def send_http_payload_curl(
    ip_address: str,
    headers: dict,
    payload: str,
    scheme: str = "http",
    port: int = 80,
    path: str = "/",
    method: str = "POST",
) -> str:
    """
    Makes HTTP requests using 'curl' and the given parameters. 

    This tool allows for fine-grained request changes.

    You can manipulate HTTP requests with various curl flags to test for common API vulnerabilities, for example:
    - Test different HTTP Methods: Some APIs might allow unintended methods on specific endpoints
    - Send Data (POST requests): Test for injection vulnerabilities (like SQLi or OS command injection) by sending various payloads in the request body.
    - Handle Authentication: Pass cookies, API keys, or basic authentication credentials.


    Args:
        ip_address: The IPv4 or IPv6 address to check (e.g., "8.8.8.8").
        port: The port to view (default=80)
        path: The path to view (default="/")
        method: The HTTP method to use (default="POST")
        headers: A Python dict of request headers (i.e. {"Content-Type": "application/json"})
        payload: A request body to send

    Returns:
        HTML page at the IP address
    """

    headers_list = []
    for k, v in headers.items():
        headers_list.extend(["-H", f"{k}: {v}"])

    payload = f"-d '{payload}'"

    result = subprocess.run(
        ["/usr/bin/curl", "-L", "-X", method]
        + headers_list
        + [payload]
        + [f"{scheme}://{ip_address}:{port}{path}"],
        capture_output=True,
        text=True,
    )
    return result.stdout


if __name__ == "__main__":
    print("Starting LocalHacker FastMCP Server...")
    mcp.run(transport="stdio")
