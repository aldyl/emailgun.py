#!/bin/python3
# -*- coding: utf-8 -*-

from keys.secret import sender, sender_key

import pandas as pd
df = pd.read_csv('empleado.csv')
emails = df['email']

import smtplib
from email.mime.text import MIMEText

servidor = smtplib.SMTP('smtp.gmail.com', 587)
servidor.starttls()
servidor.login(sender, sender_key)

# Mensaje a enviar con MIMEtext
mensaje = MIMEText('La administracion les desea buen fin de semana')
mensaje['From'] = sender
mensaje['Subject'] = 'Grupo Sigma'
mensaje['To'] = 'aldy.leongarcia@gmail.com'



# Envio del mensaje
servidor.sendmail(mensaje['From'], mensaje['To'], mensaje.as_string())

