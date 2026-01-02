# 📚 Guía para Principiantes - Discord Travel Tips

Esta guía te ayudará a descargar y usar el sistema de tips de viaje, **sin necesidad de experiencia previa**.

## 🎯 Paso 1: Instalar Python

### Windows:
1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descarga Python 3.11 o superior
3. **IMPORTANTE**: Durante la instalación, marca la casilla "Add Python to PATH"
4. Haz clic en "Install Now"
5. Cuando termine, abre "Símbolo del sistema" (CMD) y escribe:
   ```bash
   python --version
   ```
   Deberías ver algo como: `Python 3.11.x`

### Mac:
1. Abre "Terminal" (búscala en Spotlight)
2. Escribe:
   ```bash
   python3 --version
   ```
3. Si no está instalado, descárgalo de [python.org/downloads](https://www.python.org/downloads/)

### Linux:
Python ya viene instalado. Verifica con:
```bash
python3 --version
```

## 🎯 Paso 2: Descargar el Repositorio

Tienes **dos opciones** (escoge la más fácil para ti):

### Opción A: Descargar como ZIP (Más fácil)

1. Ve a GitHub: `https://github.com/igfernandezlanda/claude-workspace`
2. Haz clic en el botón verde **"Code"**
3. Selecciona **"Download ZIP"**
4. Descomprime el archivo en tu carpeta de Documentos
5. Renombra la carpeta a `discord-tips` (opcional, para que sea más fácil)

### Opción B: Usar Git (Recomendado si sabes usarlo)

1. Abre Terminal (Mac/Linux) o CMD (Windows)
2. Ve a tu carpeta de Documentos:
   ```bash
   # Windows
   cd %USERPROFILE%\Documents

   # Mac/Linux
   cd ~/Documents
   ```
3. Clona el repositorio:
   ```bash
   git clone https://github.com/igfernandezlanda/claude-workspace.git discord-tips
   ```

## 🎯 Paso 3: Abrir la Carpeta en Terminal

### Windows:
1. Abre "Explorador de archivos"
2. Navega a la carpeta donde descargaste el proyecto
3. En la barra de dirección (arriba), escribe `cmd` y presiona Enter
4. Se abrirá la terminal en esa carpeta

### Mac:
1. Abre "Finder"
2. Ve a la carpeta del proyecto
3. Click derecho → "Servicios" → "Nueva terminal en esta carpeta"

### Linux:
1. Abre tu gestor de archivos
2. Click derecho en la carpeta → "Abrir en terminal"

## 🎯 Paso 4: Instalar Dependencias

En la terminal que acabas de abrir, escribe:

```bash
# Windows
pip install requests

# Mac/Linux
pip3 install requests
```

Espera a que termine la instalación (unos segundos).

## 🎯 Paso 5: ¡Ejecutar el Script! 🎉

Ahora puedes ejecutar el script de tres formas:

### Forma 1: Prueba Rápida (Recomendado para empezar)

```bash
# Windows
python test_tip.py

# Mac/Linux
python3 test_tip.py
```

Esto te mostrará un ejemplo y te preguntará si quieres publicarlo.

### Forma 2: Modo Interactivo Completo

```bash
# Windows
python discord_travel_tips.py

# Mac/Linux
python3 discord_travel_tips.py
```

El script te hará preguntas paso a paso:
- ¿Qué ciudad?
- ¿Qué zona?
- ¿Nombre del lugar?
- etc.

### Forma 3: Ver Ejemplos

```bash
# Windows
python ejemplo_uso.py

# Mac/Linux
python3 ejemplo_uso.py
```

Te mostrará un menú con varios ejemplos listos.

## 📋 Ejemplo de Uso Completo

Cuando ejecutes `python discord_travel_tips.py`, verás algo así:

```
🌍 GENERADOR AUTOMATIZADO DE TIPS DE VIAJE PARA DISCORD
============================================================

📝 Información del lugar:
----------------------------------------
Ciudad: Madrid
Zona: Malasaña
Subsección: Centro
Nombre del lugar: Casa Labra

🏷️  Categorías disponibles:
  1. restaurantes
  2. cafes
  3. bares
  4. museos
  5. parques
  6. compras
  7. Otro

Selecciona categoría (1-7): 1

🔍 ¿Buscar información automáticamente? (s/n): n

📋 Información del tip:
----------------------------------------
Vibe/Ambiente: Taberna histórica desde 1860, auténtica madrileña
Specialty/Especialidad: Bacalao rebozado y croquetas caseras
Pro Tip: Pide en la barra y come de pie como un local

Rating (1.0-5.0, opcional): 4.5
Precio (€, €€, €€€, €€€€, opcional): €
Metro más cercano (opcional): Sol

¿Publicar en Discord? (s/n): s
```

## 🔧 Configuración Opcional: Google Places API

Si quieres que el script busque automáticamente ratings y precios, necesitas una API key:

### Paso a Paso:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Haz clic en "Nuevo Proyecto"
3. Ponle un nombre (ej: "Discord Tips")
4. Ve a "APIs y Servicios" → "Biblioteca"
5. Busca "Places API" y actívala
6. Ve a "Credenciales" → "Crear credenciales" → "Clave de API"
7. Copia la clave que te dan

### Configurar la API Key:

**Opción 1: Archivo .env** (Recomendado)
1. Abre el archivo `.env.example` con un editor de texto
2. Reemplaza `tu_api_key_aqui` con tu clave real
3. Guárdalo como `.env` (sin el .example)

**Opción 2: Variable de entorno**
```bash
# Windows (en CMD)
set GOOGLE_PLACES_API_KEY=tu_clave_aqui

# Mac/Linux
export GOOGLE_PLACES_API_KEY=tu_clave_aqui
```

## ❓ Preguntas Frecuentes

### ¿Qué hago si me da error "python no reconocido"?
- En Windows, usa `python` (sin el 3)
- En Mac/Linux, usa `python3` (con el 3)
- Si aún no funciona, reinstala Python marcando "Add to PATH"

### ¿Funciona sin la API de Google?
¡Sí! Puedes ingresar la información manualmente. La API solo automatiza la búsqueda de ratings y precios.

### ¿Cómo obtengo el webhook de Discord?
1. Ve a tu servidor de Discord
2. Click derecho en el canal donde quieres publicar
3. "Editar canal" → "Integraciones" → "Webhooks"
4. "Nuevo Webhook" → Copiar URL del webhook

### ¿Los emojis custom funcionarán?
Los emojis como `:Marcador1_v2:` deben estar configurados en tu servidor de Discord. Si no los tienes, se mostrarán como texto.

### ¿Puedo cambiar el webhook?
Sí, abre `discord_travel_tips.py` con un editor de texto y busca la línea:
```python
WEBHOOK_URL = "https://discord.com/api/webhooks/..."
```
Reemplaza la URL con la tuya.

## 🆘 ¿Necesitas Ayuda?

Si algo no funciona:

1. **Verifica que Python esté instalado**:
   ```bash
   python --version
   # o
   python3 --version
   ```

2. **Verifica que requests esté instalado**:
   ```bash
   pip show requests
   # o
   pip3 show requests
   ```

3. **Lee el mensaje de error** - usualmente te dice qué falta

4. **Abre un issue en GitHub** con el error que te aparece

## 🎉 ¡Listo!

Ahora solo ejecuta:
```bash
python discord_travel_tips.py
```

¡Y empieza a publicar tips de viaje en Discord! 🌍✨
