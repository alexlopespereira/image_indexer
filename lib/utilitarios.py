# coding=utf-8
import os
import getpass
import re
import sys
import subprocess
import datetime
import string
import smtplib
import commands
from email.MIMEText import MIMEText

arquivo_log = ''

def coletar_informacoes_locais():

    IP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1]
    remov = re.sub('(?:[0-9]{1,3}\.){3}[0-9]{1,3}$','',IP)
    IP = string.replace(IP,remov,'')
    OS = commands.getoutput("/bin/uname -a")
    USUARIO = getpass.getuser()
    LOGIN = os.getlogin()

    return {'ip':IP, 'os':OS, 'usuario':USUARIO, 'login':LOGIN}



def logar(arquivo, valor):
    with open(arquivo, "a") as file:
        file.write(datetime.datetime.now().strftime("%Y-%m-%d(%H:%M:%S)") + " - " +valor + "\n")

def enviar_log(anexo):

    msg = MIMEText(file(anexo).read(), 'plain', 'utf-8')
    msg['Subject'] = "Indexador Imagens - %s" % Servidor

    try:
        server = smtplib.SMTP('smtp.sipam.gov.br', 587)
        server.starttls()
        server.sendmail(email_operador, email_admin, msg.as_string())
        return "OK"
    except smtplib.SMTPRecipientsRefused as e:
        return "ERRO AO ENVIAR LOG: %s" % str(e.recipients)
    except smtplib.SMTPException as e:
        return "ERRO AO ENVIAR LOG: %s" % e.smtp_error
