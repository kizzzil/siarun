import json
import requests
import re
from bs4 import BeautifulSoup
from queue import Queue


def find_program_info(text, regex_list):
    res = []
    for pattern in regex_list:
        find_versions = re.search(pattern, text)
        if not(find_versions is None):
            res.append(find_versions.group(0))
    return res

def crawl(site, html_regexes, url_regexes):
    
    q = Queue()
    q.put(site)

    visited_urls = []

    result = set()

    while not q.empty():
        current_page = q.get()
        print(current_page)
        try:
            response = requests.get(current_page)
        except:
            print("что-то пошло не так ...")
            continue
        
        progr_info_in_body = find_program_info(response.text, html_regexes)

        if progr_info_in_body:
            for info in progr_info_in_body:
                result.add(info)

        progr_info_in_url = find_program_info(current_page, url_regexes)

        if progr_info_in_url:
            for info in progr_info_in_url:
                ## ПОКА ЗАХАРДКОДИЛ
                if 'wp-content/plugins/' in info:
                    size = len('wp-content/plugins/')
                    info = "WP plugin " + info[size::]
                elif 'wp-content/themes/' in info:
                    size = len('wp-content/themes/')
                    info = "WP theme " + info[size::]

                name = re.search(r'WP \w+ (\w|-|\d)+\/', info).group()
                name = name[:-1:]
                version = re.search(r'ver=\d+\.\d+(\.\d+)?', info).group()
                
                result.add(f'{name} {version}')
        
        soup = BeautifulSoup(response.content, "html.parser")

        html_hrefs = str(soup.select("[href]"))

        pattern = r'href=[\'"]?([^\'" >]+)'
        urls = re.findall(pattern, html_hrefs)

        exclude_filetype = ['.js', 'css', 'php', 'jpg', 'xml']
        exclude_first_char = ['#', ':', "$", "@"]
        
        for url in urls:
            if url[0] == 'h' or url[0] == '/':
                if current_page in url and url not in visited_urls and url[-3::] not in exclude_filetype:
                    visited_urls.append(url)
                    q.put(url)
                elif url[:4:] != 'http' and (current_page + url) and url[-3::] not in exclude_filetype\
                        not in visited_urls and url != '\\':
                    visited_urls.append(current_page + url)
                    q.put(current_page + url)

    result = list(result)
    return result


def crawl_website():
    with open('target_chain_1.json', 'r') as file:
        data = json.load(file)

    url_regexes = [r'wp-content/plugins/.+ver=\d+\.\d+(\.\d+)?', 
                   r'wp-content/themes/.+ver=\d+\.\d+(\.\d+)?']
    html_regexes = [r'Apache/([0-9]+\.[0-9]+\.[0-9]+)', 
                    r'WordPress ([0-9]+\.[0-9]+(\.[0-9]+)?)', 
                    r'nginx/([0-9]+\.[0-9]+\.[0-9]+)']
    
    with open('target_chain_2.json', 'w') as file:
        tmp_subdomain_data = {}
        for url in data['subdomains']:
            tmp_subdomain_data[f'{url}'] = {}
            tmp_subdomain_data[f'{url}']['site_info'] = crawl(url, html_regexes, url_regexes)
        data['subdomains'] = {}
        data['subdomains'] = tmp_subdomain_data
        json.dump(data, file, indent=4)

crawl_website()