#!/usr/bin/env python3
"""
Sistema automatizado para publicar tips de viaje en Discord
Busca información automáticamente y la publica con formato específico
"""

import os
import sys
import json
import requests
from typing import Dict, Optional, Tuple
import re


class DiscordTravelTipGenerator:
    """Generador automatizado de tips de viaje para Discord"""

    # Mapeo de categorías a emojis y separadores
    CATEGORY_CONFIG = {
        'restaurantes': {
            'emoji': ':Marcador1_v2:',
            'separator': '―――',
            'color': 0xE74C3C  # Rojo
        },
        'cafes': {
            'emoji': ':Marcador2_v2:',
            'separator': '╭─╮',
            'color': 0xF39C12  # Naranja
        },
        'bares': {
            'emoji': ':Marcador3_v2:',
            'separator': '┌─┐',
            'color': 0x9B59B6  # Morado
        },
        'museos': {
            'emoji': ':Marcador4_v2:',
            'separator': '═══',
            'color': 0x3498DB  # Azul
        },
        'parques': {
            'emoji': ':Marcador5_v2:',
            'separator': '───',
            'color': 0x2ECC71  # Verde
        },
        'compras': {
            'emoji': ':Marcador6_v2:',
            'separator': '━━━',
            'color': 0xE91E63  # Rosa
        }
    }

    def __init__(self, webhook_url: str, google_api_key: Optional[str] = None):
        """
        Inicializa el generador

        Args:
            webhook_url: URL del webhook de Discord
            google_api_key: API key de Google Places (opcional)
        """
        self.webhook_url = webhook_url
        self.google_api_key = google_api_key or os.getenv('GOOGLE_PLACES_API_KEY')

    def get_stars(self, rating: float) -> str:
        """
        Convierte rating numérico a estrellas según el sistema especificado

        Args:
            rating: Rating del 1.0 al 5.0

        Returns:
            String con estrellas correspondientes
        """
        if rating >= 4.9:
            return '⭐️⭐️⭐️'
        elif rating >= 4.7:
            return '⭐️⭐️'
        elif rating >= 4.5:
            return '⭐️'
        else:
            return ''

    def get_price_level(self, price_level: Optional[int]) -> str:
        """
        Convierte price_level de Google a símbolos €

        Args:
            price_level: Nivel de precio (1-4) de Google Places

        Returns:
            String con símbolos € correspondientes
        """
        if price_level is None:
            return '€€'

        price_symbols = {
            1: '€',
            2: '€€',
            3: '€€€',
            4: '€€€€'
        }
        return price_symbols.get(price_level, '€€')

    def search_place_info(self, place_name: str, city: str) -> Optional[Dict]:
        """
        Busca información del lugar usando Google Places API

        Args:
            place_name: Nombre del lugar
            city: Ciudad donde se encuentra

        Returns:
            Diccionario con información del lugar o None si no se encuentra
        """
        if not self.google_api_key:
            print("⚠️  No se configuró Google Places API Key. Usando modo manual.")
            return None

        try:
            # Búsqueda de texto en Google Places
            search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            params = {
                'input': f"{place_name} {city}",
                'inputtype': 'textquery',
                'fields': 'place_id,name,formatted_address,rating,price_level',
                'key': self.google_api_key
            }

            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('status') != 'OK' or not data.get('candidates'):
                print(f"⚠️  No se encontró información para '{place_name}' en {city}")
                return None

            place_id = data['candidates'][0]['place_id']

            # Obtener detalles del lugar
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,rating,price_level,formatted_address,types,user_ratings_total',
                'key': self.google_api_key
            }

            response = requests.get(details_url, params=params)
            response.raise_for_status()
            details = response.json()

            if details.get('status') == 'OK':
                return details['result']

            return None

        except Exception as e:
            print(f"❌ Error al buscar información: {e}")
            return None

    def validate_word_count(self, text: str, max_words: int, field_name: str) -> bool:
        """
        Valida que el texto no exceda el límite de palabras

        Args:
            text: Texto a validar
            max_words: Máximo de palabras permitidas
            field_name: Nombre del campo (para mensajes de error)

        Returns:
            True si es válido, False si excede el límite
        """
        word_count = len(text.split())
        if word_count > max_words:
            print(f"⚠️  {field_name} excede el límite de {max_words} palabras ({word_count} palabras)")
            return False
        return True

    def truncate_to_words(self, text: str, max_words: int) -> str:
        """
        Trunca el texto al número máximo de palabras

        Args:
            text: Texto a truncar
            max_words: Máximo de palabras

        Returns:
            Texto truncado
        """
        words = text.split()
        if len(words) > max_words:
            return ' '.join(words[:max_words]) + '...'
        return text

    def generate_tip(self,
                     city: str,
                     zone: str,
                     subsection: str,
                     place_name: str,
                     category: str,
                     vibe: str,
                     specialty: str,
                     pro_tip: str,
                     rating: Optional[float] = None,
                     price: Optional[str] = None,
                     metro: Optional[str] = None,
                     auto_search: bool = True) -> Dict:
        """
        Genera el tip con el formato exacto especificado

        Args:
            city: Ciudad
            zone: Zona de la ciudad
            subsection: Subsección específica
            place_name: Nombre del lugar
            category: Categoría del lugar
            vibe: Descripción del ambiente (≤15 palabras)
            specialty: Especialidad del lugar (≤12 palabras)
            pro_tip: Consejo profesional (≤20 palabras)
            rating: Rating del lugar (opcional, se busca automáticamente)
            price: Nivel de precio (opcional, se busca automáticamente)
            metro: Estación de metro más cercana (opcional)
            auto_search: Si True, busca información automáticamente

        Returns:
            Diccionario con el contenido formateado para Discord
        """
        # Buscar información automáticamente si está habilitado
        if auto_search and rating is None:
            place_info = self.search_place_info(place_name, city)
            if place_info:
                rating = place_info.get('rating')
                price_level = place_info.get('price_level')
                if price is None and price_level:
                    price = self.get_price_level(price_level)
                print(f"✅ Información encontrada: Rating {rating}, Precio {price}")

        # Validar límites de palabras
        self.validate_word_count(vibe, 15, "Vibe")
        self.validate_word_count(specialty, 12, "Specialty")
        self.validate_word_count(pro_tip, 20, "Pro Tip")

        # Truncar si excede los límites
        vibe = self.truncate_to_words(vibe, 15)
        specialty = self.truncate_to_words(specialty, 12)
        pro_tip = self.truncate_to_words(pro_tip, 20)

        # Obtener configuración de la categoría
        category_lower = category.lower()
        config = self.CATEGORY_CONFIG.get(category_lower, {
            'emoji': ':Marcador1_v2:',
            'separator': '―――',
            'color': 0x95A5A6
        })

        # Construir el mensaje
        stars = self.get_stars(rating) if rating else ''
        price_str = price or '€€'

        # Formato exacto del tip
        separator = config['separator']
        emoji = config['emoji']

        # Construir las líneas del mensaje
        lines = [
            f"{emoji} **{place_name}** {stars}",
            f"{separator}",
            f"📍 {zone} • {subsection}",
        ]

        # Agregar metro si está disponible
        if metro:
            lines.append(f"🚇 {metro}")

        lines.extend([
            f"💰 {price_str}",
            f"",
            f"✨ **Vibe:** {vibe}",
            f"🍽️ **Specialty:** {specialty}",
            f"💡 **Pro Tip:** {pro_tip}"
        ])

        content = '\n'.join(lines)

        return {
            'embeds': [{
                'description': content,
                'color': config['color']
            }]
        }

    def post_to_discord(self, tip_data: Dict) -> bool:
        """
        Publica el tip en Discord vía webhook

        Args:
            tip_data: Datos del tip generado

        Returns:
            True si se publicó correctamente, False en caso contrario
        """
        try:
            response = requests.post(
                self.webhook_url,
                json=tip_data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            print("✅ Tip publicado exitosamente en Discord!")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Error al publicar en Discord: {e}")
            if hasattr(e.response, 'text'):
                print(f"Respuesta: {e.response.text}")
            return False

    def interactive_mode(self):
        """Modo interactivo para crear y publicar tips"""
        print("\n" + "="*60)
        print("🌍 GENERADOR AUTOMATIZADO DE TIPS DE VIAJE PARA DISCORD")
        print("="*60 + "\n")

        # Solicitar información básica
        print("📝 Información del lugar:")
        print("-" * 40)
        city = input("Ciudad: ").strip()
        zone = input("Zona: ").strip()
        subsection = input("Subsección: ").strip()
        place_name = input("Nombre del lugar: ").strip()

        print("\n🏷️  Categorías disponibles:")
        for i, cat in enumerate(self.CATEGORY_CONFIG.keys(), 1):
            print(f"  {i}. {cat.capitalize()}")
        print("  7. Otro")

        category_choice = input("\nSelecciona categoría (1-7): ").strip()
        category_map = {str(i): cat for i, cat in enumerate(self.CATEGORY_CONFIG.keys(), 1)}
        category = category_map.get(category_choice, 'restaurantes')

        # Preguntar si quiere búsqueda automática
        auto_search = input("\n🔍 ¿Buscar información automáticamente? (s/n): ").lower().startswith('s')

        # Información manual
        print("\n📋 Información del tip:")
        print("-" * 40)
        print("(Límites: Vibe ≤15 palabras, Specialty ≤12 palabras, Pro Tip ≤20 palabras)")
        vibe = input("Vibe/Ambiente: ").strip()
        specialty = input("Specialty/Especialidad: ").strip()
        pro_tip = input("Pro Tip: ").strip()

        # Información adicional (opcional si no hay auto-búsqueda)
        rating = None
        price = None
        metro = None

        if not auto_search:
            rating_input = input("\nRating (1.0-5.0, opcional): ").strip()
            if rating_input:
                try:
                    rating = float(rating_input)
                except ValueError:
                    print("⚠️  Rating inválido, se omitirá")

            price = input("Precio (€, €€, €€€, €€€€, opcional): ").strip() or None

        metro = input("Metro más cercano (opcional): ").strip() or None

        # Generar el tip
        print("\n⏳ Generando tip...")
        tip_data = self.generate_tip(
            city=city,
            zone=zone,
            subsection=subsection,
            place_name=place_name,
            category=category,
            vibe=vibe,
            specialty=specialty,
            pro_tip=pro_tip,
            rating=rating,
            price=price,
            metro=metro,
            auto_search=auto_search
        )

        # Mostrar preview
        print("\n" + "="*60)
        print("📋 PREVIEW DEL TIP:")
        print("="*60)
        print(json.dumps(tip_data, indent=2, ensure_ascii=False))
        print("="*60)

        # Confirmar publicación
        confirm = input("\n¿Publicar en Discord? (s/n): ").lower().startswith('s')

        if confirm:
            self.post_to_discord(tip_data)
        else:
            print("❌ Publicación cancelada")


def main():
    """Función principal"""
    # Webhook de Discord proporcionado
    # Publicará en el hilo: 🇪🇸 Bilbao
    THREAD_ID = "1393993178302120039"
    WEBHOOK_URL = f"https://discord.com/api/webhooks/1456771590728585266/rFb-reKNtE874lAjsWZ3P6cShzuOYYLX2XbqEPnAqhVtcsPqi5Q-iNelJb1uG9yQ8KTC?thread_id={THREAD_ID}"

    # Inicializar generador
    generator = DiscordTravelTipGenerator(
        webhook_url=WEBHOOK_URL,
        google_api_key=os.getenv('GOOGLE_PLACES_API_KEY')
    )

    # Verificar si hay API key configurada
    if not generator.google_api_key:
        print("\n⚠️  AVISO: No se detectó Google Places API Key")
        print("Para habilitar búsqueda automática, configura:")
        print("  export GOOGLE_PLACES_API_KEY='tu_api_key'")
        print("\nSe continuará en modo manual.\n")

    # Modo interactivo
    try:
        generator.interactive_mode()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
        sys.exit(0)


if __name__ == "__main__":
    main()
