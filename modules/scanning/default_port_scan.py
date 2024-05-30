import json
import requests
import re
from bs4 import BeautifulSoup
from queue import Queue
import os
import nmap

## выборка поддоменов
## получам уникальные ip из всех поддоменов.
## применяем nmap с определенными флагами для них


def port_scan():
    with open('target_chain_2.json', 'r') as file:
        data = json.load(file)
    for url in data['subdomains'].keys():

        if "https" in url:
            domain = url[8::]
        elif "http" in url:
            domain = url[7::]

        nm = nmap.PortScanner()
        nm_data = nm.scan(hosts=domain, arguments='-sC -sV -p22-443')

        ports_path = nm_data['scan'][list(nm_data['scan'].keys())[0]]['tcp']

        ports_info = set()

        for port in ports_path.keys():
            product = ports_path[port]['product']
            version = ports_path[port]['version']
            if product != "" and version != "":
                ports_info.add((product, version))
        
        data['subdomains'][url]['ports_info'] = list(ports_info)

    with open(f"target_chain_3.json", 'w') as f:
        json.dump(data, f, indent=4)
        
# port_scan()

        