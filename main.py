import requests
from bs4 import BeautifulSoup
import pandas as pd

product_name_array = []
product_category_array = []
product_description_array = []
product_rating_array = []
product_price_array = []
product_availability_array = []

def start_web_scraping():
    #Collecting data from 50 pages from the website
    for i in range(1, 51):
        print("Starting Web Scraping...")
        url = 'https://books.toscrape.com/catalogue/category/books_1/page-'+str(i)+'.html'
        print("Fetching all books for page "+str(i))
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        page_h3_tags = soup.findAll('h3')
        for h3 in page_h3_tags:
            h3_href_attribute = h3.find('a')['href']
            href_individual_book_endpoint = h3_href_attribute.split("/")[2]
            individual_book_page_url = 'https://books.toscrape.com/catalogue/'+href_individual_book_endpoint+'/index.html'
            individual_book_page = requests.get(individual_book_page_url)
            individual_book_page_content = BeautifulSoup(individual_book_page.content, 'html.parser')

            print("Fetching Book(s) details...")
            product_category = individual_book_page_content.find('ul',class_='breadcrumb').findAll('li')[2].find('a').text
            product_name = individual_book_page_content.find('div', class_='col-sm-6 product_main').find('h1').text
            product_price = individual_book_page_content.find('p', class_='price_color').text
            product_availability = individual_book_page_content.find('p', class_='instock availability').text.strip()
            product_rating = individual_book_page_content.find('div', class_='col-sm-6 product_main').findAll('p')[2]['class'][1]

            if (individual_book_page_content.find('div', id='product_description')):
                product_description = individual_book_page_content.find('div', id='product_description').find_next('p').text
            else:
                product_description = 'Description not provided'
            product_name_array.append(product_name)
            product_category_array.append(product_category)
            product_description_array.append(product_description)
            product_availability_array.append(product_availability)
            product_price_array.append(product_price)
            product_rating_array.append(product_rating)


def display_scraped_data_in_csv():
    print("Data Fetching Completed Successfully...")
    print("Appending data to csv file...")
    df = pd.DataFrame({
                  'Product Name': product_name_array,
                  'Product Category': product_category_array,
                  'Product Description': product_description_array,
                  'Product Availability': product_availability_array,
                  'Product Price': product_price_array,
                  'Product Rating': product_rating_array
                  })
    df.to_csv(r'Generated_Books_Data_After_Web_Scraping.csv', encoding='utf-8-sig')
    print("data append to csv file completed...")
    print("You can find the generated csv in project's root folder...")

start_web_scraping()
display_scraped_data_in_csv()