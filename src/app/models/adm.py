import bcrypt
from models.dao import DAO

class Admin:
    def __init__(self, id, nome, email, senha):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_senha(senha)
        
    def __str__(self):
        return f"{self.__id}-{self.__nome}-{self.__email}-{self.__senha}"

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_email(self): return self.__email
    def get_senha(self): return self.__senha

    def set_id(self, id): self.__id = id
    def set_nome(self, nome):
        if nome == "": raise ValueError("Nome inválido")
        self.__nome = nome
    def set_email(self, email):
        if email == "": raise ValueError("E-mail inválido")
        self.__email = email
    def set_senha(self, senha):
        if senha == "": raise ValueError("Senha inválida")
        if isinstance(senha, bytes):
            self.__senha = senha
            return
        self.__senha = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    def set_mat(self, mat):
        self.__mat = mat
    def set_pt(self, pt):
        self.__pt = pt
    def set_xp_mat(self, xp_mat):
        if xp_mat == "": raise ValueError("XP Inválido")
        self.__xp_mat = xp_mat
    def set_xp_pt(self, xp_pt):
        if xp_pt == "": raise ValueError("XP Inválido")
        self.__xp_pt = xp_pt
    def set_pic(self, pic):
        self.__pic = pic
    def set_pic_mime(self, pic_mime):
        self.__pic_mime = pic_mime
    def set_beta(self, beta):
        self.__beta = beta
    
    def to_sqlite(self):
        values_array = [
            self.get_nome(),
            self.get_email(),
            self.get_senha(),
            int(self.get_mat()),
            int(self.get_pt()),
            int(self.get_xp_mat()),
            int(self.get_xp_pt()),
            self.get_pic(),
            self.get_pic_mime(),
            int(self.get_beta())
        ]
        return values_array
        
class UsuarioDAO(DAO):
    table = "users"

    @classmethod
    def listar_email(cls, email):
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE email == ?;
        """, (email,))
        
        return cursor.fetchone()

    @classmethod
    def salvar(cls, obj):
        conn = cls.get_connection()
        cursor = conn.cursor()

        user_data = obj.to_sqlite()

        cursor.execute('INSERT OR IGNORE INTO users (name, email, password, enrolled_math, enrolled_pt, xp_math, xp_pt, profile_pic, profile_pic_mime, is_beta) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', user_data)

        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return cursor.lastrowid