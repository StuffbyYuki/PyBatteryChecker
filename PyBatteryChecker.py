# Usage: python PyBatteryChecker.py -e YOUR_EMAIL_ADDRESS -p YOUR_PASS_FOR_YOUR_EMAIL_ACCOUNT
# Created by: Yuki Kakegawa

import psutil
import smtplib, ssl
import argparse
from email.mime.text import MIMEText
import time

def parse_args():
    """Get arguments taken from command line"""
    parser = argparse.ArgumentParser(description='Get credentials for sending email.')
    parser.add_argument('--email', '-e', required=True, help='email address')
    parser.add_argument('--emailpass', '-p', required=False, help='password for using your email account')
    args = parser.parse_args()

    return args

def send_email(receiver, password=None, subject=None, from_=None, to=None, content=None):
    """Send email to an email address that you specify"""
    sender = "smtp.gmail.com"
    port = 587  # For starttls

    # password = input("Type your password and press enter: ")    
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = to
    
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(sender, port)
        server.starttls(context=context) # Secure the connection
        server.login(receiver, password)
        server.sendmail(sender, receiver, msg.as_string())      
        print("Successfully sent email")
    except smtplib.SMTPException as e:
        # Print any error messages to stdout
        print("Error: unable to send email", e)
    finally:
        server.quit() 

def main():
    args = parse_args()

    # Send an email every five minutes until the battery reaches 100% 
    receiver = args.email
    password = args.emailpass
    subject = 'Battery Checker Result'
    from_ = 'PyBatteryChecker.py'
    to = args.email

    while True:
        battery = psutil.sensors_battery()
        battery_percent = str(battery.percent)
        pluggedin = "Plugged In" if battery.power_plugged else "Not Plugged In"
        content = f"Battery {battery_percent}% charged | Your computer is {pluggedin}\n"
        send_email(receiver, password, subject, from_, to, content)
        if battery_percent == '100':
            break
        else:
            print("Waiting on the battery life to reach 100%...\n")
            time.sleep(300)

if __name__ == '__main__':
    main()
