class DNSEntry:
    hostname = str()
    ip = str()
    port = int()
    qtype = str()

    # construcor for tuple
    def __init__(self, item):
        self.hostname, self.ip, self.port, self.qtype = item

    def __init__(self, hn, ip, port, type):
        self.hostname = hn
        self.ip = ip
        self.port = port
        self.qtype = type

    def __str__(self):
        return self.hostname + " " + self.ip + " " + str(self.port) + " " + self.qtype

    def __repr__(self):
        return self.hostname + " " + self.ip + " " + str(self.port) + " " + self.qtype

    def __eq__(self, other):
        if (self.hostname, self.ip, self.port, self.qtype) == (other.hostname, other.ip, other.port, other.qtype):
            return True
        else:
            return False

    @staticmethod
    def from_str(entry : str):
        entry = entry.rstrip("[]\n\r").lstrip("[]\n\r")  # clear out junk in the string
        hn, ip, port, type = entry.split(' ')  # split into its fields
        port = int(port)  # port must be an int
        return DNSEntry(hn, ip, port, type)
