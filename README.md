# 🌍 Discord Travel Tips - Sistema Automatizado

Sistema automatizado para publicar tips de viaje en Discord con búsqueda automática de información y formato estandarizado.

> 🆕 **¿Primera vez con Python o GitHub?** → Lee la [Guía para Principiantes](GUIA_PRINCIPIANTES.md) con instrucciones paso a paso.

## 🚀 Características

- ✅ **Búsqueda automática** de información (Google Places API)
- ✅ **Formato exacto** con emojis custom y separadores especiales
- ✅ **Validación automática** de límites de palabras
- ✅ **Sistema de estrellas** según ratings
- ✅ **Modo interactivo** fácil de usar
- ✅ **Publicación directa** a Discord vía webhook

## 📋 Requisitos

- Python 3.7+
- Cuenta de Discord con permisos de webhook
- Google Places API Key (opcional, para búsqueda automática)

## 🔧 Instalación

1. **Clonar el repositorio:**
```bash
git clone <url-del-repo>
cd claude-workspace
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar API Key (opcional):**
```bash
cp .env.example .env
# Editar .env y agregar tu Google Places API Key
```

Para obtener una API key de Google Places:
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto nuevo
3. Habilita "Places API"
4. Crea credenciales (API Key)
5. Copia la key a tu archivo `.env`

## 🎯 Uso

### Modo Interactivo (Recomendado)

```bash
python discord_travel_tips.py
```

El script te pedirá:
1. Ciudad, Zona, Subsección
2. Nombre del lugar
3. Categoría (restaurantes, cafés, bares, etc.)
4. Vibe, Specialty, Pro Tip
5. Información adicional (metro, etc.)

### Uso Programático

```python
from discord_travel_tips import DiscordTravelTipGenerator

# Inicializar
webhook_url = "https://discord.com/api/webhooks/..."
generator = DiscordTravelTipGenerator(webhook_url)

# Generar y publicar tip
tip_data = generator.generate_tip(
    city="Madrid",
    zone="Malasaña",
    subsection="Centro",
    place_name="La Carmencita",
    category="restaurantes",
    vibe="Restaurante histórico con decoración belle époque",
    specialty="Cocina española tradicional con toques modernos",
    pro_tip="Reserva con antelación los fines de semana",
    metro="Tribunal",
    auto_search=True  # Busca rating y precio automáticamente
)

# Publicar en Discord
generator.post_to_discord(tip_data)
```

## 📝 Formato del Tip

El sistema genera tips con el siguiente formato:

```
:Marcador1_v2: **Nombre del Lugar** ⭐️⭐️⭐️
―――
📍 Zona • Subsección
🚇 Metro
💰 €€€

✨ **Vibe:** Descripción del ambiente (≤15 palabras)
🍽️ **Specialty:** Especialidad del lugar (≤12 palabras)
💡 **Pro Tip:** Consejo profesional (≤20 palabras)
```

Ver [FORMATO_SKILL.md](FORMATO_SKILL.md) para detalles completos del formato.

## 🏷️ Categorías Disponibles

| Categoría | Emoji | Separador | Color |
|-----------|-------|-----------|-------|
| Restaurantes | :Marcador1_v2: | ――― | Rojo |
| Cafés | :Marcador2_v2: | ╭─╮ | Naranja |
| Bares | :Marcador3_v2: | ┌─┐ | Morado |
| Museos | :Marcador4_v2: | ═══ | Azul |
| Parques | :Marcador5_v2: | ─── | Verde |
| Compras | :Marcador6_v2: | ━━━ | Rosa |

## ⭐ Sistema de Estrellas

- **4.9-5.0**: ⭐️⭐️⭐️
- **4.7-4.8**: ⭐️⭐️
- **4.5-4.6**: ⭐️
- **< 4.5**: sin estrellas

## 🔒 Configuración de Discord

1. **Crear webhook:**
   - Ve a tu servidor de Discord
   - Configuración del canal → Integraciones → Webhooks
   - Crear webhook y copiar la URL

2. **Emojis custom:**
   - Los emojis `:Marcador1_v2:` a `:Marcador6_v2:` deben estar configurados en tu servidor
   - Si no existen, el script los mostrará como texto

## 🛠️ Solución de Problemas

### No se encuentra información automáticamente

- Verifica que tu Google Places API Key esté correctamente configurada
- Asegúrate de que Places API esté habilitada en Google Cloud Console
- Revisa que el nombre del lugar sea exacto

### Error al publicar en Discord

- Verifica que la URL del webhook sea correcta
- Asegúrate de que el webhook no haya sido eliminado
- Revisa los permisos del canal

### Límite de palabras excedido

- El script truncará automáticamente el texto
- Reescribe el contenido para que sea más conciso

## 📚 Documentación Adicional

- [Formato del Skill](FORMATO_SKILL.md) - Especificaciones detalladas del formato
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service) - Documentación oficial
- [Discord Webhooks](https://discord.com/developers/docs/resources/webhook) - Documentación de webhooks

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## ✨ Créditos

Sistema desarrollado para automatizar la publicación de tips de viaje con formato estandarizado.