from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import os

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import math,random

global temp
temp = []

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('home.html')


@app.route('/apply')
def apply():
    return render_template('internForm.html')


@app.route('/internn', methods=['POST'])
def internn():
    if request.method == 'POST':
        category = request.form['category']
        loc = request.form['loc']
    
    return category + '  ' + loc

@app.route('/home')
def home():
    return render_template('home.html')

# Code for InternDAta

@app.route('/intern', methods=['POST'])
def intern():
    if request.method == 'POST':
        category = request.form['category']
        loc = request.form['loc']
        loc.lower()
        url = ''
        if(loc == 'online'):
            url = 'https://internshala.com/internships/' + category + '-internship'
        else:
            url = 'https://internshala.com/internships/' + category + '-internship-in-' + loc + '?ref=home'

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        jobs = soup.find_all('div', class_='internship_meta')

        
        res = []
        for job in jobs:
            title = ''
            company = ''
            location = ''
            stipend = ''
            link = ''

            title_elem = job.find('h3', class_='heading_4_5 profile')
            if title_elem is not None:
                title = title_elem.text.strip()
                # print(title)

            company_elem = job.find('h4', class_='heading_6 company_name')
            if company_elem is not None:
                company = company_elem.text.strip()
                # print(company)

            location_elem = job.find('div', class_='individual_internship_details')
            if location_elem is not None:
                location = location_elem.find('a', class_='location_link').text.strip()
                # print(location)

            stipend_elem = job.find('span', class_='stipend')
            if stipend_elem is not None:
                stipend = stipend_elem.text.strip()
                # print(stipend)
            else:
                stipend = '10,000 / month'

            link_elem = job.find('a', href=True)
            if link_elem is not None:
                link = 'https://internshala.com' + link_elem['href']
                # print(link)

            if(title and company):
                dict2 = {
                    'title': title,
                    'company': company,
                    'location': location,
                    'stipend': stipend,
                    'link': link
                }

            res.append(dict2)
        temp.append(res)
    return render_template('intern.html', res=res)


#code for sending mail
@app.route('/mail', methods = ['GET','POST'])
def mail():
    if request.method == 'POST':

        toaddr = request.form['email']
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        fromaddr = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        server.login(fromaddr,password)

        subject = 'Top Internship Picks From Finder Deck'
        # toaddr = 'levinholevi4139@gmail.com'

        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL")
        msg['Subject'] = subject

        data = temp[0]
        a1 = random.randint(0,len(data))
        a2 = random.randint(0,len(data))

        dict_a = data[a1]
        dict_b = data[a2]
        body = ''' 
            Here are the top picks from Finder Desk based on your internest !!!\n
            1.  Intern title: {} \n
                Organisation: {} \n
                Stipend: {} \n
                Apply Here:  {} \n

            2.  Intern title: {} \n
                Organisation: {} \n
                Stipend: {} \n
                Apply Here:  {} \n

            Thank You for using Finder Desk !!!

            '''.format(dict_a['title'],dict_a['company'],dict_a['stipend'], dict_a['link'], dict_b['title'], dict_b['company'], dict_b['stipend'], dict_b['link'])

        



        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(fromaddr, toaddr, msg.as_string())
        print("Sent succesfully")

        server.quit()

        # return 'Sent succesfully'
        return render_template('index.html')



# Code for testing
@app.route('/test')
def test():
    data = temp[0]
    dict_a = data[0]
    print(dict_a['title'])

    return "hellow"

@app.route('/testing')
def testing():
    url = 'https://internshala.com/internships/python%2Fdjango-internship-in-bangalore/'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    jobs = soup.find_all('div', class_='internship_meta')

    res = []
    for job in jobs:
        title = ''
        company = ''
        location = ''
        stipend = ''
        link = ''

        title_elem = job.find('h3', class_='heading_4_5 profile')
        if title_elem is not None:
            title = title_elem.text.strip()
            print(title)

        company_elem = job.find('h4', class_='heading_6 company_name')
        if company_elem is not None:
            company = company_elem.text.strip()
            print(company)

        location_elem = job.find('div', class_='individual_internship_details')
        if location_elem is not None:
            location = location_elem.find('a', class_='location_link').text.strip()
            print(location)

        stipend_elem = job.find('span', class_='stipend')
        if stipend_elem is not None:
            stipend = stipend_elem.text.strip()
            print(stipend)
        else:
            stipend = '10,000 / month'

        link_elem = job.find('a', href=True)
        if link_elem is not None:
            link = 'https://internshala.com' + link_elem['href']
            print(link)

        if(title and company):
            dict2 = {
                'title': title,
                'company': company,
                'location': location,
                'stipend': stipend,
                'link': link
            }

        res.append(dict2)
    return render_template('intern.html', res=res)



# Flask Application

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)



