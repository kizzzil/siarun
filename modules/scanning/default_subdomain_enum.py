import json
import requests
from requests.exceptions import HTTPError

def subdomain_enum(site, wordlist_path):
    valid_subdomain = []

    with open(wordlist_path, 'r') as wordlist:
        list_subdomain_prefix = wordlist.readlines()
        # орабатываем конец строки \n в wordlist
        for i_prefix in range(len(list_subdomain_prefix)):
            if list_subdomain_prefix[i_prefix][-1] == '\n':
                list_subdomain_prefix[i_prefix] = list_subdomain_prefix[i_prefix][:-1:]

    for prefix in list_subdomain_prefix:
        http_err = True 
        https_err = True 

        # попытка подключения по http
        # try:
        #     print(f"connect to http://{prefix}.{site}")
        #     requests.get(f"http://{prefix}.{site}")
        #     http_err = False
        # except (HTTPError, ConnectionError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        #     print('HTTP ERROR')
            

        # попытка подключения по https
        try:
            print(f"connect to https://{prefix}.{site}")
            requests.get(f"http://{prefix}.{site}")
            https_err = False
        except (HTTPError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print('HTTPs ERROR')
            
            
        if not(http_err):
            valid_subdomain.append(f"http://{prefix}.{site}")
        if not(https_err):
            valid_subdomain.append(f"https://{prefix}.{site}")

    return valid_subdomain

def subdomain_enumeration():
    # десериализация из json
    with open('target.json', 'r') as file:
        data = json.load(file)


    valid_subdomain = subdomain_enum(data['target'], \
                                     data['settings']['subdomain_wordlist'])
    data['subdomains'] = valid_subdomain

    valid_subdomain.append(f"https://{data['target']}")
    # сериализация в json
    with open('target_chain_1.json', 'w') as file:
        json.dump(data, file, indent=4)
        
subdomain_enumeration()