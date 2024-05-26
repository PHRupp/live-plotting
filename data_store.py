
import json
from typing import List, Optional

class MyData:

    def __init__(
        self,
        max_size: int = 10,
    ):
        """
        NOTE: Data list goes from [oldest, ..., newest]
        """
        self._max_size: int = max_size
        self._lat_deg: List[float] = []
        self._lon_deg: List[float] = []
        self._alt_m: List[float] = []
        self._time_s: List[float] = []

    def has_data(self):
        return len(self._lat_deg) > 0

    def update(
        self,
        new_lat_deg: float,
        new_lon_deg: float,
        new_alt_m: float,
        new_time_s: float,
    ):
        # Update position history
        self._lat_deg.append(new_lat_deg)
        self._lon_deg.append(new_lon_deg)
        self._alt_m.append(new_alt_m)
        self._time_s.append(new_time_s)

        # Remove oldest position
        while len(self._lat_deg) > self._max_size:
            del self._lat_deg[0]
            del self._lon_deg[0]
            del self._alt_m[0]
            del self._time_s[0]
        return
    
    def to_dict(self) -> dict:
        return self.__dict__

    def from_dict(self, in_dict: dict):
        if type(in_dict) == dict:
            self.__dict__ = in_dict
        return self

    def to_json_str(self, indent: Optional[int] = None):
        return json.dumps(self.to_dict(), indent=indent)

    def from_json_str(self, json_str: str):
        self.__dict__ = json.loads(json_str)
        return self

class MyConfig:

    def __init__(
        self,
        zoom_factor: int = 10,
        orig_lat: float = 0.0,
        orig_lon: float = 0.0,
    ):
        """
        NOTE: Data list goes from [oldest, ..., newest]
        """
        self._zoom_factor: int = zoom_factor
        self._orig_lat_deg: int = orig_lat
        self._orig_lon_deg: int = orig_lon

    def to_dict(self) -> dict:
        return self.__dict__

    def from_dict(self, in_dict: dict):
        if type(in_dict) == dict:
            self.__dict__ = in_dict
        return self

    def to_json_str(self, indent: Optional[int] = None):
        return json.dumps(self.to_dict(), indent=indent)

    def from_json_str(self, json_str: str):
        self.__dict__ = json.loads(json_str)
        return self
