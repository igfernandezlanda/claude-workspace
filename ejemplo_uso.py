#!/usr/bin/env python3
"""
Ejemplo de uso programático del generador de tips de Discord
"""

from discord_travel_tips import DiscordTravelTipGenerator
import os

# Configuración - Publicará en el hilo: 🇪🇸 Bilbao
WEBHOOK_URL = "https://discord.com/api/webhooks/1456771590728585266/rFb-reKNtE874lAjsWZ3P6cShzuOYYLX2XbqEPnAqhVtcsPqi5Q-iNelJb1uG9yQ8KTC"
THREAD_ID = "1393993178302120039"

def ejemplo_restaurante():
    """Ejemplo: Publicar tip de un restaurante"""
    print("📍 Ejemplo: Restaurante en Madrid\n")

    generator = DiscordTravelTipGenerator(webhook_url=WEBHOOK_URL, thread_id=THREAD_ID)

    tip_data = generator.generate_tip(
        city="Madrid",
        zone="Malasaña",
        subsection="Centro",
        place_name="La Carmencita",
        category="restaurantes",
        vibe="Restaurante histórico con decoración belle époque y ambiente acogedor",
        specialty="Cocina española tradicional con toques modernos",
        pro_tip="Reserva con antelación, especialmente para cena los fines de semana",
        metro="Tribunal",
        rating=4.8,
        price="€€€",
        auto_search=False  # Usar datos manuales
    )

    # Previsualizar
    print("Preview del tip:")
    print("-" * 60)
    for embed in tip_data['embeds']:
        print(embed['description'])
    print("-" * 60)

    # Publicar
    confirm = input("\n¿Publicar en Discord? (s/n): ")
    if confirm.lower().startswith('s'):
        generator.post_to_discord(tip_data)


def ejemplo_cafe_con_busqueda():
    """Ejemplo: Café con búsqueda automática de información"""
    print("\n☕ Ejemplo: Café con búsqueda automática\n")

    # Asegurarse de tener la API key configurada
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("⚠️  Para este ejemplo necesitas configurar GOOGLE_PLACES_API_KEY")
        print("Saltando ejemplo...\n")
        return

    generator = DiscordTravelTipGenerator(
        webhook_url=WEBHOOK_URL,
        google_api_key=api_key,
        thread_id=THREAD_ID
    )

    tip_data = generator.generate_tip(
        city="Barcelona",
        zone="El Born",
        subsection="Centro",
        place_name="Els Quatre Gats",
        category="cafes",
        vibe="Café modernista histórico con arte en las paredes",
        specialty="Café artesanal y pasteles catalanes tradicionales",
        pro_tip="Visita en la mañana para evitar multitudes",
        metro="Jaume I",
        auto_search=True  # Buscará rating y precio automáticamente
    )

    # Publicar directamente
    generator.post_to_discord(tip_data)


def ejemplo_museo():
    """Ejemplo: Museo"""
    print("\n🏛️ Ejemplo: Museo\n")

    generator = DiscordTravelTipGenerator(webhook_url=WEBHOOK_URL, thread_id=THREAD_ID)

    tip_data = generator.generate_tip(
        city="Madrid",
        zone="Retiro",
        subsection="Paseo del Arte",
        place_name="Museo del Prado",
        category="museos",
        vibe="Impresionante colección de arte europeo de los siglos XII al XIX",
        specialty="Obras maestras de Velázquez, Goya y El Bosco",
        pro_tip="Compra entradas online y visita temprano para evitar filas",
        metro="Banco de España",
        rating=4.7,
        price="€€",
        auto_search=False
    )

    # Preview
    for embed in tip_data['embeds']:
        print(embed['description'])
    print()


def ejemplo_batch_tips():
    """Ejemplo: Publicar múltiples tips de una vez"""
    print("\n🔄 Ejemplo: Publicación en lote\n")

    generator = DiscordTravelTipGenerator(webhook_url=WEBHOOK_URL, thread_id=THREAD_ID)

    # Lista de tips para publicar
    tips = [
        {
            'city': 'Valencia',
            'zone': 'Ciutat Vella',
            'subsection': 'Centro Histórico',
            'place_name': 'Horchatería Santa Catalina',
            'category': 'cafes',
            'vibe': 'Horchatería tradicional valenciana desde 1836',
            'specialty': 'Horchata artesanal con fartons recién horneados',
            'pro_tip': 'Prueba la horchata bien fría en verano',
            'metro': 'Plaza de la Reina',
            'rating': 4.9,
            'price': '€'
        },
        {
            'city': 'Sevilla',
            'zone': 'Triana',
            'subsection': 'Junto al río',
            'place_name': 'Mercado de Triana',
            'category': 'compras',
            'vibe': 'Mercado tradicional con productos frescos y tapas locales',
            'specialty': 'Jamón ibérico, quesos y tapas de mercado',
            'pro_tip': 'Visita en la mañana y desayuna en uno de los bares',
            'metro': 'Plaza de Cuba',
            'rating': 4.6,
            'price': '€€'
        }
    ]

    for i, tip_info in enumerate(tips, 1):
        print(f"Publicando tip {i}/{len(tips)}: {tip_info['place_name']}")

        tip_data = generator.generate_tip(
            **tip_info,
            auto_search=False
        )

        # Pequeña pausa entre publicaciones para no saturar el webhook
        import time
        if i > 1:
            time.sleep(2)

        generator.post_to_discord(tip_data)

    print(f"\n✅ {len(tips)} tips publicados exitosamente!")


def main():
    """Menú principal de ejemplos"""
    print("\n" + "="*60)
    print("🌍 EJEMPLOS DE USO - Discord Travel Tips")
    print("="*60)

    ejemplos = {
        '1': ('Restaurante (datos manuales)', ejemplo_restaurante),
        '2': ('Café (búsqueda automática)', ejemplo_cafe_con_busqueda),
        '3': ('Museo', ejemplo_museo),
        '4': ('Publicación en lote', ejemplo_batch_tips),
    }

    print("\nEjemplos disponibles:")
    for key, (descripcion, _) in ejemplos.items():
        print(f"  {key}. {descripcion}")
    print("  5. Ejecutar todos")
    print("  0. Salir")

    opcion = input("\nSelecciona un ejemplo (0-5): ").strip()

    if opcion == '0':
        print("👋 ¡Hasta luego!")
        return
    elif opcion == '5':
        for _, (_, funcion) in ejemplos.items():
            try:
                funcion()
            except Exception as e:
                print(f"❌ Error: {e}")
        return
    elif opcion in ejemplos:
        _, funcion = ejemplos[opcion]
        try:
            funcion()
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ Opción inválida")


if __name__ == "__main__":
    main()
