import os
import requests #for getting the pdf files or url
from bs4 import BeautifulSoup #for tree traversal scraping in a webpage
from urllib.parse import urljoin

url="https://math.bme.hu/~nagyat/peldatar/" #website toscrap
folder='Peldatar pdfs'

if not os.path.exists(folder):  #creates a folder if it's not there already
  os.makedirs(folder)

response=requests.get(url) #sends HTTP GET req to the website
if response.status_code==200: #successful req
  soup=BeautifulSoup(response.text,'html.parser') #parse the HT?L content of the page
  links=soup.find_all('a',href=True) #finds all the links on the page

  for i in links:    #iterate through the links
    href=i.get('href')
    if href.endswith('.pdf'):
      pdf_url=urljoin(url,href)
      #get the pdf file's name (the part after the last / in the url)
      pdf_filename=os.path.join(folder,pdf_url.split('/')[-1]) 

      pdf_response=requests.get(url)  #send a HTTP GET req to the pdf url
      if pdf_response.status_code==200:
        with open(pdf_filename,'wb') as pdf_file:
          pdf_file.write(pdf_response.content)
        print(f"Downloaded: {pdf_filename}")
      else:
        print(f"Failed to download: {pdf_filename}")
else:
  print(f"Failed to reach {url}")