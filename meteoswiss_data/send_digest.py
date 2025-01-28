from aktuelle_messwerte import get_aktuelle_messwerte
from foehnindex import get_foehnindex
from modellvorhersage_COSMO_2E import get_COSMO_forecast

foehnindex = get_foehnindex()

foehnindex.to_csv('foehnindex.csv', index=False)



# def send_email_digest(subject, body):
#     # Replace the placeholders with your email details
#     smtp_server = 'your_smtp_server'
#     smtp_port = 587
#     email_from = 'your_email@example.com'
#     email_password = 'your_email_password'
#     email_to = 'recipient@example.com'

#     msg = MIMEMultipart()
#     msg['From'] = email_from
#     msg['To'] = email_to
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(email_from, email_password)
#         server.sendmail(email_from, email_to, msg.as_string())
#         server.quit()
#         print("Email sent successfully!")
#     except smtplib.SMTPException as e:
#         print("Error sending email:", str(e))

# def generate_digest():
#     # Generate the email digest
#     subject = "Kiteboarding Weekend Forecast"
#     body = f"""
#     <h2>Silvaplana</h2>
#     <p>{silvaplana_forecast}</p>

#     <h2>Urnersee</h2>
#     <p>{urnersee_forecast}</p>
#     <p>Spot Description: {urnersee_description}</p>

#     <h2>Sempachersee</h2>
#     <p>{sempachersee_forecast}</p>

#     <h2>Thunersee</h2>
#     <p>{thunersee_forecast}</p>

#     <h2>General Wind Forecast for Switzerland</h2>
#     <p>{switzerland_wind_forecast}</p>
#     <p>Meteoschweiz Data: {meteoschweiz_data}</p>

#     <h2>Foehn Situation</h2>
#     <p><img src="{foehn_diagram}" alt="Foehn Diagram"></p>
#     """

#     # Send the email digest
#     send_email_digest(subject, body)

# # Call the function to generate and send the digest
# generate_digest()