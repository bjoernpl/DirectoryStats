import json
from pathlib import Path
from typing import Tuple, Dict
import hashlib


class Handler:

    def __init__(self, path):
        path_hash = str(hashlib.md5(str(path.resolve()).encode('utf-8')).hexdigest())
        self._cache_path = Path("cache") / path_hash
        print(self._cache_path.absolute())
        if not self._cache_path.exists():
            self._cache_path.mkdir(parents=True)
        self.stats_file = self._cache_path / "stats.json"
        self.cache_file = self._cache_path / "cache.json"
        self._init_files()

    @staticmethod
    def _create_if_not_exists(file):
        if not file.exists():
            with open(file, 'w') as fp:
                json.dump({}, fp)

    def _init_files(self):
        self._create_if_not_exists(self.stats_file)
        self._create_if_not_exists(self.cache_file)

    @staticmethod
    def _read_json(file):
        with open(file) as f:
            return json.load(f)

    @staticmethod
    def _write_json(obj, file):
        if obj:
            with open(file, 'w') as f:
                json.dump(obj, f, indent=4)

    def _load_data(self) -> Tuple[Dict, Dict]:
        stats = self._read_json(self.stats_file)
        cache = self._read_json(self.cache_file)
        return stats, cache

    def load(self) -> Tuple[Dict, Dict]:
        """
        Loads the stats and cache dicts from memory
        :return: Tuple(stats dict, cache dict)
        """
        return self._load_data()

    def save(self, stats=None, cache=None):
        self._write_json(stats, self.stats_file)
        self._write_json(cache, self.cache_file)
