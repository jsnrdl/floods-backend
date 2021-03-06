"""
The `Config` class is used by the `Flask` application for accessing various
bits of application configuration
"""

import os

import yaml

from ccai.singleton import Singleton

# pylint: disable=R0903
class ConfigSingleton(Singleton):
    """Configuration object for the `Flask` application."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    API_KEYS_FILE = os.path.join(BASE_DIR, "../api_keys.yaml")
    MUNIT_CONFIG_FILE = os.path.join(BASE_DIR, "nn/munit/config.yaml")
    MUNIT_CHECKPOINT_FILE = os.path.join(BASE_DIR, "nn/munit/checkpoints/gen_00125000.pt")
    MUNIT_STYLE_FILE = os.path.join(BASE_DIR, "nn/munit/styles/style_high_res.npy")

    API_KEYS_NAME = ["GEO_CODER_API_KEY", "STREET_VIEW_API_KEY"]

    # These variables are populated in __init__
    GEO_CODER_API_KEY = ""
    STREET_VIEW_API_KEY = ""

    def __init__(self) -> None:
        Singleton.__init__(self)
        if os.path.exists(self.API_KEYS_FILE):
            with open(self.API_KEYS_FILE, "r") as api_keys_file:
                keys = yaml.load(api_keys_file, Loader=yaml.FullLoader)  # type: ignore

                for key, value in keys.items():
                    setattr(self, key, value)
        else:
            for key in self.API_KEYS_NAME:
                value = os.environ.get(key, None)

                if value is None:
                    value = ""

                setattr(self, key, value)

        with open(self.MUNIT_CONFIG_FILE, "r") as munit_config_file:
            self.munit_config = yaml.load(munit_config_file, Loader=yaml.FullLoader)  # type: ignore


CONFIG = ConfigSingleton()
