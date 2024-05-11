import socket


class Instance:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name


class RetrieveInstanceIPs:
    def get_ips(self, address):
        host, port = address.split(':')
        ais = socket.getaddrinfo(host=host, port=port)

        ip_set = set()
        for result in ais:
            ip_set.add(result[-1][0])

        result = []
        for ip in ip_set:
            result.append(Instance(ip, port, host))

        return result
