from pathlib import Path

import yaml


class ConfigurationError(Exception):
    pass


class Config:
    def __init__(self, cfg_file):
        self._cfg = self._load_cfg(cfg_file)

    def _load_cfg(self, cfg_file):
        if not Path(cfg_file).exists():
            raise FileNotFoundError(f"{cfg_file} does not exist.")

        with open(cfg_file, "r") as f:
            cfg = yaml.safe_load(f)

        # check whether config contains either pedestrian_csv_url or pedestrian_api_url
        if not cfg.get("pedestrian_csv_url") and not cfg.get("pedestrian_api_url"):
            raise ConfigurationError(
                f"You must provide at least one of either pedestrian_csv_url or pedestrian_api_url."
            )

        return cfg

    def __getitem__(self, key):
        return self._cfg.get(key)
