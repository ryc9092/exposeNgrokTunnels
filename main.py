import logging
import smtplib
import ssl

from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import yaml

import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("/var/log/exposeNgrokTunnels.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

DEVICE_TUNNELS_FILE = "/tmp/exposeNgrokTunnels.yaml"
EMAIL_CONCONFIG_FILE = "./emailConfiguration.yaml"
NGROK_API_URL = "http://localhost:4040/api/tunnels"


def get_ngrok_tunnels_list() -> list:
    try:
        response_ngrok_tunnels_info = requests.get(NGROK_API_URL)
        ngrok_tunnels_info = response_ngrok_tunnels_info.json().get("tunnels")

        ngrok_tunnels_list = []
        for tunnel in ngrok_tunnels_info:
            ngrok_tunnels_list.append(tunnel.get("public_url"))

        ngrok_tunnels_list.sort()
        return ngrok_tunnels_list

    except Exception as e:
        logger.error(f"Failed to get ngrok tunnels list: {e}")
        return []


def get_device_tunnels_list() -> list:
    try:
        device_tunnels_list = []
        with open(DEVICE_TUNNELS_FILE, mode="r") as f:
            device_tunnels_list = yaml.safe_load(f).get("tunnels")

    except Exception as e:
        logger.warning(f"Failed to read device tunnels information: {e}")

    device_tunnels_list.sort()
    return device_tunnels_list


def write_tunnels_info(tunnels_list: list):
    logger.info(f"Write tunnels info to device: {tunnels_list}")
    with open(DEVICE_TUNNELS_FILE, "w") as f:
        yaml.dump({"tunnels": tunnels_list}, f)


def send_tunnels_info_email(ngrok_tunnels: list):
    try:
        content = f"""Subject: Ngrok tunnels info of un42\n\n{ngrok_tunnels}"""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config.SMTP_SERVER, context=context) as server:
            server.login(config.SENDER, config.PASSWORD)
            server.sendmail(config.SENDER, config.RECEIVER, content)

    except Exception as e:
        logger.error(f"Failed to send ngrok tunnels info email: {e}")


def do_expose_tunnels_work():
    ngrok_tunnels_list = get_ngrok_tunnels_list()
    device_tunnels_list = get_device_tunnels_list()

    if (not device_tunnels_list) or (ngrok_tunnels_list != device_tunnels_list):
        write_tunnels_info(ngrok_tunnels_list)
        send_tunnels_info_email(ngrok_tunnels_list)


if __name__ == "__main__":
    try:
        logger.info("Start scheduler to expose ngrok tunnels...")

        scheduler = BlockingScheduler()
        scheduler.add_job(
            do_expose_tunnels_work, "interval", minutes=config.INTERVAL_MINUTES
        )
        scheduler.start()

    except Exception as e:
        logger.error(f"Failed to expose tunnels: {e}")
