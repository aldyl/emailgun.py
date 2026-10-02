# emailgun.py
Service to send mass emails to employees and customers.

## Configuracion

1. Copia `.env.example` a `.env` y rellena `EMAIL_SENDER` y `EMAIL_APP_PASSWORD`.
   Con Gmail necesitas una [contrasena de aplicacion](https://myaccount.google.com/apppasswords)
   (requiere verificacion en 2 pasos). `.env` esta en `.gitignore`: nunca lo subas.
2. Edita `empleado.csv` (columnas `name,email,message`).

## Uso

`pipenv run` carga `.env` automaticamente:

```sh
# Ver los correos sin enviarlos
pipenv run python simple_service/emailgun.py --dry-run

# Enviar
pipenv run python simple_service/emailgun.py --subject "Grupo Sigma"
```

Opciones: `--csv RUTA` para otro archivo de destinatarios, `--subject` para el asunto.
El script termina con codigo 1 si algun envio falla.
