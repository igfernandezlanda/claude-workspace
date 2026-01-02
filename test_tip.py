#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del generador
"""

from discord_travel_tips import DiscordTravelTipGenerator
import json

# Webhook proporcionado - Publicará en el hilo: 🇪🇸 Bilbao
THREAD_ID = "1393993178302120039"
WEBHOOK_URL = f"https://discord.com/api/webhooks/1456771590728585266/rFb-reKNtE874lAjsWZ3P6cShzuOYYLX2XbqEPnAqhVtcsPqi5Q-iNelJb1uG9yQ8KTC?thread_id={THREAD_ID}"

print("🧪 Prueba del Generador de Tips de Discord\n")
print("="*60)

# Inicializar generador
generator = DiscordTravelTipGenerator(webhook_url=WEBHOOK_URL)

# Crear un tip de ejemplo
print("\n📝 Generando tip de ejemplo...")
print("-"*60)

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
    rating=4.8,
    price="€€€",
    auto_search=False
)

# Mostrar el resultado
print("\n✅ Tip generado exitosamente!\n")
print("="*60)
print("PREVIEW DEL TIP:")
print("="*60)
print("\nContenido del mensaje:\n")
for embed in tip_data['embeds']:
    print(embed['description'])
    print(f"\nColor del embed: #{embed['color']:06X}")

print("\n" + "="*60)
print("\n📤 ¿Quieres publicar este tip en Discord? (s/n): ", end='')

import sys
try:
    response = input().strip().lower()
    if response.startswith('s'):
        print("\n⏳ Publicando en Discord...")
        if generator.post_to_discord(tip_data):
            print("✅ ¡Tip publicado exitosamente en tu canal de Discord!")
            print("\n💡 Verifica tu canal para ver el resultado")
        else:
            print("❌ Hubo un error al publicar")
    else:
        print("\n❌ Publicación cancelada. El tip no fue enviado a Discord.")
except KeyboardInterrupt:
    print("\n\n❌ Operación cancelada")
    sys.exit(0)

print("\n" + "="*60)
print("✅ Prueba completada")
print("="*60)
