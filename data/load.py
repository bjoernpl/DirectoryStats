import json
from pathlib import Path
from typing import Tuple, Dict


class Handler:

    def __init__(self, path):
        self._cache_path = Path("cache") / str(hash(path))
        print(self._cache_path.absolute())
        if not self._cache_path.exists():
            self._cache_path.mkdir(parents=True)
        self.stats_file = self._cache_path / "stats.json"
        self.cache_file = self._cache_path / "cache.json"
        self._init_files()

    def _init_files(self):
        if not self.stats_file.exists():
            with open(self.stats_file, 'w') as fp:
                json.dump({}, fp)

        if not self.cache_file.exists():
            with open(self.cache_file, 'w') as fp:
                json.dump({}, fp)

    def _load_data(self) -> Tuple[Dict, Dict]:
        with open(self.stats_file) as f:
            stats = json.load(f)
        with open(self.cache_file) as f:
            cache = json.load(f)
        return stats, cache

    def load(self) -> Tuple[Dict, Dict]:
        """
        Loads the stats and cache dicts from memory
        :return: Tuple(stats dict, cache dict)
        """
        return self._load_data()

    def save(self, stats=None, cache=None):
        if stats:
            json.dumps(stats, fp=self.stats_file)

        if cache:
            json.dumps(cache, fp=self.cache_file)
