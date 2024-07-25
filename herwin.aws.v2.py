#################################
#Author : Herwin Yudha S
#Github : hysspy
#Update : 25 July 2024 11:20 SGT
#################################

import os
import psutil
import time
import logging
import ssl
import smtplib
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Firefox
from Screenshot import Screenshot

#Start DEBUG Logging
#LOG_FNAME = datetime.now().strftime('D:/Path to/Python/Log/debuglog-%H_%M_%S_%d_%m_%Y.log')
#for handler in logging.root.handlers[:]:
#    logging.root.removeHandler(handler)
#logging.basicConfig(filename=LOG_FNAME,level=logging.DEBUG)
#logging.basicConfig(filename=LOG_FNAME,level=logging.INFO)  
#logging.info('Forecasting Job Started...')
#logging.debug('abc method started...')

#Print SHELL LOG to file
LOG_FILENAME = datetime.now().strftime('C:/Path/To/Python/Log/shelllog-%H_%M_%S_%d_%m_%Y.log')
log = open(LOG_FILENAME, 'w')

def oprint(message):
    print(message)
    global log
    log.write(message + "\n")
    return()

oprint("=======START LOG=======")

# Setup Firefox driver
options = Options()
options.add_argument('--headless')
options.add_argument('--hide-scrollbars')
options.add_argument('--disable-gpu')
driver = Firefox(options = options)

ob = Screenshot.Screenshot()

# Navigate to the url
driver.get('M1-aws-link')

# Take a screenshot
driver.save_screenshot("screenshot-1.png")
oprint("Open Web OK")

#input text box
# Find input text field
input_text_fname = driver.find_element(By.ID, 'account')

# Take a screenshot before entering a value
driver.save_screenshot("screenshot-2.png")
oprint("Save OK")

# Enter a value in the input text field
input_text_fname.send_keys("Phone-number")
oprint("Input Numbers OK")

# Take a screenshot after entering a value
driver.save_screenshot("screenshot-3.png")
oprint("Save OK")

#input username
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))).send_keys("Secret")
driver.find_element(By.XPATH, "//input[@id='password']").send_keys("Secret")
oprint("Login OK")

# Take a screenshot after entering a value
driver.save_screenshot("screenshot-4.png")
oprint("Save OK")

#press signin
button = driver.find_element(By.ID, 'signin_button')
button.click()

oprint("Wait 16s")
time.sleep(16)

###Enable below when Expired password appear on aws page
#press continue
#button = driver.find_element(By.ID, 'continue_button')
#button.click()

#oprint("Wait 16s")
#time.sleep(16)
#####################

# Take a screenshot after entering a value
S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),1263) # May need manual adjustment                                                                                                                
#ob.find_element(By.TAG_NAME, 'body').screenshot('screenshot-7.png')
element = driver.find_element(By.TAG_NAME, 'body')
img_url = ob.get_element(driver, element, save_path=r'C:\Path\To\Python\', image_name='M0AWS.png')
oprint(img_url)
oprint("GET FINAL ScreenShot OK")

# Close the driver
driver.close()
oprint("Close Driver")
driver.quit()
oprint("Quit Driver")

oprint("Wait 2s")
time.sleep(2)

#######Crop image#######
#Create an Image Object from an Image
im = Image.open('M0AWS.png')
oprint("Load Image OK")

#left, upper, right, lower Crop
cropped = im.crop((43,75,1356,744))

#Save the cropped image
cropped.save('M1AWS.png')
oprint("CROP OK")

oprint("Preparing Email")
#######SEND MAIL######

###########################
# Define the HTML document
# Add an image element
##############################################################
html = '''
    <html>
        <body>
            <h3>M1 AWS DBMonitoring</h3>
            <img src='cid:M1AWS.png'> 
        </body>
    </html>
    '''
##############################################################

# Define a function to attach files as MIMEApplication to the email
    ## Add another input extra_headers default to None
##############################################################
def attach_file_to_email(email_message, filename, extra_headers=None):
    # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
    with open(filename, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    # Add header/name to the attachments    
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Set up the input extra_headers for img
      ## Default is None: since for regular file attachments, it's not needed
      ## When given a value: the following code will run
         ### Used to set the cid for image
    if extra_headers is not None:
        for name, value in extra_headers.items():
            file_attachment.add_header(name, value)
    # Attach the file to the message
    email_message.attach(file_attachment)
##############################################################    

#Load env creds
load_dotenv()
oprint("Load Creds")
# Set up the email addresses and password. Please replace below with your email address and password
toaddr = ['Emailto']
cc = ['Emailcc']
email_from = 'GatewayEmail'
usrname = os.getenv("secretUser")
password = os.getenv("secretPass")

# Generate today's date to be included in the email Subject
date_str = pd.Timestamp.today().strftime('%d/%m/%Y, %H:%M')

# Create a MIMEMultipart class, and set up the From, To, Subject fields
email_message = MIMEMultipart()
email_message['From'] = email_from
email_message['To'] = ','.join(toaddr)
email_message['Cc'] = ','.join(cc)
email_message['Subject'] = f'M1 AWS Hourly Report {date_str} SGT'

# Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
email_message.attach(MIMEText(html, "html"))

# Attach more (documents)
## Apply function with extra_header on m1aws.png. This will render m1aws.png in the html content
##############################################################
attach_file_to_email(email_message, 'M1AWS.png', {'Content-ID': '<M1AWS>'})
##############################################################

# Convert it as a string
email_string = email_message.as_string()

# Connect to the SMTP server and send the email
smtp_server = "smtp-mail"
smtp_port = smtp-port

#context = ssl.create_default_context()

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(usrname, password)  # Check above username & password
    server.sendmail(email_from, (toaddr+cc), email_string)
    server.quit()
oprint("Email Sent OK")

#Close multiple processes selenium firefox + geckodriver
os.system('taskkill /f /t /im firefox.exe /fi "USERNAME eq (name)"')
oprint("Close firefox")
time.sleep(2)
os.system('taskkill /f /t /im geckodriver.exe /fi "USERNAME eq (name)"')
oprint("Close geckodriver")

#Clean Old Log Files more than 1 days
oprint("Checking Logs if older than 1 days...")

folder = "Log"

#older than the specified days
N = 1

#changing the current working directory to the folder specified
os.chdir(os.path.join(os.getcwd(), folder))

#get a list of files present in the given folder
list_of_files = os.listdir()

#get the current time
current_time = time.time()

#"day" is the number of seconds in a day
day = 86400

#loop over all the files
for i in list_of_files:
	#get the location of the file
	file_location = os.path.join(os.getcwd(), i)
	#file_time is the time when the file is modified
	file_time = os.stat(file_location).st_mtime

	#if a file is modified before N days then delete it
	if(file_time < current_time - day*N):
		oprint(f" Delete : {i}")
		os.remove(file_location)

oprint(".......Done")
oprint("=======END LOG=======")
log.close()
