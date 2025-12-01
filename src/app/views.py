from models.dao import DAO
from models.user import Usuario, UsuarioDAO
from models.email import Email, EmailDAO
from models.adm import Admin, AdminDAO
import bcrypt

class View:
    @staticmethod
    def setup_db():
        DAO.setup_db()

    @staticmethod
    def autenticar(email, senha):
        data = View.email_listar(email)
        if data == None:
            return None

        if data.get_table() == "users":
            usuario = View.usuario_listar_id(data.get_fk())
            if bcrypt.checkpw(senha.encode(), usuario.get_senha()):
                return usuario
        elif data.get_table() == "admins":
            admin = View.admin_listar_id(data.get_fk())
            if bcrypt.checkpw(senha.encode(), admin.get_senha()):
                return admin

    @staticmethod
    def email_listar(email):
        result = EmailDAO.email_listar(email)
        if result == None:
            return None
        if not result[1] == None:
            return Email(0, result[0], result[1], "users")
        return Email(0, result[0], result[2], "admins")
    
    @staticmethod
    def inserir_usuario(nome, email, senha, descricao, matematica, portugues, beta):
        u = Usuario(0, nome, senha, matematica, portugues, beta, desc=descricao)
        user_id = UsuarioDAO.salvar(u)
        e = Email(0, email, user_id, "users")
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
        e = Email(0, email, adm_id, "admins")
        email_id = EmailDAO.salvar(e)
        if email_id == None:
            adm_id = None
        return adm_id

    @staticmethod
    def minimo_admin():
        if len(View.admin_listar()) == 0:
            View.inserir_admin("admin", "admin@mail.com", "123")