import socket
import common_ports
import re


def get_open_ports(target, port_range, verbose=False):
  open_ports = [] if not verbose else []
  fmt = "{:<8} {:<}"
  ip = ""

  # Check if the target is an IP address
  is_ip_address = re.match(r"\d+\.\d+\.\d+\.\d+", target)

  if is_ip_address:
    ip = target
  else:
    try:
      ip = socket.gethostbyname(target)
      if verbose:
        open_ports.append(f"Open ports for {target} ({ip})")
        open_ports.append(fmt.format("PORT", "SERVICE"))
    except socket.gaierror:
      return "Error: Invalid hostname"

  for port in range(port_range[0], port_range[1] + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    try:
      if sock.connect_ex((ip, port)) == 0:
        if verbose:
          service = common_ports.ports_and_services.get(port, "Unknown")
          open_ports.append(fmt.format(port, service))
        else:
          open_ports.append(port)
    except socket.gaierror:
      return "Error: Invalid IP address"
    finally:
      sock.close()

  if verbose:
    return "\n".join(open_ports)

  return open_ports
