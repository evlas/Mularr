<p align="center">
  <img src="brand/logo.png" alt="Mularr Logo" width="360">
</p>

# Mularr - Home Assistant Integration 🐴

🌍 **Language / Lingua**: **English** • [Italiano](README.it.md)

Custom integration for **Home Assistant** to monitor and control **[Mularr](https://github.com/joecarl/mularr)** (aMule Web & Automation).

---

## 🚀 Features

* ⚙️ **Full GUI-based setup** via Config Flow.
* 🔒 **API Key support** and automatic connection testing.
* 📊 **Telemetry sensors**:
  * Download and Upload speed (in B/s, kB/s with dedicated device class).
  * ID Status (HighID / LowID).
  * KAD Status (Firewalled / Direct).
  * Connected server and network details.
  * Active downloads count.
  * Shared files, total sources, and upload queue.
  * Total downloaded and uploaded (long-term statistics supported).
  * Available free disk space.
  * Public IP address and detected geolocation.
* 🔌 **Binary Sensors**:
  * Active ED2K connection.
  * Active KAD network.
  * Gluetun VPN status.
* 🔘 **Control Buttons**:
  * Restart aMule daemon.
  * Clear completed transfers.
  * Connect to server.
* 🎚️ **Switch**:
  * Switch to connect or disconnect the ED2K server session.

---

## 📦 Installation

### Method 1: Manual Installation
1. Copy the `custom_components/mularr` folder into the `custom_components` directory of your Home Assistant installation:
   ```text
   /config/custom_components/mularr/
   ```
2. Restart Home Assistant.

### Method 2: Installation via HACS
1. Open **HACS** in Home Assistant.
2. Go to **Integrations** and click the three dots in the top right -> **Custom repositories**.
3. Paste the URL of your GitHub repository and select the **Integration** category.
4. Click **Download** and restart Home Assistant.

---

## 🛠️ Configuration

1. In Home Assistant, go to **Settings** -> **Devices & services**.
2. Click **Add Integration** in the bottom right corner.
3. Search for **Mularr**.
4. Fill in the connection form:
   * **Host**: `192.168.0.2`
   * **Port**: `8940` (default)
   * **API Key**: your API key (if enabled)
   * **Use SSL**: disabled (unless running behind an HTTPS reverse proxy)
5. Click **Submit**. The integration will verify credentials and set up the device with all entities.

---

## 🎨 Example Lovelace Card

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
