# goodwe-modbus MQTT container

A **standalone Docker container** that polls a Goodwe solar inverter over Modbus (UDP or TCP) and publishes every reading to an MQTT broker.  It runs independently of Home Assistant while remaining 100 % compatible with **Home Assistant MQTT Discovery**, so sensors appear automatically in HA if you point it at the same broker.

---

## Architecture

```
Goodwe Inverter
  │  (Modbus UDP/TCP)
  ▼
goodwe-modbus container
  │  (aiomqtt)
  ▼
MQTT broker  (e.g. Mosquitto)
  │
  ├─► Home Assistant  (via MQTT integration + auto-discovery)
  └─► Any other MQTT subscriber
```

---

## Quick start

```bash
cd container
cp .env.example .env
# Edit .env — set INVERTER_HOST and MQTT_HOST at minimum
docker compose up -d
```

If you don't already have an MQTT broker, the included `docker-compose.yml` also spins up a Mosquitto instance.

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `INVERTER_HOST` | **required** | IP / hostname of the inverter |
| `INVERTER_PROTOCOL` | `UDP` | `UDP` or `TCP` |
| `INVERTER_PORT` | `8899` (UDP) / `502` (TCP) | Modbus port |
| `INVERTER_FAMILY` | `auto` | Inverter family: `auto`, `ET`, `EH`, `BT`, `BH`, `ES`, `EM`, `BP`, `DT`, `MS`, `NS`, `XS` |
| `INVERTER_COMM_ADDR` | `247` (0xF7) | Modbus comm address |
| `SCAN_INTERVAL` | `30` | Poll interval in seconds |
| `MQTT_HOST` | **required** | MQTT broker hostname |
| `MQTT_PORT` | `1883` | MQTT broker port |
| `MQTT_USERNAME` | _(none)_ | MQTT username |
| `MQTT_PASSWORD` | _(none)_ | MQTT password |
| `MQTT_TOPIC_PREFIX` | `goodwe` | Root topic prefix |
| `MQTT_CLIENT_ID` | `goodwe-modbus` | MQTT client identifier |
| `MQTT_HA_DISCOVERY` | `true` | Publish HA auto-discovery config payloads |
| `MQTT_HA_DISCOVERY_PREFIX` | `homeassistant` | HA discovery prefix (match HA setting) |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |

---

## MQTT topic structure

| Topic | Contents |
|---|---|
| `goodwe/<serial>/sensor/<key>/state` | Single sensor value (plain string) |
| `goodwe/<serial>/state` | JSON snapshot of all sensor values |
| `homeassistant/sensor/goodwe_<serial>_<key>/config` | HA discovery config (retained, sent once on startup) |

`<serial>` is the inverter's serial number read on first connection.

---

## Sensors published

| Key | Name | Unit |
|---|---|---|
| `vpv1` … `vpv4` | PV1–PV4 Voltage | V |
| `ipv1` … `ipv4` | PV1–PV4 Current | A |
| `ppv` | PV Power | W |
| `vgrid` | Grid Voltage | V |
| `igrid` | Grid Current | A |
| `fgrid` | Grid Frequency | Hz |
| `pgrid` | Grid Power | W |
| `work_mode` | Work Mode | — |
| `temperature` | Inverter Temperature | °C |
| `error_codes` | Error Codes | — |
| `e_day` | Energy Today | kWh |
| `e_total` | Energy Total | kWh |
| `h_total` | Hours Total | h |
| `battery_soc` | Battery State of Charge | % |
| `battery_voltage` | Battery Voltage | V |
| `battery_current` | Battery Current | A |
| `battery_power` | Battery Power | W |
| `battery_mode` | Battery Mode | — |
| `load_power` | Load Power | W |
| `backup_power` | Backup Power | W |

> **Note:** Only sensors that the inverter actually returns are published.  Battery sensors will be absent on PV-only (non-hybrid) models.

---

## Building without docker compose

```bash
cd container
docker build -t goodwe-modbus-mqtt .
docker run --rm \
  -e INVERTER_HOST=192.168.1.100 \
  -e MQTT_HOST=192.168.1.10 \
  goodwe-modbus-mqtt
```

---

## Synology deployment (Container Manager)

The image is published on Docker Hub as `agarwalpranab/goodwe-modbus-mqtt` (tags: `latest` and versioned, e.g. `1.0.0`) for `linux/amd64`, `linux/arm64` and `linux/arm/v7`, so it runs on any Synology model that supports Container Manager.  Nothing needs to be built on the NAS.

The container only makes **outbound** connections (to the inverter and to the MQTT broker), so no port mappings or volumes are required.

### Option A — Project (docker-compose), recommended

1. In **Container Manager → Project → Create**, choose a project name (e.g. `goodwe-modbus`) and a path such as `/volume1/docker/goodwe-modbus`.
2. Select **Create docker-compose.yml** and paste:

   ```yaml
   services:
     goodwe-modbus:
       image: agarwalpranab/goodwe-modbus-mqtt:latest
       container_name: goodwe-modbus
       restart: unless-stopped
       environment:
         INVERTER_HOST: "192.168.1.100"   # required
         INVERTER_PROTOCOL: "UDP"
         INVERTER_FAMILY: "auto"
         SCAN_INTERVAL: "30"
         MQTT_HOST: "192.168.1.10"        # required — broker LAN IP, not localhost
         MQTT_PORT: "1883"
         MQTT_USERNAME: ""
         MQTT_PASSWORD: ""
         MQTT_TOPIC_PREFIX: "goodwe"
         MQTT_HA_DISCOVERY: "true"
         MQTT_HA_DISCOVERY_PREFIX: "homeassistant"
         LOG_LEVEL: "INFO"
       # network_mode: host   # uncomment if the inverter is unreachable from the default bridge network
   ```

3. Click **Next → Done**.  Container Manager pulls the image and starts the container.

### Option B — Manual container

1. **Registry**: search for `agarwalpranab/goodwe-modbus-mqtt`, click **Download**, and pick the `latest` tag (or a pinned version).
2. **Container → Create** and use these settings:

   | Setting | Value |
   |---|---|
   | Image | `agarwalpranab/goodwe-modbus-mqtt:latest` |
   | Container name | `goodwe-modbus` |
   | Enable auto-restart | On |
   | Port settings | None |
   | Volume settings | None |
   | Network | `bridge` (default); use `host` if the inverter does not respond over UDP |
   | Execution command | Leave empty (image runs `python main.py`) |

3. Under **Advanced Settings → Environment**, add the variables from the [Environment variables](#environment-variables) table.  At minimum set `INVERTER_HOST` and `MQTT_HOST`.

### Synology notes

- **`MQTT_HOST` must not be `localhost`** — inside the container that refers to the container itself.  Use the broker's LAN IP.  If Mosquitto runs on the same NAS, use the NAS IP and make sure its port 1883 is published.
- **One client per inverter**: stop any other integration (e.g. the Home Assistant GoodWe integration) that polls the same inverter; the inverter's WiFi module handles concurrent connections poorly.
- **Updating**: download the new image tag, then stop, clear and start the container (or **Project → Build/Action → Rebuild** for Option A).  Pin a version tag to avoid unexpected updates.
- **Verify**: open the container's **Log** tab; you should see successful connections to the inverter and the MQTT broker, and sensors appearing in Home Assistant.

---

## Directory layout

```
container/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── main.py                  # entrypoint
├── goodwe_mqtt/
│   ├── __init__.py
│   ├── config.py            # env-var config loader
│   ├── const.py             # unit/kind → HA metadata mapping
│   ├── inverter.py          # async Goodwe poller
│   └── mqtt.py              # MQTT publisher + HA discovery
└── mosquitto/
    └── config/
        └── mosquitto.conf   # bundled broker config
```
