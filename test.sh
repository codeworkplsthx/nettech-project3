#!/bin/bash
python3 ./com.py ./PROJ2-DNSCOM.txt
python3 ./edu.py ./PROJ2-DNSEDU.txt
python3 ./rs.py localhost localhost PROJ2-DNSRS.txt
python3 ./client.py ./PROJ2-HNS.txt

