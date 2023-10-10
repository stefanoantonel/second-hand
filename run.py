#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import json


# In[2]:


BASE_URL = 'https://www.digitec.ch'


# In[3]:


def get_soup(url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    return soup

# In[5]:


def get_initial_price(soup):
    details = soup.find('div', attrs={'class': 'productDetail'})
    strong = details.find('strong')
    return strong.text


# In[6]:


def check_second_hand(soup, used_prices):
    used = soup.find('h4', string="Buy secondhand")
    if used is None:
        return used_prices

    for sibling in used.next_siblings:
        if sibling.a:
            price = sibling.a.div.strong.text
            url = sibling.a['href']
            used_prices.append(f"<a href='{BASE_URL}/{url}' target='_blank'>{price}</a>")
    return used_prices


# In[7]:


def find_other_links(soup):
    color_section = soup.find('h2', string="Colour")
    if color_section is None:
        return []

    other_phones = color_section.next_sibling
    a_tags = other_phones.find_all('a')

    links_other_devices = []
    for a_tag in a_tags:
        if 'href' not in a_tag.attrs:
            continue
        links_other_devices.append(a_tag['href'])
    return links_other_devices


# In[8]:

html_body = "<tr></tr>"

def crawling(url, title):
    global html_body
    used_prices = []
    
    soup = get_soup(url)
    initial_price = get_initial_price(soup)
    check_second_hand(soup, used_prices)

    for page in find_other_links(soup):
        page_url = f'{BASE_URL}{page}'
        other_soup = get_soup(page_url)
        check_second_hand(other_soup, used_prices)
    result = f'--- {title} ---> \t New {[initial_price]} > Used: {used_prices}'
    initial_title = f"<a href='{url}' target='_blank'>{title}</a>"
    table_data = f"<td>{initial_title}</td><td>{initial_price}</td><td>{used_prices}</td>"
    html_body += f"<tr>{table_data}</tr>"
    print(result)


# In[9]:

with open('./pages.json') as f:
    pages = json.loads(f.read())


# In[10]:
REFURBISHED_URL = 'https://www.apple.com/ch-de/shop/refurbished/ipad/ipad'
def generate_html(html_body):
    html = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    table, th, td {{
                        border: 1px solid black;
                        border-collapse: collapse;
                        width: 100%
                    }}
                    th, td {{
                        padding: 15px;
                    }}
                </style>
            </head>
            <body>
                <table>
                    <tr>
                        <th>Phone</th>
                        <th>New</th>
                        <th>Used</th>
                    </tr>
                    {html_body}
                </table>
                <br />
                <p>
                    <a href={REFURBISHED_URL} target="_blank">Refurbished</a>
                </p>
            </body>
        </html>
    '''
    with open('./dist/index.html', 'w') as f:
        f.write(html)


for page in pages:
    for url in page['urls']:
        crawling(url, page['title'])

generate_html(html_body)

