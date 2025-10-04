#!/bin/bash

# Script de rulare pentru AutoClicker
echo "🖱️  Pornesc AutoClicker..."

# Verifică dacă Python este instalat
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nu este instalat. Te rog instalează Python3 mai întâi."
    exit 1
fi

# Verifică dacă pip este instalat
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 nu este instalat. Te rog instalează pip3 mai întâi."
    exit 1
fi

# Instalează dependențele dacă nu sunt instalate
echo "📦 Verific dependențele..."
pip3 install -r requirements.txt --quiet

# Verifică dacă instalarea a reușit
if [ $? -eq 0 ]; then
    echo "✅ Dependențele sunt instalate."
else
    echo "❌ Eroare la instalarea dependențelor."
    exit 1
fi

# Rulează aplicația
echo "🚀 Pornesc aplicația..."
python3 autoclicker.py

echo "👋 AutoClicker s-a închis."