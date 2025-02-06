
# Serbian Transport Integration

Home Assistant integration for Serbian public transport information.

## Features
- Real-time bus arrival information
- Nearest stops discovery
- Custom Lovelace card

## Supported Cities
- Belgrade (GSP Belgrade)
- Novi Sad (JGSP Novi Sad)
- Nis (JKP Direkcija za javni prevoz grada Nisa)

## Installation
1. Add this repository to HACS
2. Install "Serbian Transport" from HACS
3. Restart Home Assistant
4. Add integration through HA Settings -> Devices & Services

## Usage
After installation, you can use the custom card in your Lovelace UI:

```yaml
type: 'custom:transport-card'
entity: sensor.transport_stations_count
```

## Troubleshooting

If the custom card doesn't appear in your Lovelace dashboard, you may need to add it manually as a resource:

1. Go to Configuration -> Lovelace Dashboards -> Resources
2. Click the "+" button to add a new resource
3. Enter the following URL: `/hacsfiles/transport-card/transport-card.js`
4. Select "JavaScript Module" as the resource type
5. Click "Create"
6. Refresh your browser

## Repository

This integration is part of the [City Dashboard](https://github.com/dzarlax/city-dashboard) project.


# Srpski Transport Integracija

Home Assistant integracija za informacije o srpskom javnom prevozu.

## Funkcije
- Informacije o dolasku autobusa u realnom vremenu
- Otkrivanje najbližih stanica
- Prilagođena Lovelace kartica

## Podržani gradovi
- Beograd (GSP Beograd)
- Novi Sad (JGSP Novi Sad)
- Niš (JKP Direkcija za javni prevoz grada Niša)

## Instalacija
1. Dodajte ovaj repozitorijum u HACS
2. Instalirajte "Serbian Transport" iz HACS-a
3. Restartujte Home Assistant
4. Dodajte integraciju kroz HA Podešavanja -> Uređaji i Servisi

## Upotreba
Nakon instalacije, možete koristiti prilagođenu karticu u Lovelace interfejsu:

```yaml
type: 'custom:transport-card'
entity: sensor.transport_stations_count
```

## Rešavanje problema

Ako se prilagođena kartica ne pojavljuje na vašoj Lovelace kontrolnoj tabli, možda ćete morati da je dodate ručno kao resurs:

1. Idite na Konfiguracija -> Lovelace kontrolne table -> Resursi
2. Kliknite na "+" dugme da dodate novi resurs
3. Unesite sledeći URL: `/hacsfiles/transport-card/transport-card.js`
4. Izaberite "JavaScript Module" kao tip resursa
5. Kliknite "Kreiraj"
6. Osvežite pregledač

## Repozitorijum

Ova integracija je deo [City Dashboard](https://github.com/dzarlax/city-dashboard) projekta.


## Attribution / Atribucija

In this project, the bus icon from [Flaticon](https://www.flaticon.com/free-icons/bus) is used. Bus icons created by Freepik - Flaticon.

U ovom projektu korišćena je ikonica autobusa sa [Flaticon](https://www.flaticon.com/free-icons/bus). Bus ikonice kreirao Freepik - Flaticon.