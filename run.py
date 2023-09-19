#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests


# In[2]:


BASE_URL = 'https://www.digitec.ch'


# In[3]:


def get_soup(url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    return soup


# In[4]:


soup = get_soup('https://www.digitec.ch/en/s1/product/google-pixel-7a-128-gb-charcoal-610-sim-esim-64-mpx-5g-smartphones-32960864')


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
            used_prices.append(price)
    return used_prices


# In[7]:


def find_other_links(soup):
    color_section = soup.find('h4', string="Colour")
    other_phones = color_section.next_sibling
    a_tags = other_phones.find_all('a')

    links_other_devices = []
    for a_tag in a_tags:
        if 'href' not in a_tag.attrs:
            continue
        links_other_devices.append(a_tag['href'])
    return links_other_devices


# In[8]:

html_body = "<br />"

def crawling(url, title):
    global html_body
    used_prices = []
    
    soup = get_soup(url)
    initial_price = get_initial_price(soup)
    check_second_hand(soup, used_prices)

    for page in find_other_links(soup):
        other_soup = get_soup(f'{BASE_URL}{page}')
        check_second_hand(other_soup, used_prices)
    result = f'--- {title} ---> \t New {[initial_price]} > Used: {used_prices}'
    html_body += f"<br/> <p>--- {title} ---> New {initial_price} > Used: {used_prices}</p>"
    print(result)


# In[9]:


pages = [
    {
        'urls': ['https://www.digitec.ch/en/s1/product/google-pixel-7a-128-gb-charcoal-610-sim-esim-64-mpx-5g-smartphones-32960864'],
        'title': 'Pixel 7a'
    },
    {
        'urls': ['https://www.digitec.ch/en/s1/product/google-pixel-6a-128-gb-charcoal-610-sim-esim-1220-mpx-5g-smartphones-21531648'],
        'title': 'Pixel 6a'
    },
    {
        'urls': [
            'https://www.digitec.ch/en/s1/product/apple-ipad-2022-10-gen-wlan-only-1090-64-gb-yellow-tablets-22715682',
            'https://www.digitec.ch/en/s1/product/apple-ipad-2022-10-gen-wlan-only-1090-64-gb-silver-tablets-22715680'
        ],
        'title': 'iPad 10'
    },
    {
        'urls': ['https://www.digitec.ch/en/s1/product/apple-iphone-13-128-gb-pink-610-sim-esim-12-mpx-5g-smartphones-16644873'],
        'title': 'iPhone 13'
    },
    {
        'urls': ['https://www.digitec.ch/en/s1/product/apple-iphone-13-mini-128-gb-midnight-540-sim-esim-12-mpx-5g-smartphones-16644786'],
        'title': 'iPhone 13 mini'
    },
]


# In[10]:

def generate_html(html_body):
    html = f'''
        <!DOCTYPE html>
        <html>
            <body>
                <div>{html_body}</div>
            </body>
        </html>
    '''
    with open('./dist/index.html', 'w') as f:
        f.write(html)


for page in pages:
    for url in page['urls']:
        crawling(url, page['title'])

generate_html(html_body)

