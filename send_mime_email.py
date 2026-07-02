import smtplib
from email.message import EmailMessage

# Create email message
msg = EmailMessage()
msg['Subject'] = 'MIME Test Email from Python'
msg['From'] = 'iamsantanu21@gmail.com'
msg['To'] = '24mtnispy0004@pondiuni.ac.in'
msg.set_content('This is a plain text email sent with MIME support.')

# Add HTML version
msg.add_alternative("""
<html>
  <body>
    <h1 style="color:blue;">Hello!</h1>
    <p>This is an <b>HTML</b> version of the email.</p>
  </body>
</html>
""", subtype='html')

# Add an attachment
with open("santanu.png", "rb") as f:
    file_data = f.read()
    file_name = f.name

msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

# Send the email via SMTP server
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login('iamsantanu21@gmail.com', 'zrfl twlj iqon pkck')  
    smtp.send_message(msg)

print("Email sent successfully with MIME content!")
