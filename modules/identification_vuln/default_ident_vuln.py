import requests
import json

def get_cpe(product, version):
    url = "https://services.nvd.nist.gov/rest/json/cpes/2.0"
    params = {
        'cpeMatchString': f"cpe:2.3:a:{product.lower()}:*:{version}:*:*:*:*:*:*:*",
        'resultsPerPage': 1  # Получаем только первый результат
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return None
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else {err}")
        return None

    try:
        cpe_data = response.json()
        cpe_match_string = cpe_data['products'][0]['cpe']['cpeName']
        return cpe_match_string
    except (ValueError, KeyError, IndexError):
        print("Ошибка декодирования JSON или данные не найдены.")
        print("Содержимое ответа сервера:", response.text)
        return None

def search_cve_by_cpe(cpe_match_string):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    cpeName = cpe_match_string
    resultsPerPage = 20  # Количество результатов на страницу
    startIndex = 0        # Начальный индекс для пагинации

    url += f"?cpeName={cpeName}&isVulnerable=&resultsPerPage={resultsPerPage}&startIndex={startIndex}"

    all_cve_items = []

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return []
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return []
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return []
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else {err}")
        return []

    try:
        cves = response.json()
        for cve_items in cves['vulnerabilities']:
            all_cve_items.append((cve_items['cve']['id'], cve_items['cve']['descriptions'][0]['value']))
    except ValueError:
        print("Ошибка декодирования JSON.")
        print("Содержимое ответа сервера:")
        return []

    return all_cve_items


def ident_vuln():
    with open(f"target_chain_3.json", 'r') as f:
        data = json.load(f)
    all_software = []
    for domain in data['subdomains']:
        all_software = data['subdomains'][domain]['site_info'] + \
            data['subdomains'][domain]['ports_info'] 
        
        for soft in all_software:
            product, version = soft
            product = product.split()[0]
            cpe_match_string = get_cpe(product, version)
            if cpe_match_string:
                cve_items = search_cve_by_cpe(cpe_match_string)
            else:
                print("CPE для данного продукта и версии не найден.")
        try:
            data['subdomains'][domain]['vulns'] = cve_items
        except UnboundLocalError:
            pass

    with open(f"target_chain_4.json", 'w') as f:
        json.dump(data, f, indent=4)


# ident_vuln()        