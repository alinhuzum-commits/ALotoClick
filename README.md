# 🖱️ AutoClicker

O aplicație simplă și eficientă de autoclicker pentru automatizarea click-urilor de mouse, dezvoltată în Python cu interfață grafică.

## ✨ Caracteristici

- **Interfață grafică intuitivă** - Ușor de utilizat pentru oricine
- **Selectare poziție precisă** - Click pe locul exact unde vrei să se facă click-urile
- **Control complet al intervalului** - De la 0.1 la 10 secunde între click-uri
- **Tipuri multiple de click** - Click stânga, dreapta sau mijloc
- **Număr configurable de click-uri** - Setează un număr fix sau lasă infinit
- **Hotkey-uri globale** - Control rapid cu F1 și ESC
- **Statistici în timp real** - Vezi câte click-uri au fost efectuate
- **Oprire de siguranță** - Apasă ESC oricând pentru a opri

## 🚀 Instalare și Rulare

### Cerințe de sistem
- Python 3.6 sau mai nou
- Linux/Windows/macOS

### Pași de instalare

1. **Clonează sau descarcă proiectul**
   ```bash
   git clone <repository-url>
   cd autoclicker
   ```

2. **Instalează dependențele**
   ```bash
   pip install -r requirements.txt
   ```

3. **Rulează aplicația**
   ```bash
   python autoclicker.py
   ```

### Instalare rapidă cu script
```bash
chmod +x run.sh
./run.sh
```

## 📖 Cum să folosești

1. **Pornește aplicația** - Rulează `python autoclicker.py`

2. **Selectează poziția**
   - Apasă butonul "📍 Selectează Poziția"
   - Click pe locul unde vrei să se facă click-urile automate
   - Coordonatele vor fi afișate în aplicație

3. **Configurează setările**
   - **Interval**: Setează timpul între click-uri (0.1 - 10 secunde)
   - **Numărul de click-uri**: 0 pentru infinit, sau un număr specific
   - **Tipul de click**: Alege între click stânga, dreapta sau mijloc

4. **Controlează aplicația**
   - **▶️ Start**: Începe click-urile automate
   - **⏹️ Stop**: Oprește click-urile
   - **ESC**: Oprire rapidă din orice loc
   - **F1**: Start/Stop rapid

## ⌨️ Hotkey-uri

- **ESC** - Oprește click-urile automate
- **F1** - Comută între start și stop

## 🛡️ Siguranță

- Aplicația poate fi oprită oricând cu ESC
- Nu modifică sistemul sau fișierele
- Funcționează doar când este activă
- Nu colectează sau transmite date

## 🔧 Tehnologii folosite

- **Python 3** - Limbajul de programare principal
- **Tkinter** - Interfața grafică
- **pynput** - Control mouse și tastatură
- **threading** - Procesare în background

## 📝 Licență

Acest proiect este open source și poate fi folosit liber pentru scopuri personale și educaționale.

## 🐛 Raportare probleme

Dacă întâmpini probleme:
1. Verifică că ai instalat toate dependențele
2. Asigură-te că ai permisiuni pentru controlul mouse-ului
3. Pe Linux, s-ar putea să ai nevoie de permisiuni suplimentare

## 🤝 Contribuții

Contribuțiile sunt binevenite! Simte-te liber să:
- Raportezi bug-uri
- Sugerezi funcționalități noi
- Îmbunătățești codul
- Traduci în alte limbi

---

**⚠️ Notă**: Folosește această aplicație responsabil și respectă termenii de utilizare ai aplicațiilor și site-urilor pe care le folosești.