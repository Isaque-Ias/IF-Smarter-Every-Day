import bcrypt
from models.dao import DAO

class Admin:
    def __init__(self, id, nome, senha):
        self.set_id(id)
        self.set_nome(nome)
        self.set_senha(senha)
        
    def __str__(self):
        return f"{self.__id}-{self.__nome}-{self.__senha}"

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_senha(self): return self.__senha

    def set_id(self, id): self.__id = id
    def set_nome(self, nome):
        if nome == "": raise ValueError("Nome inválido")
        self.__nome = nome
    def set_senha(self, senha):
        if senha == "": raise ValueError("Senha inválida")
        if isinstance(senha, bytes):
            self.__senha = senha
            return
        self.__senha = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    
    def to_sqlite(self):
        values_array = [
            self.get_nome(),
            self.get_senha()
        ]
        return values_array
        
class AdminDAO(DAO):
    table = "admins"

    @classmethod
    def salvar(cls, obj):
        conn = cls.get_connection()
        cursor = conn.cursor()

        user_data = obj.to_sqlite()

        cursor.execute('INSERT OR IGNORE INTO admins (name, password) VALUES (?, ?)', user_data)

        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return cursor.lastrowid