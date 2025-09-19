
# Serbian Transport Integration

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![HACS](https://img.shields.io/badge/HACS-compatible-orange.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1.0+-green.svg)
![Automated Releases](https://img.shields.io/badge/releases-automated-green.svg)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dzarlax&repository=HASS-Serbian-transport&category=integration)

Advanced Home Assistant integration for Serbian public transport with real-time arrivals, beautiful animations, visual configuration, and intelligent station selection.

## 📸 Screenshots

### Main Interface
- **🎯 Station Selection Dropdown** - Easily choose which stations to monitor
- **📊 Real-time Arrivals** - Color-coded departure times with progress indicators
- **🎨 Modern UI** - Clean, responsive design that works on all devices

### Configuration Interface
- **⚙️ Visual Editor** - No YAML required, configure everything through the UI
- **🔧 Smart Defaults** - Automatically detects nearby stations based on your location
- **📱 Mobile Optimized** - Perfect for Home Assistant Companion app

## ✨ Features

### Core Features
- 🚌 **Real-time transport arrivals** - Live data from official transport APIs
- 📍 **Coordinate-based discovery** - Automatically finds nearby stops using your coordinates
- 🎨 **Modern visual interface** - Beautiful animations, color-coded arrivals, progress bars
- ⚙️ **Visual configuration** - Easy setup through Home Assistant UI (no YAML required)
- 📱 **Responsive design** - Works perfectly on mobile and desktop

### Advanced Features
- 🎯 **Intelligent station selection** - Choose specific stations to display with dropdown interface
- 📊 **Progress bars** - Visual time indicators with color coding
- 🔄 **Expandable view** - Compact/expanded modes for different use cases
- 🎭 **Smooth animations** - Hover effects and transitions for modern UX
- 🔧 **Automated versioning** - Continuous delivery with automated releases and changelog
- ⚡ **Smart caching** - Optimized data fetching with error handling

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
   - **Station Selection**: Choose specific stations to display (dropdown interface)
   - **Max Stations**: Number of stations to display (1-50)
   - **Show Next Departure**: Toggle next departure section
   - **Compact View**: Default view mode
   - **Refresh Interval**: Data update frequency (10-300 seconds)

#### YAML Configuration (Advanced)
```yaml
type: custom:transport-card
entity: sensor.serbian_transport_stations_count
title: "Serbian Transport"
selected_stations: ["Trg Republike", "Autokomanda", "Zeleni Venac"]  # Optional: specific stations
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
| `selected_stations` | array | `[]` | List of specific station names to display (optional) |
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
- **Station selection dropdown** - Choose specific stations to monitor
- **Hover effects** on transport groups
- **Expandable/collapsible** view with animation
- **Progress bars** showing time until arrival
- **Status indicators** for station data availability
- **Smart filtering** - Show only selected stations or all nearby stations

## 🆕 What's New in v2.4.0

### 🎯 Station Selection Dropdown
- **Intelligent filtering** - Choose exactly which stations you want to monitor
- **Distance indicators** - See how far each station is from your location
- **"All stations" option** - Toggle between filtered and complete view
- **Persistent selection** - Your choices are saved and restored

### 🚀 Automated Development
- **Continuous delivery** - Automatic releases with every feature addition
- **Smart versioning** - Semantic versions based on commit types
- **Auto-generated changelogs** - Beautiful release notes from commit messages
- **HACS integration** - Seamless updates through Home Assistant Community Store

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

## 🚀 Development & Releases

This integration features **automated versioning** with continuous delivery:

- 🤖 **Automated releases** via GitHub Actions
- 📝 **Auto-generated changelogs** from commit messages
- 🏷️ **Semantic versioning** based on conventional commits
- 📦 **HACS compatibility** with automatic updates

### Contributing
- Use [Conventional Commits](https://conventionalcommits.org/) for commit messages
- `feat:` for new features (minor version bump)
- `fix:` for bug fixes (patch version bump)
- `BREAKING:` for breaking changes (major version bump)

### Version History
See [CHANGELOG.md](CHANGELOG.md) for complete version history.

Recent releases:
- **v2.4.0**: Station selection with dropdown interface, automated versioning
- **v2.3.0**: Enhanced UI with improved error handling
- **v2.0.0**: Major rewrite with visual configuration
- **v1.x**: Initial release with basic functionality


# Srpski Transport Integracija

![Verzija](https://img.shields.io/badge/verzija-2.0.0-blue.svg)
![HACS](https://img.shields.io/badge/HACS-kompatibilna-orange.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1.0+-green.svg)
![Automatski Relizi](https://img.shields.io/badge/relizi-automatski-green.svg)

[![Otvorite vašu Home Assistant instancu i dodajte repozitorijum u Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dzarlax&repository=HASS-Serbian-transport&category=integration)

Napredna Home Assistant integracija za srpski javni prevoz sa dolaskom u realnom vremenu, lepim animacijama, vizuelnom konfiguracijom i inteligentnim izborom stanica.

## 📸 Snimci ekrana

### Glavni interfejs
- **🎯 Dropdown za izbor stanica** - Lako birate koje stanice želite da pratite
- **📊 Dolasci u realnom vremenu** - Vremena polaska označena bojama sa indikatorima napretka
- **🎨 Moderan UI** - Čist, responsive dizajn koji radi na svim uređajima

### Interfejs za konfiguraciju
- **⚙️ Vizuelni editor** - YAML nije potreban, konfiguriše se sve kroz UI
- **🔧 Pametni default-ovi** - Automatski otkriva obližnje stanice na osnovu vaše lokacije
- **📱 Optimizovano za mobilne** - Savršeno za Home Assistant Companion aplikaciju

## ✨ Funkcije

### Osnovne funkcije
- 🚌 **Dolasci prevoza u realnom vremenu** - Živi podaci sa zvaničnih transport API-ja
- 📍 **Otkrivanje bazirano na koordinatama** - Automatski pronalazi obližnje stanice koristeći vaše koordinate
- 🎨 **Moderan vizuelni interfejs** - Lepe animacije, dolasci u boji, trake napretka
- ⚙️ **Vizuelna konfiguracija** - Lako podešavanje kroz Home Assistant UI (YAML nije potreban)
- 📱 **Responsive dizajn** - Savršeno radi na mobilnim uređajima i desktopima

### Napredne funkcije  
- 🎯 **Inteligentni izbor stanica** - Biraju se specifične stanice za prikaz sa dropdown interfejsom
- 📊 **Trake napretka** - Vizuelni indikatori vremena sa kodiranjem u boji
- 🔄 **Proširiv prikaz** - Kompaktni/prošireni režimi za različite slučajeve korišćenja
- 🎭 **Glatke animacije** - Hover efekti i prelazi za moderan UX
- 🔧 **Automatsko verzioniranje** - Kontinuirano dostavljanje sa automatskim relizima i changelog-om
- ⚡ **Pametno keširanje** - Optimizovano preuzimanje podataka sa rukovanjem greškama

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
   - **Station Selection**: Izaberite specifične stanice za prikaz (dropdown interfejs)
   - **Max Stations**: Broj stanica za prikaz (1-50)
   - **Show Next Departure**: Uključi/isključi sekciju sledećeg polaska
   - **Compact View**: Podrazumevani režim prikaza
   - **Refresh Interval**: Frekvencija ažuriranja podataka (10-300 sekundi)

#### YAML konfiguracija (Napredna)
```yaml
type: custom:transport-card
entity: sensor.serbian_transport_stations_count
title: "Serbian Transport"
selected_stations: ["Trg Republike", "Autokomanda", "Zeleni Venac"]  # Opciono: specifične stanice
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
| `selected_stations` | array | `[]` | Lista specifičnih imena stanica za prikaz (opciono) |
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
- **Dropdown za izbor stanica** - Biraju se specifične stanice za praćenje
- **Hover efekti** na transport grupama
- **Proširiv/sklopiv** prikaz sa animacijom
- **Trake napretka** koje prikazuju vreme do dolaska
- **Status indikatori** za dostupnost podataka stanice
- **Pametno filtriranje** - Prikaži samo izabrane stanice ili sve bliske stanice

## 🆕 Šta je novo u v2.4.0

### 🎯 Dropdown za izbor stanica
- **Inteligentno filtriranje** - Birate tačno koje stanice želite da pratite
- **Indikatori udaljenosti** - Vidite koliko je daleko svaka stanica od vaše lokacije
- **Opcija "Sve stanice"** - Prebacivanje između filtriranog i kompletnog prikaza
- **Perzistentni izbor** - Vaši izbori se čuvaju i vraćaju

### 🚀 Automatizovan razvoj
- **Kontinuirano dostavljanje** - Automatski relizi sa svakim dodavanjem funkcije
- **Pametno verzioniranje** - Semantičke verzije na osnovu tipova commit-a
- **Automatski generisani changelog-ovi** - Lepe release note iz commit poruka
- **HACS integracija** - Besprekorna ažuriranja kroz Home Assistant Community Store

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

## 🚀 Razvoj i Relizi

Ova integracija ima **automatsko verzioniranje** sa kontinuiranim dostavljanjem:

- 🤖 **Automatski relizi** preko GitHub Actions
- 📝 **Automatski generisan changelog** iz commit poruka
- 🏷️ **Semantičko verzioniranje** bazirano na konvencionalnim commit-ima
- 📦 **HACS kompatibilnost** sa automatskim ažuriranjima

### Doprinošenje
- Koristite [Konvencionalne Commit-e](https://conventionalcommits.org/) za commit poruke
- `feat:` za nove funkcije (minor verzija)
- `fix:` za popravke grešaka (patch verzija)
- `BREAKING:` za prekidajuće promene (major verzija)

### Istorija verzija
Pogledajte [CHANGELOG.md](CHANGELOG.md) za kompletnu istoriju verzija.

Nedavni relizi:
- **v2.4.0**: Izbor stanica sa dropdown interfejsom, automatsko verzioniranje
- **v2.3.0**: Poboljšan UI sa proračunavanjem grešaka
- **v2.0.0**: Velika prepravka sa vizuelnom konfiguracijom
- **v1.x**: Početno izdanje sa osnovnim funkcionalnostima


## Attribution / Atribucija

In this project, the bus icon from [Flaticon](https://www.flaticon.com/free-icons/bus) is used. Bus icons created by Freepik - Flaticon.

U ovom projektu korišćena je ikonica autobusa sa [Flaticon](https://www.flaticon.com/free-icons/bus). Bus ikonice kreirao Freepik - Flaticon.