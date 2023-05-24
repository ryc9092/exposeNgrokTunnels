import argparse
import yaml


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="./config.yaml",
        help="Specific a config for service.",
    )

    args = parser.parse_args()

    with open(args.config) as f:
        return yaml.safe_load(f)


CONFIG = load_config()


"""
scheduler
"""

INTERVAL_MINUTES = CONFIG["scheduler"]["minutes"]


"""
email
"""

SECTION_EMAIL = "email"

SMTP_SERVER = CONFIG[SECTION_EMAIL]["smtp_server"]
SENDER = CONFIG[SECTION_EMAIL]["sender"]
RECEIVER = CONFIG[SECTION_EMAIL]["receiver"]
PASSWORD = CONFIG[SECTION_EMAIL]["password"]
