from dnsentry import DNSEntry
from table import Table
from table import read_hns_table

#table = Table("PROJ2-HNS.txt")

table = read_hns_table("PROJ2-HNS.txt")
print("Testing str()...")
print(table)

print("Testing equality...")
entry1 = DNSEntry(('mother', 'c', 3, 'd'))
entry2 = DNSEntry(('mother', 'c', 4, 'd'))
print(entry1 != entry2)

print("Testing len()...")
print(len(table))

print("Testing iteration...")
print("for each...")
for entry in table:
    print(entry)

print("for i in range...")
for i in range(0, len(table)):
    print(table[i])
