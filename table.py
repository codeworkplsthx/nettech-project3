#from typing import Tuple

from dnsentry import DNSEntry

import socket as mysoc


class Table:
    _entries = []

    def __init__(self, source):
        with open(source, 'r') as file:
            for line in file.readlines():
                self._entries.append(DNSEntry.from_str(line))

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, item) -> bool:
        for e in self._entries:
            if item == e:
                return True
        return False

    def __repr__(self):
        return str(self._entries)

    def __str__(self):
        return str(self._entries)

    def __setitem__(self, item):
        self._entries.append(DNSEntry(item))

    def __getitem__(self, item):
        if type(item) == Tuple[str, str, int, str]:

            for e in self._entries:
                if item == e:
                    return item

        elif type(item) == int:
            return self._entries[item]

    def __iter__(self):
        return self._entries.__iter__()

    def append(self, item: DNSEntry):
        self._entries.append(DNSEntry(item))


def _process_line(line):
    return DNSEntry(line.rstrip("\r\n").split(' '))


# reads list of hostnames into a list
def read_hns_table(which : str) -> list:
    hns_table = list()
    for line in open(which, 'r'):
        hns_table.append(line.rstrip("\n\r"))

    return hns_table


def create_socket() -> mysoc.socket:
    try:
        socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        return socket
        # complain if can't create socket
    except mysoc.error as err:
        print('socket open error ' + str(err) + '\n')


def read_dns_table(which : str) -> [DNSEntry]:
    dns_table = list()
    for line in open(which, 'r'):
        hostname, ip, port, qtype = line.split(' ')
        hostname = hostname.rstrip("\n\r")
        ip = ip.rstrip('\n\r')
        port = port.rstrip('\n\r')
        qtype = qtype.rstrip('\n\r')
        entry = DNSEntry(hostname, ip, port, qtype)
        dns_table.append(entry)

    return dns_table
