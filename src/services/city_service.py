from domains.city import City
from db_sqlite import get_connection
from domains.state_enum import State

class CityService:
    def __init__(self):
        self.conn = get_connection()

    def validate(self, city: City):
        errors = []
        if not city.name or not city.name.strip():
            errors.append("O nome da cidade não pode ser vazio.")
        if not city.state:
            errors.append("O estado deve ser selecionado.")
        if not city.country_id:
            errors.append("O país deve ser selecionado.")
        if city.latitude is None or not (-90 <= city.latitude <= 90):
            errors.append("Latitude inválida. Deve estar entre -90 e 90.")
        if city.longitude is None or not (-180 <= city.longitude <= 180):
            errors.append("Longitude inválida. Deve estar entre -180 e 180.")

        if errors:
            raise ValueError(" | ".join(errors))

    def save(self, city: City) -> City:
        self.validate(city)
        cursor = self.conn.cursor()
        if city.id:  # update
            cursor.execute("""
                UPDATE city
                SET name = ?, state = ?, country_id = ?, latitude = ?, longitude = ?
                WHERE id = ?
            """, (city.name, city.state.name if city.state else None, city.country_id,
                  city.latitude, city.longitude, city.id))
        else:  # insert
            cursor.execute("""
                INSERT INTO city (name, state, country_id, latitude, longitude)
                VALUES (?, ?, ?, ?, ?)
            """, (city.name, city.state.name if city.state else None, city.country_id,
                  city.latitude, city.longitude))
            city.id = cursor.lastrowid
        self.conn.commit()
        return city

    def delete(self, city_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM city WHERE id = ?", (city_id,))
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, state, country_id, latitude, longitude FROM city")
        rows = cursor.fetchall()
        cities = []
        for r in rows:
            state_enum = State[r[2]] if r[2] else None
            cities.append(City(id=r[0], name=r[1], state=state_enum,
                               country_id=r[3], latitude=r[4], longitude=r[5]))
        return cities

    def get_by_id(self, city_id: int) -> City:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, state, country_id, latitude, longitude FROM city WHERE id = ?", (city_id,))
        r = cursor.fetchone()
        if not r:
            return None
        state_enum = State[r[2]] if r[2] else None
        return City(id=r[0], name=r[1], state=state_enum, country_id=r[3], latitude=r[4], longitude=r[5])
    
  #  def get_cities():
   #     """Retorna todas as cidades como lista de dicionários"""
    #    conn = get_connection()
     #   cursor = conn.cursor()
      #  cursor.execute("SELECT id, name, state, country_id, latitude, longitude FROM City")
       # rows = cursor.fetchall()
        #conn.close()
       # return [
       #     {
       #         "id": r[0],
       #         "name": r[1],
       #         "state": r[2],
       #         "country_id": r[3],
        #        "latitude": r[4],
         #       "longitude": r[5]
          #  } for r in rows
        #]