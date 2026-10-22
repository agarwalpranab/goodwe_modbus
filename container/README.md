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
| `vpv1` / `vpv2` | PV1/PV2 Voltage | V |
| `ipv1` / `ipv2` | PV1/PV2 Current | A |
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
│   ├── const.py             # sensor registry
│   ├── inverter.py          # async Goodwe poller
│   └── mqtt.py              # MQTT publisher + HA discovery
└── mosquitto/
    └── config/
        └── mosquitto.conf   # bundled broker config
```
