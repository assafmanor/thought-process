def is_address_valid(address):
    tup = address.split(':')
    if len(tup) != 2:
        return False
    ip, port = tup
    ip_parts = ip.split('.')
    if len(ip_parts) != 4:
        return False
    for ip_part in ip_parts:
        if not ip_part.isdigit():
            return False
        if int(ip_part) < 0 or int(ip_part) > 255:
            return False
    if not port.isdigit():
        return False
    if int(port) < 0 or int(port) > 65535:
        return False
    return True
