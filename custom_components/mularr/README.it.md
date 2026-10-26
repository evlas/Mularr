<p align="center">
  <img src="brand/logo.png" alt="Mularr Logo" width="360">
</p>

# Mularr - Home Assistant Integration 🐴

🌍 **Lingua / Language**: [English](README.md) • **Italiano**

Integrazione personalizzata per **Home Assistant** per monitorare e controllare **[Mularr](https://github.com/joecarl/mularr)** (aMule Web & Automation).

---

## 🚀 Caratteristiche

* ⚙️ **Configurazione completa da interfaccia grafica (UI)** con Config Flow.
* 🔒 **Supporto API Key** e controllo automatico della connessione.
* 📊 **Sensori di telemetria**:
  * Velocità Download e Upload (in B/s, kB/s con device class dedicata).
  * Stato ID (HighID / LowID).
  * Stato KAD (Firewalled / Direct).
  * Server connesso e dettagli di rete.
  * Conteggio download attivi.
  * File condivisi, fonti totali e coda di upload.
  * Totale scaricato e inviato (statistiche a lungo termine supportate).
  * Spazio disco residuo su storage.
  * Indirizzo IP pubblico e geolocalizzazione rilevata.
* 🔌 **Sensori Binari**:
  * Connessione ED2K attiva.
  * Rete KAD attiva.
  * Stato VPN Gluetun.
* 🔘 **Pulsanti di controllo**:
  * Riavvio demone aMule.
  * Pulizia trasferimenti completati.
  * Connessione server.
* 🎚️ **Switch**:
  * Interruttore per connettere o disconnettere la sessione dal server ED2K.

---

## 📦 Installazione

### Metodo 1: Installazione Manuale
1. Copia l'intera cartella `custom_components/mularr` all'interno della cartella `custom_components` della tua installazione di Home Assistant:
   ```text
   /config/custom_components/mularr/
   ```
2. Riavvia Home Assistant.

### Metodo 2: Installazione via HACS
1. Apri **HACS** in Home Assistant.
2. Vai su **Integrazioni** e clicca sui tre puntini in alto a destra -> **Repository personalizzati**.
3. Incolla l'URL del tuo repository GitHub e seleziona la categoria **Integrazione**.
4. Clicca su **Scarica** e riavvia Home Assistant.

---

## 🛠️ Configurazione

1. In Home Assistant vai su **Impostazioni** -> **Dispositivi e servizi**.
2. Clicca su **Aggiungi integrazione** in basso a destra.
3. Cerca **Mularr**.
4. Inserisci i dati della tua istanza:
   * **Host**: `192.168.0.2`
   * **Porta**: `8940` (default)
   * **API Key**: la tua chiave API (se abilitata)
   * **Usa SSL**: disattivato (a meno che tu non abbia un reverse proxy HTTPS)
5. Clicca su **Invia**. L'integrazione verificherà le credenziali e creerà il dispositivo con tutte le entità.

---

## 🎨 Esempio Card Lovelace

```yaml
type: entities
title: Mularr
show_header_toggle: false
entities:
  - entity: switch.mularr_192_168_0_2_ed2k_server_connection
  - entity: sensor.mularr_192_168_0_2_download_speed
  - entity: sensor.mularr_192_168_0_2_upload_speed
  - entity: sensor.mularr_192_168_0_2_active_downloads
  - entity: sensor.mularr_192_168_0_2_id_status
  - entity: sensor.mularr_192_168_0_2_kad_status
  - entity: sensor.mularr_192_168_0_2_connected_server
  - entity: sensor.mularr_192_168_0_2_free_disk_space
  - entity: button.mularr_192_168_0_2_restart_daemon
  - entity: button.mularr_192_168_0_2_clear_completed
```
