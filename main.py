import sys
import json

sys.path.insert(1, f"{sys.path[0]}/modules/scanning")
sys.path.insert(1, f"{sys.path[0]}/modules/identification_vuln")

from default_subdomain_enum import *
from default_port_scan import *
from default_crawl_website import *
from default_ident_vuln import *

if __name__ == "__main__":

    try:
        target = sys.argv[1]
    except:
        "пожалуйста введите имя домена или ip"

    print('создается стартовый файл target.json с дефолтными настройками')

    default_json = {'target': target, "settings": {"subdomain_wordlist": "subdomain_wordlist.txt"} }

    with open('target.json', 'w') as f:
        json.dump(default_json, f, indent=4)

    subdomain_enumeration()
    crawl_website()
    port_scan()
    ident_vuln()

    print('с результатами можете ознакомиться в файле target_chain_4.json')
        



    