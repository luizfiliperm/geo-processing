from domains.state_enum import State

class City:
    def __init__(
        self,
        id: int = None,
        name: str = "",
        state: State = None,
        country_id: int = None,
        latitude: float = None,
        longitude: float = None
    ):
        self.id = id
        self.name = name
        self.state = state
        self.country_id = country_id
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return (f"City(id={self.id}, name='{self.name}', state={self.state}, "
                f"country_id={self.country_id}, latitude={self.latitude}, longitude={self.longitude})")
