"""module ini untuk mengenerate toml config file jika missing.

ketika config file dan tidak ada, maka akan di generate default file
tanpa values, dan wajib di isi oleh user

"""

import pathlib

import loguru

BASE_PATH = pathlib.Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = BASE_PATH / "config.toml"


def generate_default_config_file():
    """Jika File config.toml tidak ada, maka generate default file."""
    if CONFIG_FILE.exists():
        loguru.logger.info(
            f"Config file already exists at {CONFIG_FILE}, skipping generation."
        )
        return
    # Placeholder config content with empty values
    default_config = """
app_rate_limit = ""
log_level = ""
log_file = ""

[server]
host = ""
port = ""
workers = ""
debug = ""

# jika members ada lebih dari satu, tambahkan array of table [[members]]
[[members]]
name = ""
ipaddress = ""
report_url = ""
rate_limiter = ""
is_allowed = ""
description = ""

# jika akun digipos ada lebih dari satu, tambahkan array of table
[[digipos]]
url = ""
username = ""
password = ""
retries = ""
time_out = ""

[parser.digipos]
# setup untuk parsing data response dari digipos
"""
    CONFIG_FILE.write_text(default_config)
    loguru.logger.info(f"Generated default config file at {CONFIG_FILE}")


# test purposes
# if __name__ == "__main__":
#     generate_default_config_file()
