from db_sqlite import get_connection
from domains.country import Country

class CountryService:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def validate(self, country: Country):
        if not country.name:
            raise ValueError("Nome do país é obrigatório")
        if not country.iso_code or len(country.iso_code) != 2:
            raise ValueError("Código ISO deve ter 2 letras")

        query = "SELECT id FROM Country WHERE (name = ? OR iso_code = ?)"
        self.cursor.execute(query, (country.name, country.iso_code))
        row = self.cursor.fetchone()
        
        if row and (not country.id or row[0] != country.id):
            raise ValueError("Já existe um país com esse nome ou código ISO")

    def save(self, country: Country) -> Country:
        self.validate(country)
        if country.id:
            self.cursor.execute(
                "UPDATE Country SET name = ?, iso_code = ? WHERE id = ?",
                (country.name, country.iso_code, country.id)
            )
        else:
            self.cursor.execute(
                "INSERT INTO Country (name, iso_code) VALUES (?, ?)",
                (country.name, country.iso_code)
            )
            country.id = self.cursor.lastrowid
        self.conn.commit()
        return country

    def get_all(self):
        self.cursor.execute("SELECT id, name, iso_code FROM Country")
        rows = self.cursor.fetchall()
        return [Country(id=row[0], name=row[1], iso_code=row[2]) for row in rows]

    def get_by_id(self, country_id: int):
        self.cursor.execute("SELECT id, name, iso_code FROM Country WHERE id = ?", (country_id,))
        row = self.cursor.fetchone()
        if row:
            return Country(id=row[0], name=row[1], iso_code=row[2])
        return None

    def delete(self, country_id: int):
        self.cursor.execute("DELETE FROM Country WHERE id = ?", (country_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
