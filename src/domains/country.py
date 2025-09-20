class Country:
    def __init__(self, id: int = None, name: str = "", iso_code: str = ""):
        self.id = id
        self.name = name
        self.iso_code = iso_code

    def __repr__(self):
        return f"Country(id={self.id}, name='{self.name}', iso_code='{self.iso_code}')"
