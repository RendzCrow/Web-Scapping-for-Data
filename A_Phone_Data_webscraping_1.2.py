import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

# Code that allows me to check if the website is accessible
# The reqired results of the code is 200, if the result is 200 then the website is accessible.
# If the result is 404 then the website is not accessible. Then the website is forbiden to access.
def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}
    url = f"https://www.amazon.co.za/s?k=phones&crid=3452RT32SZUYO&qid=1740504908&sprefix=phones+%2Caps%2C403&xpid=Sq1pKBkoXjceZ&ref=sr_pg_{page}"
    r = requests.get(url, headers)
    # The code below is an advance method of checking if the website is accessible. within the function extract(page).
    #Before using the reurn r.status_code, make sure to comment out the return soup, below it.
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Failed to access page {page}: {e}")
        return None
    
    if r.status_code != 200:
        print(f"Failed to access page {page}: Status Code {r.status_code}")
        return None
    
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup
#If you are not checking for the status code, please make sure that the code below is commented out.
# print(extract(1))

# This function is used to fetch data from the website, that has been passed the extract function above.
def transform(soup):
    divs = soup.find_all('div', class_='sg-col-4-of-24')
    #Line of code below is used to check the length of the divs, in a way to check that you have identified the correct divs.
    # make sure that the rest of the code below the len function is commented out. 
    #return len(divs)
    for item in divs:
        # The code below scrapes the phone model from the website.
        #make sure to be able to identify the correct class of when inspecing the website. 
        #Dont be stuck on one class that work, look for the ones that work with data you want to scrape from the website.
        phone_element = item.find('h2', class_='a-size-base-plus a-spacing-none a-color-base a-text-normal')  
        if phone_element:
            phone_model = phone_element.text.strip()
        else:
            phone_model = 'No phone_model available'

        rating_element = item.find('span', class_='a-icon-alt') 
        if rating_element:
            rating = rating_element.text.strip()
        else:
            rating = 'No rating available'
        #This code is a bit tricky, because the class is not easily identifiable, so it works.
        price_element = item.find('span', class_='a-price-whole')  
        if price_element:
            price = price_element.text.strip()
        else:
            price = 'No price available'

        phone = {
            'phone_model': phone_model,
            'rating': rating,
            'price': price
        }
        phone_list.append(phone)
    return

# The code below is used to check if the transform function is working correctly.
#Make sure to comment out the rest of the code below the return phone_list.
c = extract(1)
# print(transform(c)) 


phone_list = []
page = 1

while True:
    print(f"Scraping page {page}...")
    c = extract(page)
    if c:
        transform(c)
        page += 1
        time.sleep(2)  # Add a delay to avoid blocking
    else:
        break

# for i in range(1, 20,1):
#     c = extract(1)
#     transform(c)


df = pd.DataFrame(phone_list)
print(df.head())
df.to_csv('Amazon_Phones.csv', index=False)

    





