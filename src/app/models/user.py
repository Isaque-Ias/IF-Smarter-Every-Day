import bcrypt
from models.dao import DAO
from models.error import LengthError

class Usuario:
    def __init__(self, id, nome, senha, mat, pt, xp_mat=0, xp_pt=0, desc="", pic="", pic_mime="", beta=False):
        self.set_id(id)
        self.set_nome(nome)
        self.set_senha(senha)
        self.set_desc(desc)
        self.set_mat(mat)
        self.set_pt(pt)
        self.set_beta(beta)
        self.set_xp_mat(xp_mat)
        self.set_xp_pt(xp_pt)
        self.set_pic(pic)
        self.set_pic_mime(pic_mime)

    def __str__(self):
        return f"{self.__id}-{self.__nome}-{self.__senha}-{self.__desc}-{self.__mat}-{self.__pt}-{self.__xp_mat}-{self.__xp_pt}-{self.__beta}-{self.__pic}-{self.__pic_mime}"

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_senha(self): return self.__senha
    def get_desc(self): return self.__desc
    def get_mat(self): return self.__mat
    def get_pt(self): return self.__pt
    def get_xp_mat(self): return self.__xp_mat
    def get_xp_pt(self): return self.__xp_pt
    def get_pic(self): return self.__pic
    def get_pic_mime(self): return self.__pic_mime
    def get_beta(self): return self.__beta

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
    def set_mat(self, mat):
        self.__mat = mat
    def set_pt(self, pt):
        self.__pt = pt
    def set_xp_mat(self, xp_mat):
        if xp_mat == "": raise ValueError("XP Inválido")
        if not isinstance(xp_mat, int): raise TypeError("Deve ser um inteiro")
        self.__xp_mat = xp_mat
    def set_xp_pt(self, xp_pt):
        if xp_pt == "": raise ValueError("XP Inválido")
        if not isinstance(xp_pt, int): raise TypeError("Deve ser um inteiro")
        self.__xp_pt = xp_pt
    def set_desc(self, desc):
        if not isinstance(desc, str): raise TypeError("A descrição deve ser um texto válido")
        if len(desc) > 1000: raise LengthError("Limite de caracteres excedido")
        self.__desc = desc
    def set_pic(self, pic):
        self.__pic = pic
    def set_pic_mime(self, pic_mime):
        self.__pic_mime = pic_mime
    def set_beta(self, beta):
        self.__beta = beta
    
    def to_sqlite(self):
        values_array = [
            self.get_nome(),
            self.get_senha(),
            int(self.get_mat()),
            int(self.get_pt()),
            int(self.get_xp_mat()),
            int(self.get_xp_pt()),
            self.get_desc(),
            self.get_pic(),
            self.get_pic_mime(),
            int(self.get_beta())
        ]
        return values_array
        
class UsuarioDAO(DAO):
    table = "users"

    @classmethod
    def listar_nome(cls, nome):
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE name == ?;
        """, (nome,))
        
        return cursor.fetchone()

    @classmethod
    def salvar(cls, obj):
        conn = cls.get_connection()
        cursor = conn.cursor()

        user_data = obj.to_sqlite()
        cursor.execute('INSERT OR IGNORE INTO users (name, password, enrolled_math, enrolled_pt, xp_math, xp_pt, description, profile_pic, profile_pic_mime, is_beta) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', user_data)
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return cursor.lastrowid