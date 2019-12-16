def is_address_valid(address):
    tup = address.split(':')
    if len(tup) > 2:
        return False
    if len(tup) == 2:
        ip, port = tup
        ip_parts = ip.split('.')
        if len(ip_parts) != 4:
            return False
        for ip_part in ip_parts:
            if not ip_part.isdigit():
                return False
            if int(ip_part) < 0 or int(ip_part) > 255:
                return False
    else:
        port = address
    if not port.isdigit():
        return False
    if int(port) < 0 or int(port) > 65535:
        return False
    return True


def get_address_tuple(address):
    tup = address.split(':')
    if len(tup) == 1:
        ip = '0.0.0.0'
        port = int(address)
        return (ip, port)
    ip, port = tup
    return (ip, int(port))
