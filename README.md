<p align="center">
  <img src="custom_components/mularr/brand/logo.png" alt="Mularr Logo" width="360">
</p>

# Mularr - Home Assistant Integration 🐴

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/evlas/Mularr?color=blue&style=flat-square)](https://github.com/evlas/Mularr/releases)
[![Hassfest](https://github.com/evlas/Mularr/actions/workflows/hassfest.yml/badge.svg)](https://github.com/evlas/Mularr/actions/workflows/hassfest.yml)
[![HACS Action](https://github.com/evlas/Mularr/actions/workflows/hacs.yml/badge.svg)](https://github.com/evlas/Mularr/actions/workflows/hacs.yml)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

🌍 **Language / Lingua**: **English** • [Italiano](README.it.md)

Custom integration for **Home Assistant** to monitor, manage, and automate your **Mularr** (aMule Web & Automation) instance.

---

## 🐴 What is Mularr?

This integration requires an active instance of **[Mularr](https://github.com/joecarl/mularr)**, an open-source project created by **[joecarl](https://github.com/joecarl)**.

**Mularr** is a powerful Docker container solution for **aMule** that blends classic P2P with modern media automation tools:
* 🌐 **Retro-Style Web Interface**: Responsive dashboard with nostalgic aesthetics (default Windows XP, Windows 11, Modern, and Hacker themes).
* 🔄 **Integration with the \*Arr Stack**: Provides qBittorrent API compatibility and Torznab indexers to seamlessly connect aMule with Sonarr, Radarr, etc.
* 🛡️ **VPN & Gluetun Support**: Native integration for VPN health monitoring and automatic port forwarding updates.
* ✈️ **Telegram Integration**: Bot notifications for finished downloads and remote download management via Telegram.
* 📦 **Bundled aMule Daemon**: Includes pre-configured aMule v3.0+, eliminating the need to manage separate containers.

> 📖 For instructions on how to install and run the Mularr container via Docker Compose, visit the official repository: **[https://github.com/joecarl/mularr](https://github.com/joecarl/mularr)**.

---

## 🌟 Key Features

* ⚙️ **GUI-based Configuration**: Effortless setup via Config Flow.
* 🔒 **API Key Authentication**: With automatic detection of invalid credentials.
* ⏱️ **Custom Polling Interval**: Adjustable via Options Flow (from 2 to 300 seconds).
* 🚀 **High Performance**: Fully asynchronous client (`aiohttp`) with parallel requests.
* 🌍 **Multi-language Support**: Native English, Italian, Spanish, and French translations.

---

## 📊 Provided Entities

All entities are automatically grouped under a single **Mularr** device in Home Assistant:

### 📈 Sensors (`sensor`)
| Entity | Unique ID | Description | Unit / Class |
| :--- | :--- | :--- | :--- |
| **Download Speed** | `download_speed` | Current download rate | `B/s` / `kB/s` (`data_rate`) |
| **Upload Speed** | `upload_speed` | Current upload rate | `B/s` / `kB/s` (`data_rate`) |
| **ID Status** | `id_status` | aMule network ID state | `HighID` / `LowID` |
| **KAD Status** | `kad_status` | KAD network state | `Firewalled` / `Direct` |
| **Connected Server** | `connected_server` | Active ED2K server name with IP, port, and ping | Text / Attributes |
| **Active Downloads** | `active_downloads` | Number of files currently downloading | Count |
| **Shared Files** | `shared_files` | Number of files shared on the network | Count |
| **Total Sources** | `total_sources` | Total sources across all active downloads | Count |
| **Upload Queue** | `upload_queue` | Users waiting in upload queue | Count |
| **Total Downloaded** | `total_downloaded` | Lifetime total bytes downloaded | `B` / `GB` (`total_increasing`) |
| **Total Uploaded** | `total_uploaded` | Lifetime total bytes uploaded | `B` / `GB` (`total_increasing`) |
| **Free Disk Space** | `free_disk_space` | Available space on Mularr storage disk | `B` / `GB` (`data_size`) |
| **Public IP** | `public_ip` | Detected public IP address with city and country | IP / Geo Attributes |

### 🔌 Binary Sensors (`binary_sensor`)
| Entity | Unique ID | Description | Device Class |
| :--- | :--- | :--- | :--- |
| **ED2K Connected** | `ed2k_connected` | Active connection to the ED2K network | `connectivity` |
| **KAD Connected** | `kad_connected` | Active connection to the KAD network | `connectivity` |
| **VPN Active** | `vpn_status` | Gluetun VPN operational status | `connectivity` |

### 🔘 Buttons (`button`)
| Entity | Unique ID | Action |
| :--- | :--- | :--- |
| **Restart Daemon** | `restart_daemon` | Performs a clean restart of the aMule daemon |
| **Clear Completed** | `clear_completed` | Clears finished downloads from the transfer list |
| **Connect to Server** | `connect_server` | Attempts to connect to the best available server |

### 🎚️ Switch (`switch`)
| Entity | Unique ID | Action |
| :--- | :--- | :--- |
| **ED2K Server Connection** | `server_connection` | Connects or disconnects the ED2K server connection |

---

## 📥 Installation

### Method 1: Via HACS (Recommended)
1. Make sure [HACS](https://hacs.xyz/) is installed in Home Assistant.
2. Open **HACS** from the sidebar and click on **Integrations**.
3. Click the **three dots in the top-right corner** and select **Custom repositories**.
4. Enter your GitHub repository URL:
   * **Repository**: `https://github.com/evlas/Mularr`
   * **Type**: `Integration`
5. Click **Add**.
6. Search for **Mularr**, click **Download**, and select the latest version.
7. **Restart Home Assistant**.

---

### Method 2: Manual Installation
1. Download the latest release or clone the repository.
2. Copy the `custom_components/mularr` folder into the `custom_components` directory of your Home Assistant installation:
   ```text
   /config/custom_components/mularr/
   ```
3. **Restart Home Assistant**.

---

## ⚙️ Configuration

1. In Home Assistant, go to **Settings** -> **Devices & services**.
2. Click **Add Integration** (bottom right).
3. Search for **Mularr**.
4. Fill in the form with your instance details:
   * **Host or IP Address**: e.g., `192.168.0.2`
   * **Port**: `8940` (default)
   * **API Key**: your secret key (if set in Mularr's environment variables)
   * **Use SSL**: check if Mularr is served over HTTPS
5. Click **Submit**: the integration will verify connectivity and create the device.

> [!TIP]
> To adjust the polling interval, click **Configure** on the integration card and set your desired seconds (default: 10s).

---

## 🎨 Example Lovelace Dashboard

You can add this Entities card to display your Mularr status:

```yaml
type: entities
title: 🐴 Mularr
show_header_toggle: false
entities:
  - entity: switch.mularr_192_168_0_2_ed2k_server_connection
  - entity: binary_sensor.mularr_192_168_0_2_ed2k_connected
  - entity: binary_sensor.mularr_192_168_0_2_kad_connected
  - entity: sensor.mularr_192_168_0_2_id_status
  - entity: sensor.mularr_192_168_0_2_kad_status
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

## 🤖 Automation Examples

### 1. Smartphone alert when Mularr falls into LowID
```yaml
alias: "Mularr LowID Alert"
trigger:
  - platform: state
    entity_id: sensor.mularr_192_168_0_2_id_status
    to: "LowID"
    for:
      minutes: 2
action:
  - service: notify.notify
    data:
      title: "Mularr - Warning"
      message: "aMule has dropped to LowID! Check your port forwarding or VPN."
```

### 2. Automatically clear completed downloads every night at 04:00
```yaml
alias: "Mularr - Clear completed downloads nightly"
trigger:
  - platform: time
    at: "04:00:00"
action:
  - service: button.press
    target:
      entity_id: button.mularr_192_168_0_2_clear_completed
```

---

## 📄 License

Distributed under the GNU General Public License v3.0 (GPLv3). See [LICENSE](LICENSE) for more details.
