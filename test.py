import smtplib

EMAIL = "addinzafran1505@gmail.com"
PASS = "wlgwspoevnqnpepp" # PASTE YOUR 16-CHAR APP PASSWORD HERE

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, PASS)
    print("Success! Your credentials are correct.")
    server.quit()
except Exception as e:
    print(f"Failed: {e}")