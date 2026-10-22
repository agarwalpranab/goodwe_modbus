"""Entrypoint for the goodwe-modbus MQTT container."""
from __future__ import annotations

import asyncio
import logging
import signal
import sys
from typing import Any

from goodwe_mqtt.config import load_config
from goodwe_mqtt.inverter import InverterPoller
from goodwe_mqtt.mqtt import MqttPublisher


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )


async def run() -> None:
    cfg = load_config()
    _setup_logging(cfg.log_level)

    log = logging.getLogger("goodwe_mqtt.main")
    log.info(
        "Starting goodwe-modbus MQTT bridge  "
        "(inverter=%s:%d  mqtt=%s:%d  interval=%ds)",
        cfg.inverter.host,
        cfg.inverter.port,
        cfg.mqtt.host,
        cfg.mqtt.port,
        cfg.inverter.scan_interval,
    )

    publisher = MqttPublisher(cfg.mqtt)
    await publisher.connect()

    # This callback is invoked by InverterPoller on every successful poll.
    async def on_data(data: dict[str, Any]) -> None:
        await publisher.publish_with_reconnect(data, poller.inverter_info)

    poller = InverterPoller(cfg.inverter, on_data)

    # Graceful shutdown on SIGINT / SIGTERM
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def _shutdown(sig: signal.Signals) -> None:
        log.info("Received %s — shutting down", sig.name)
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _shutdown, sig)

    # Run the poller as a background task
    poll_task = asyncio.create_task(poller.run(), name="inverter-poller")

    # Wait until a stop signal is received
    await stop_event.wait()

    poll_task.cancel()
    try:
        await poll_task
    except asyncio.CancelledError:
        pass

    await publisher.disconnect()
    log.info("Shutdown complete")


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
