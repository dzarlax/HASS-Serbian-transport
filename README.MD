
# Serbian Transport Integration

![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)
![HACS](https://img.shields.io/badge/HACS-compatible-orange.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1.0+-green.svg)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dzarlax&repository=HASS-Serbian-transport&category=integration)

Advanced Home Assistant integration for Serbian public transport with real-time arrivals, beautiful animations, and visual configuration.

## ✨ Features

### Core Features
- 🚌 **Real-time transport arrivals** - Live data from official transport APIs
- 📍 **Coordinate-based discovery** - Automatically finds nearby stops using your coordinates
- 🎨 **Modern visual interface** - Beautiful animations, color-coded arrivals, progress bars
- ⚙️ **Visual configuration** - Easy setup through Home Assistant UI (no YAML required)
- 📱 **Responsive design** - Works perfectly on mobile and desktop

### Advanced Features
- 🎯 **Next departure highlighting** - Shows the soonest arrival across all stops
- 📊 **Progress bars** - Visual time indicators with color coding
- 🔄 **Expandable view** - Compact/expanded modes for different use cases
- 🎭 **Smooth animations** - Hover effects and transitions for modern UX
- 🔧 **Migration support** - Seamless updates from older versions

## 🏙️ Supported Cities
- **Belgrade** (GSP Belgrade)
- **Novi Sad** (JGSP Novi Sad) 
- **Niš** (JKP Direkcija za javni prevoz grada Niša)

## 📦 Installation

### One-Click Installation (Easiest)
Click the button below to automatically open HACS and install the integration:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dzarlax&repository=HASS-Serbian-transport&category=integration)

After installation, add the integration to your Home Assistant:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=serbian_transport)

### Via HACS (Manual)
1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click "Explore & Download Repositories"
4. Search for "Serbian Transport"
5. Download and install
6. Restart Home Assistant
7. Add integration: **Settings** → **Devices & Services** → **Add Integration** → **Serbian Transport**

### Manual Installation
1. Copy the `serbian_transport` folder to your `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the UI

## 🎛️ Configuration

### Integration Setup
1. **Settings** → **Devices & Services** → **Add Integration**
2. Search for "Serbian Transport"
3. Enter your coordinates (or use Home Assistant defaults)
4. Set search radius (100-20000 meters)
5. Save configuration

### Card Configuration

#### Visual UI Configuration (Recommended)
1. Add card to dashboard
2. Choose **"Serbian Transport Card"** from the list
3. Configure using the visual editor:
   - **Entity**: Select your transport sensor
   - **Title**: Custom card title
   - **Max Stations**: Number of stations to display (1-50)
   - **Show Next Departure**: Toggle next departure section
   - **Compact View**: Default view mode
   - **Refresh Interval**: Data update frequency (10-300 seconds)

#### YAML Configuration (Advanced)
```yaml
type: custom:transport-card
entity: sensor.serbian_transport_stations_count
title: "Serbian Transport"
show_next_departure: true
compact_view: false
max_stations: 10
refresh_interval: 30
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entity` | string | **required** | Transport sensor entity ID |
| `title` | string | `"Serbian Transport"` | Card title |
| `show_next_departure` | boolean | `true` | Show next departure section |
| `compact_view` | boolean | `false` | Use compact layout by default |
| `max_stations` | number | `10` | Maximum stations to display (1-50) |
| `refresh_interval` | number | `30` | Update interval in seconds (10-300) |

## 🎨 Visual Features

### Color-Coded Arrivals
- 🔴 **Urgent** (≤2 min) - Red gradient
- 🟠 **Soon** (≤5 min) - Orange gradient  
- 🟢 **Normal** (≤15 min) - Green gradient
- 🔵 **Late** (>15 min) - Blue gradient

### Interactive Elements
- **Hover effects** on transport groups
- **Expandable/collapsible** view with animation
- **Progress bars** showing time until arrival
- **Status indicators** for station data availability

## 🔧 Troubleshooting

### Card Not Appearing
The card should be automatically registered. If it doesn't appear:

1. **Settings** → **Dashboards** → **Resources**
2. Add new resource: `/hacsfiles/HASS-Serbian-transport/transport-card.js`
3. Type: **JavaScript Module**
4. Refresh browser (Ctrl+F5)

### No Data Showing
- Check if coordinates are correct
- Verify search radius (try increasing it)
- Ensure internet connectivity
- Check Home Assistant logs for errors

### Migration Issues
If upgrading from an older version:
- The integration automatically migrates old configurations
- Clear browser cache if the card doesn't update
- Check entity names (might have changed)

## 🏗️ Development

This integration is part of the [City Dashboard](https://github.com/dzarlax/city-dashboard) project.

### API Endpoints
- **Production**: `https://transport-api.dzarlax.dev`
- **Fallback cities**: Belgrade (`bg`), Novi Sad (`ns`), Niš (`nis`)

### Version History
- **v2.2.0**: Simplified interface, removed complex filtering
- **v2.1.x**: Advanced features with sorting and favorites
- **v2.0.0**: Major rewrite with visual configuration
- **v1.x**: Initial release with basic functionality


# Srpski Transport Integracija

![Verzija](https://img.shields.io/badge/verzija-2.2.0-blue.svg)
![HACS](https://img.shields.io/badge/HACS-kompatibilna-orange.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1.0+-green.svg)

[![Otvorite vašu Home Assistant instancu i dodajte repozitorijum u Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dzarlax&repository=HASS-Serbian-transport&category=integration)

Napredna Home Assistant integracija za srpski javni prevoz sa dolaskom u realnom vremenu, lepim animacijama i vizuelnom konfiguracijom.

## ✨ Funkcije

### Osnovne funkcije
- 🚌 **Dolasci prevoza u realnom vremenu** - Živi podaci sa zvaničnih transport API-ja
- 📍 **Otkrivanje bazirano na koordinatama** - Automatski pronalazi obližnje stanice koristeći vaše koordinate
- 🎨 **Moderan vizuelni interfejs** - Lepe animacije, dolasci u boji, trake napretka
- ⚙️ **Vizuelna konfiguracija** - Lako podešavanje kroz Home Assistant UI (YAML nije potreban)
- 📱 **Responsive dizajn** - Savršeno radi na mobilnim uređajima i desktopima

### Napredne funkcije  
- 🎯 **Označavanje sledećeg polaska** - Prikazuje najraniji dolazak preko svih stanica
- 📊 **Trake napretka** - Vizuelni indikatori vremena sa kodiranjem u boji
- 🔄 **Proširiv prikaz** - Kompaktni/prošireni režimi za različite slučajeve korišćenja
- 🎭 **Glatke animacije** - Hover efekti i prelazi za moderan UX
- 🔧 **Podrška za migraciju** - Besprekorne nadogradnje sa starijih verzija

## 🏙️ Podržani gradovi
- **Beograd** (GSP Beograd)
- **Novi Sad** (JGSP Novi Sad)
- **Niš** (JKP Direkcija za javni prevoz grada Niša)

## 📦 Instalacija

### Instalacija jednim klikom (Najlakše)
Kliknite dugme ispod da automatski otvorite HACS i instalirate integraciju:

[![Otvorite vašu Home Assistant instancu i dodajte repozitorijum u Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dzarlax&repository=HASS-Serbian-transport&category=integration)

Nakon instalacije, dodajte integraciju u vaš Home Assistant:

[![Otvorite vašu Home Assistant instancu i počnite podešavanje nove integracije.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=serbian_transport)

### Preko HACS-a (Ručno)
1. Otvorite HACS u Home Assistant-u
2. Idite na "Integracije"
3. Kliknite "Istražite i preuzmite repozitorijume"
4. Tražite "Serbian Transport"
5. Preuzmite i instalirajte
6. Restartujte Home Assistant
7. Dodajte integraciju: **Podešavanja** → **Uređaji i Servisi** → **Dodaj Integraciju** → **Serbian Transport**

### Ručna instalacija
1. Kopirajte `serbian_transport` folder u vaš `custom_components` direktorijum
2. Restartujte Home Assistant
3. Dodajte integraciju preko UI-ja

## 🎛️ Konfiguracija

### Podešavanje integracije
1. **Podešavanja** → **Uređaji i Servisi** → **Dodaj Integraciju**
2. Tražite "Serbian Transport"
3. Unesite vaše koordinate (ili koristite Home Assistant podrazumevane)
4. Postavite radijus pretrage (100-20000 metara)
5. Sačuvajte konfiguraciju

### Konfiguracija kartice

#### Vizuelna UI konfiguracija (Preporučeno)
1. Dodajte karticu na kontrolnu tablu
2. Izaberite **"Serbian Transport Card"** sa liste
3. Konfigurišite koristeći vizuelni editor:
   - **Entity**: Izaberite vaš transport senzor
   - **Title**: Prilagođeni naslov kartice
   - **Max Stations**: Broj stanica za prikaz (1-50)
   - **Show Next Departure**: Uključi/isključi sekciju sledećeg polaska
   - **Compact View**: Podrazumevani režim prikaza
   - **Refresh Interval**: Frekvencija ažuriranja podataka (10-300 sekundi)

#### YAML konfiguracija (Napredna)
```yaml
type: custom:transport-card
entity: sensor.serbian_transport_stations_count
title: "Serbian Transport"
show_next_departure: true
compact_view: false
max_stations: 10
refresh_interval: 30
```

### Opcije konfiguracije

| Opcija | Tip | Podrazumevano | Opis |
|--------|-----|---------------|------|
| `entity` | string | **obavezno** | ID transport senzor entiteta |
| `title` | string | `"Serbian Transport"` | Naslov kartice |
| `show_next_departure` | boolean | `true` | Prikaži sekciju sledećeg polaska |
| `compact_view` | boolean | `false` | Koristi kompaktni layout po default-u |
| `max_stations` | number | `10` | Maksimalno stanica za prikaz (1-50) |
| `refresh_interval` | number | `30` | Interval ažuriranja u sekundama (10-300) |

## 🎨 Vizuelne funkcije

### Dolasci označeni bojama
- 🔴 **Hitno** (≤2 min) - Crveni gradijent
- 🟠 **Uskoro** (≤5 min) - Narandžasti gradijent
- 🟢 **Normalno** (≤15 min) - Zeleni gradijent
- 🔵 **Kasno** (>15 min) - Plavi gradijent

### Interaktivni elementi
- **Hover efekti** na transport grupama
- **Proširiv/sklopiv** prikaz sa animacijom
- **Trake napretka** koje prikazuju vreme do dolaska
- **Status indikatori** za dostupnost podataka stanice

## 🔧 Rešavanje problema

### Kartica se ne pojavljuje
Kartica treba da bude automatski registrovana. Ako se ne pojavljuje:

1. **Podešavanja** → **Kontrolne table** → **Resursi**
2. Dodajte novi resurs: `/hacsfiles/HASS-Serbian-transport/transport-card.js`
3. Tip: **JavaScript Module**
4. Osvežite browser (Ctrl+F5)

### Nema podataka
- Proverite da li su koordinate ispravne
- Proverite radijus pretrage (pokušajte da ga povećate)
- Obezbedite internet konekciju
- Proverite Home Assistant logove za greške

### Problemi sa migracijom
Ako nadograđujete sa starije verzije:
- Integracija automatski migrira stare konfiguracije
- Obrisite browser keš ako se kartica ne ažurira
- Proverite imena entiteta (možda su se promenila)

## 🏗️ Razvoj

Ova integracija je deo [City Dashboard](https://github.com/dzarlax/city-dashboard) projekta.

### API Endpoints
- **Produkcija**: `https://transport-api.dzarlax.dev`
- **Fallback gradovi**: Beograd (`bg`), Novi Sad (`ns`), Niš (`nis`)

### Istorija verzija
- **v2.2.0**: Uprošćen interfejs, uklonjeno složeno filtriranje
- **v2.1.x**: Napredne funkcije sa sortiranjem i omiljenim
- **v2.0.0**: Velika prepravka sa vizuelnom konfiguracijom
- **v1.x**: Početno izdanje sa osnovnim funkcionalnostima


## Attribution / Atribucija

In this project, the bus icon from [Flaticon](https://www.flaticon.com/free-icons/bus) is used. Bus icons created by Freepik - Flaticon.

U ovom projektu korišćena je ikonica autobusa sa [Flaticon](https://www.flaticon.com/free-icons/bus). Bus ikonice kreirao Freepik - Flaticon.