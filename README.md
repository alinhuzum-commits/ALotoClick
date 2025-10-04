# AutoClicker

O aplicație simplă de autoclicker cu interfață grafică, creată în Python.

## Caracteristici

- ✨ Interfață grafică intuitivă
- ⏱️ Interval personalizabil între click-uri (de la 0.001 la 60 secunde)
- 🖱️ Suport pentru click stânga, dreapta sau mijloc
- 👆 Click-uri single sau double
- ⌨️ Hotkey personalizabil pentru pornire/oprire (implicit: 's')
- 🎯 Simplu de utilizat

## Cerințe

- Python 3.6 sau mai nou
- pip (managerul de pachete Python)

## Instalare

1. Clonați sau descărcați acest repository

2. Instalați dependențele necesare:
```bash
pip install -r requirements.txt
```

## Utilizare

1. Rulați aplicația:
```bash
python autoclicker.py
```

sau faceți fișierul executabil (Linux/Mac):
```bash
chmod +x autoclicker.py
./autoclicker.py
```

2. Configurați setările dorite:
   - **Click Interval**: Timpul între click-uri (în secunde)
   - **Mouse Button**: Selectați butonul mouse-ului (Stânga/Dreapta/Mijloc)
   - **Click Type**: Single click sau double click
   - **Toggle Hotkey**: Tasta pentru pornire/oprire (implicit 's')

3. Apăsați butonul "Start" sau tasta hotkey pentru a porni autoclicker-ul

4. Apăsați din nou pentru a opri

## Comenzi rapide

- Apăsați tasta hotkey (implicit **'s'**) pentru a porni/opri autoclicker-ul
- Închideți fereastra pentru a ieși din aplicație

## Note importante

⚠️ **Atenție**: Utilizați această aplicație în mod responsabil. Unele jocuri și aplicații pot detecta și interzice utilizarea autoclicker-elor.

## Funcționare tehnică

Aplicația folosește:
- `tkinter` pentru interfața grafică
- `pynput` pentru controlul mouse-ului și detectarea tastelor
- `threading` pentru a rula click-urile în background

## Troubleshooting

### Linux
Dacă întâmpinați probleme pe Linux, ar putea fi necesar să instalați dependențe suplimentare:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk python3-dev

# Fedora
sudo dnf install python3-tkinter
```

### MacOS
Pe MacOS, va fi necesar să acordați permisiuni de accesibilitate pentru aplicație în System Preferences → Security & Privacy → Privacy → Accessibility.

### Windows
Pe Windows, ar putea fi necesar să rulați aplicația ca administrator pentru unele funcții.

## Licență

Acest proiect este open source și disponibil pentru uz personal.
