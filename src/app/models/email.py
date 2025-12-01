from models.dao import DAO

class Email:
    def __init__(self, email, fk, table):
        self.set_email(email)
        self.set_fk(fk)
        self.set_table(table)
        
    def __str__(self):
        return f"{self.__email}-{self.__fk}-{self.__table}"

    def get_email(self): return self.__email
    def get_fk(self): return self.__fk
    def get_table(self): return self.__table

    def set_email(self, email):
        if email == "": raise ValueError("E-mail inválido")
        self.__email = email
    def set_fk(self, fk):
        if fk == "": raise ValueError("Chave estrangeira inválida")
        self.__fk = fk
    def set_table(self, table):
        if table not in ["users", "admins"]: raise ValueError("Tabela inválida")
        self.__table = table
    
    def to_sqlite(self):
        values_array = [
            self.get_email(),
            self.get_fk()
        ]
        return values_array

class EmailDAO(DAO):
    table = "emails"

    @classmethod
    def email_listar(cls, email):
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM emails WHERE email == ?;
        """, (email,))
        
        return cursor.fetchone()

    @classmethod
    def salvar(cls, obj):
        conn = cls.get_connection()
        cursor = conn.cursor()

        user_data = obj.to_sqlite()
        if obj.get_table() == "users":
            attr = "user_id"
        else:
            attr = "admin_id"

        cursor.execute(f'INSERT OR IGNORE INTO emails (email, {attr}) VALUES (?, ?)', user_data)

        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return cursor.lastrowid