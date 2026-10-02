#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Envia un correo personalizado a cada empleado listado en un CSV.

Las credenciales se leen de las variables de entorno EMAIL_SENDER y
EMAIL_APP_PASSWORD (ver .env.example). El CSV debe tener las columnas
name, email y message.
"""

import argparse
import csv
import os
import smtplib
import sys
from email.mime.text import MIMEText
from pathlib import Path

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
DEFAULT_CSV = Path(__file__).resolve().parent.parent / "empleado.csv"
DEFAULT_SUBJECT = "Grupo Sigma"


def leer_destinatarios(ruta):
    """Devuelve las filas del CSV con los valores sin espacios sobrantes."""
    with open(ruta, newline="", encoding="utf-8") as f:
        return [
            {clave.strip(): (valor or "").strip() for clave, valor in fila.items()}
            for fila in csv.DictReader(f, skipinitialspace=True)
        ]


def crear_mensaje(remitente, destinatario, asunto):
    # Mensaje a enviar con MIMEText
    cuerpo = f"Hola {destinatario['name']},\n\n{destinatario['message']}"
    mensaje = MIMEText(cuerpo, "plain", "utf-8")
    mensaje["From"] = remitente
    mensaje["To"] = destinatario["email"]
    mensaje["Subject"] = asunto
    return mensaje


def obtener_credenciales():
    remitente = os.environ.get("EMAIL_SENDER")
    clave = os.environ.get("EMAIL_APP_PASSWORD")
    if not remitente or not clave:
        sys.exit("Faltan las variables de entorno EMAIL_SENDER y/o EMAIL_APP_PASSWORD.")
    return remitente, clave


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="archivo CSV de destinatarios")
    parser.add_argument("--subject", default=DEFAULT_SUBJECT, help="asunto del correo")
    parser.add_argument("--dry-run", action="store_true", help="muestra los correos sin enviarlos")
    args = parser.parse_args()

    destinatarios = [d for d in leer_destinatarios(args.csv) if d.get("email")]
    if not destinatarios:
        sys.exit(f"No hay destinatarios con email en {args.csv}.")

    if args.dry_run:
        remitente = os.environ.get("EMAIL_SENDER", "remitente@example.com")
        for destinatario in destinatarios:
            mensaje = crear_mensaje(remitente, destinatario, args.subject)
            cuerpo = mensaje.get_payload(decode=True).decode("utf-8")
            print(f"Para: {mensaje['To']}\nAsunto: {mensaje['Subject']}\n\n{cuerpo}\n{'-' * 40}")
        print(f"[dry-run] {len(destinatarios)} correos preparados, ninguno enviado.")
        return

    remitente, clave = obtener_credenciales()
    fallidos = []
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as servidor:
            servidor.starttls()
            servidor.login(remitente, clave)

            # Envio de un mensaje por destinatario
            for destinatario in destinatarios:
                mensaje = crear_mensaje(remitente, destinatario, args.subject)
                try:
                    servidor.send_message(mensaje)
                    print(f"OK    {destinatario['email']}")
                except smtplib.SMTPException as error:
                    fallidos.append(destinatario["email"])
                    print(f"ERROR {destinatario['email']}: {error}", file=sys.stderr)
    except smtplib.SMTPAuthenticationError:
        sys.exit("Error de autenticacion: revisa EMAIL_SENDER y EMAIL_APP_PASSWORD.")
    except (smtplib.SMTPException, OSError) as error:
        sys.exit(f"Error de conexion con {SMTP_HOST}:{SMTP_PORT}: {error}")

    enviados = len(destinatarios) - len(fallidos)
    print(f"Enviados: {enviados}/{len(destinatarios)}")
    if fallidos:
        sys.exit(1)


if __name__ == "__main__":
    main()
