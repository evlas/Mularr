# Mularr - Home Assistant Integration 🐴

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/vito/homeassistant-mularr?color=blue&style=flat-square)](https://github.com/vito/homeassistant-mularr/releases)
[![Hassfest](https://github.com/vito/homeassistant-mularr/actions/workflows/hassfest.yml/badge.svg)](https://github.com/vito/homeassistant-mularr/actions/workflows/hassfest.yml)
[![HACS Action](https://github.com/vito/homeassistant-mularr/actions/workflows/hacs.yml/badge.svg)](https://github.com/vito/homeassistant-mularr/actions/workflows/hacs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Integrazione personalizzata per **Home Assistant** per monitorare, gestire e automatizzare la tua istanza di **Mularr** (aMule Web & Automation).

---

## 🌟 Caratteristiche Principali

* ⚙️ **Configurazione guidata da interfaccia grafica (UI)** tramite Config Flow.
* 🔒 **Supporto API Key** con rilevamento automatico errori di autenticazione.
* ⏱️ **Intervallo di aggiornamento personalizzabile** (Options Flow) da 2 a 300 secondi.
* 🚀 **Prestazioni elevate**: client completamente asincrono (`aiohttp`) con chiamate parallele.
* 🌍 **Supporto Multilingua**: Italiano e Inglese nativi.

---

## 📊 Entità Fornite

Tutte le entità vengono associate automaticamente a un unico dispositivo **Mularr** in Home Assistant:

### 📈 Sensori (`sensor`)
| Entità | ID Unico | Descrizione | Unità / Classe |
| :--- | :--- | :--- | :--- |
| **Velocità Download** | `download_speed` | Velocità di ricezione attuale | `B/s` / `kB/s` (`data_rate`) |
| **Velocità Upload** | `upload_speed` | Velocità di trasmissione attuale | `B/s` / `kB/s` (`data_rate`) |
| **Stato ID** | `id_status` | Stato rete aMule | `HighID` / `LowID` |
| **Server Connesso** | `connected_server` | Nome del server ED2K attivo con IP, porta e ping | Testo / Attributi |
| **Download Attivi** | `active_downloads` | Numero di file attualmente in scaricamento | Conteggio |
| **File Condivisi** | `shared_files` | Numero di file condivisi in rete | Conteggio |
| **Fonti Totali** | `total_sources` | Fonti trovate per tutti i download | Conteggio |
| **Coda di Upload** | `upload_queue` | Utenti in attesa nella coda di upload | Conteggio |
| **Totale Scaricato** | `total_downloaded` | Byte totali scaricati nella storia del client | `B` / `GB` (`total_increasing`) |
| **Totale Inviato** | `total_uploaded` | Byte totali inviati nella storia del client | `B` / `GB` (`total_increasing`) |
| **Spazio Disco Libero** | `free_disk_space` | Spazio residuo nel disco di archiviazione Mularr | `B` / `GB` (`data_size`) |
| **IP Pubblico** | `public_ip` | Indirizzo IP pubblico rilevato con città e nazione | IP / Attributi Geo |

### 🔌 Sensori Binari (`binary_sensor`)
| Entità | ID Unico | Descrizione | Device Class |
| :--- | :--- | :--- | :--- |
| **ED2K Connesso** | `ed2k_connected` | Connessione alla rete ED2K attiva | `connectivity` |
| **KAD Connesso** | `kad_connected` | Connessione alla rete KAD attiva | `connectivity` |
| **KAD Firewalled** | `kad_firewalled` | Segnala se il KAD è dietro firewall | `problem` |
| **VPN Attiva** | `vpn_status` | Stato della VPN Gluetun | `connectivity` |

### 🔘 Pulsanti (`button`)
| Entità | ID Unico | Azione |
| :--- | :--- | :--- |
| **Riavvia Demone** | `restart_daemon` | Esegue un riavvio pulito del demone aMule |
| **Pulisci Completati** | `clear_completed` | Rimuove i download completati dalla lista trasferimenti |
| **Connetti a Server** | `connect_server` | Tenta la connessione al miglior server disponibile |

### 🎚️ Interruttore (`switch`)
| Entità | ID Unico | Azione |
| :--- | :--- | :--- |
| **Connessione Server ED2K** | `server_connection` | Accende (connette) o spegne (disconnette) la connessione ED2K |

---

## 📥 Installazione

### Metodo 1: Tramite HACS (Consigliato)
1. Assicurati di avere [HACS](https://hacs.xyz/) installato in Home Assistant.
2. Apri **HACS** dal menu laterale e clicca su **Integrazioni**.
3. Clicca sui **tre puntini in alto a destra** e seleziona **Repository personalizzati**.
4. Inserisci l'URL del tuo repository GitHub:
   * **Repository**: `https://github.com/evlas/Mularr`
   * **Tipo**: `Integrazione`
5. Clicca su **Aggiungi**.
6. Cerca **Mularr**, clicca su **Scarica** e seleziona l'ultima versione.
7. **Riavvia Home Assistant**.

---

### Metodo 2: Installazione Manuale
1. Scarica l'ultima release o clona il repository.
2. Copia la cartella `custom_components/mularr` dentro la cartella `custom_components` della tua installazione di Home Assistant:
   ```text
   /config/custom_components/mularr/
   ```
3. **Riavvia Home Assistant**.

---

## ⚙️ Configurazione

1. In Home Assistant vai su **Impostazioni** -> **Dispositivi e servizi**.
2. Clicca su **Aggiungi integrazione** (in basso a destra).
3. Cerca **Mularr**.
4. Compila il modulo con i dati della tua istanza:
   * **Host o Indirizzo IP**: es. `192.168.0.2`
   * **Porta**: `8940` (default)
   * **API Key**: la tua chiave segreta (se configurata nelle variabili d'ambiente di Mularr)
   * **Usa SSL**: seleziona se Mularr risponde su HTTPS
5. Clicca su **Invia**: l'integrazione verificherà la raggiungibilità e aggiungerà il dispositivo.

> [!TIP]
> Per modificare l'intervallo di polling, clicca su **Configura** nella scheda dell'integrazione e imposta i secondi desiderati (default: 10s).

---

## 🎨 Esempio Dashboard Lovelace

Puoi aggiungere questa scheda Entities per visualizzare lo stato di Mularr:

```yaml
type: entities
title: 🐴 Mularr
show_header_toggle: false
entities:
  - entity: switch.mularr_192_168_0_2_ed2k_server_connection
  - entity: binary_sensor.mularr_192_168_0_2_ed2k_connected
  - entity: binary_sensor.mularr_192_168_0_2_kad_connected
  - entity: sensor.mularr_192_168_0_2_id_status
  - entity: sensor.mularr_192_168_0_2_connected_server
  - type: divider
  - entity: sensor.mularr_192_168_0_2_download_speed
  - entity: sensor.mularr_192_168_0_2_upload_speed
  - entity: sensor.mularr_192_168_0_2_active_downloads
  - entity: sensor.mularr_192_168_0_2_free_disk_space
  - type: divider
  - entity: button.mularr_192_168_0_2_restart_daemon
  - entity: button.mularr_192_168_0_2_clear_completed
```

---

## 🤖 Esempi di Automazioni

### 1. Notifica su smartphone se Mularr passa in LowID
```yaml
alias: "Allarme Mularr LowID"
trigger:
  - platform: state
    entity_id: sensor.mularr_192_168_0_2_id_status
    to: "LowID"
    for:
      minutes: 2
action:
  - service: notify.notify
    data:
      title: "Mularr - Attenzione"
      message: "aMule è passato in LowID! Verifica le porte o la VPN."
```

### 2. Pulisci i completati ogni notte alle 04:00
```yaml
alias: "Mularr - Pulisci completati notturno"
trigger:
  - platform: time
    at: "04:00:00"
action:
  - service: button.press
    target:
      entity_id: button.mularr_192_168_0_2_clear_completed
```

---

## 📄 Licenza

Distribuito sotto licenza MIT. Consulta il file [LICENSE](LICENSE) per maggiori informazioni.
