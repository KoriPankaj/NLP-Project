#pip install pandas


import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


input_data = pd.read_excel(r"E:\Black COffer\20211030 Test Assignment\Input.xlsx")

output_directory = "Data_extracted"
os.makedirs(output_directory, exist_ok=True)

for i, j in input_data.iterrows():
    url = j['URL']
    url_id = j['URL_ID']
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string
    print(title)
    article_content = ""
    class_name = ['td-post-content tagdiv-type', 'tdb-block-inner td-fix-index']
    
    for k in class_name:
        main_article_div = soup.find('div', class_= k)
       
        
        filename = os.path.join(output_directory, f'{url_id}.txt')
        if response.status_code == 404:
            tit = "Page not found"
            
            with open(filename,'w', encoding= 'utf-8') as file:
                file.write(tit + "\n")
                
        elif main_article_div:
            for paragraph in main_article_div.find_all('p'):
                article_content += paragraph.get_text() + "\n"
                
            art_tit = title + "\n" + article_content
            
            with open(filename, 'w', encoding= 'utf-8') as file:
                file.write(art_tit)
    
    

