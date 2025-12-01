from models.dao import DAO
from models.user import Usuario, UsuarioDAO
from models.email import Email, EmailDAO
from models.adm import Admin, AdminDAO
from models.questao import Questao, QuestaoDAO
import bcrypt

class View:
    @staticmethod
    def setup_db():
        DAO.setup_db()

    @staticmethod
    def autenticar(email, senha):
        data = View.email_listar(email)
        if data == None:
            return None, None

        if data.get_table() == "users":
            usuario = View.usuario_listar_id(data.get_fk())
            if bcrypt.checkpw(senha.encode(), usuario.get_senha()):
                return usuario, "user"
        else:
            admin = View.admin_listar_id(data.get_fk())
            if bcrypt.checkpw(senha.encode(), admin.get_senha()):
                return admin, "admin"

    @staticmethod
    def email_listar(email):
        result = EmailDAO.email_listar(email)
        if result == None:
            return None
        if not result[1] == None:
            return Email(result[0], result[1], "users")
        return Email(result[0], result[2], "admins")
    
    @staticmethod
    def inserir_usuario(nome, email, senha, descricao, matematica, portugues, beta):
        u = Usuario(0, nome, senha, matematica, portugues, beta, desc=descricao)
        user_id = UsuarioDAO.salvar(u)
        e = Email(email, user_id, "users")
        email_id = EmailDAO.salvar(e)
        if email_id == None:
            user_id = None
        return user_id
    
    @staticmethod
    def usuario_listar_id(id):
        result = UsuarioDAO.listar_id(id)
        if result == None:
            return
        return Usuario(*result)
    
    @staticmethod
    def admin_listar_id(id):
        result = AdminDAO.listar_id(id)
        if result == None:
            return
        return Admin(*result)
    
    @staticmethod
    def usuario_listar_nome(nome):
        result = UsuarioDAO.listar_nome(nome)
        if result == None:
            return
        return Usuario(*result)
    
    @staticmethod
    def admin_listar():
        return AdminDAO.listar()
    
    @staticmethod
    def inserir_admin(nome, email, senha):
        adm = Admin(0, nome, senha)
        adm_id = AdminDAO.salvar(adm)
        e = Email(email, adm_id, "admins")
        email_id = EmailDAO.salvar(e)
        if email_id == None:
            adm_id = None
        return adm_id

    def inserir_questao(cat, alt, c_alt, text, pic, mime_type, adder):
        q = Questao(0, cat, alt, c_alt, text, pic, mime_type, adder)
        q_id = QuestaoDAO.salvar(q)
        return q_id

    @staticmethod
    def minimo_admin():
        if len(View.admin_listar()) == 0:
            View.inserir_admin("admin", "admin@mail.com", "123")

    @staticmethod
    def questoes_listar():
        query = QuestaoDAO.listar()
        objects = []
        for element in query:
            objects.append(Questao(element[0], element[1], element[5], element[6], element[2], element[3], element[4], element[7]))
        return objects