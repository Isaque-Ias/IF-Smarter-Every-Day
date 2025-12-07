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
            if usuario == None:
                return None, None
            if bcrypt.checkpw(senha.encode(), usuario.get_senha()):
                return usuario, "user"
        else:
            admin = View.admin_listar_id(data.get_fk())
            if admin == None:
                return None, None
            if bcrypt.checkpw(senha.encode(), admin.get_senha()):
                return admin, "admin"
        return None, None

    @staticmethod
    def email_listar(email):
        result = EmailDAO.email_listar(email)
        if result == None:
            return None
        if not result[1] == None:
            return Email(result[0], result[1], "users")
        return Email(result[0], result[2], "admins")
    
    @staticmethod
    def admin_email(id):
        result = EmailDAO.listar_admin_id(id)
        if result == None:
            return None
        if not result[1] == None:
            return Email(result[0], result[1], "users")
        return Email(result[0], result[2], "admins")
    
    @staticmethod
    def user_email(id):
        result = EmailDAO.listar_user_id(id)
        if result == None:
            return None
        if not result[1] == None:
            return Email(result[0], result[1], "users")
        return Email(result[0], result[2], "admins")
    
    @staticmethod
    def inserir_usuario(nome, email, senha, descricao, matematica, portugues, beta):
        u = Usuario(0, nome, senha, matematica, portugues, desc=descricao, beta=beta)
        user_id = UsuarioDAO.salvar(u, email)
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
        query = AdminDAO.listar()

        if query == None:
            return None
        
        objects = []
        for element in query:
            objects.append(Admin(element[0], element[1], element[2]))
        return objects
    
    @staticmethod
    def inserir_admin(nome, email, senha):
        adm = Admin(0, nome, senha)
        adm_id = AdminDAO.salvar(adm, email)
        return adm_id

    def inserir_questao(cat, title, alt, c_alt, text, pic, mime_type, adder):
        q = Questao(0, cat, title, alt, c_alt, text, pic, mime_type, adder)
        q_id = QuestaoDAO.salvar(q)
        return q_id

    @staticmethod
    def minimo_admin():
        if len(View.admin_listar()) == 0:
            View.inserir_admin("admin", "admin@mail.com", "123")

    @staticmethod
    def questoes_listar():
        query = QuestaoDAO.listar()

        if query == None:
            return None
        
        objects = []
        for element in query:
            objects.append(Questao(element[0], element[1], element[2], element[6], element[7], element[3], element[4], element[5], element[8]))
        return objects

    @staticmethod
    def questoes_listar_categoria(categoria):
        query = QuestaoDAO.listar_categoria(categoria)

        if query == None:
            return None

        objects = []
        for element in query:
            objects.append(Questao(element[0], element[1], element[2], element[6], element[7], element[3], element[4], element[5], element[8]))
        return objects

    @staticmethod
    def questoes_listar_id(id):
        element = QuestaoDAO.listar_id(id)
        
        if element == None:
            return None
            
        object = Questao(element[0], element[1], element[2], element[6], element[7], element[3], element[4], element[5], element[8])
        return object

    @staticmethod
    def questoes_excluir_id(id):
        success = QuestaoDAO.excluir_id(id)
        return success

    @staticmethod
    def admins_excluir_id(id):
        success = AdminDAO.excluir_id(id)
        return success

    @staticmethod
    def users_excluir_id(id):
        success = UsuarioDAO.excluir_id(id)
        return success

    @staticmethod
    def editar_questao_id(id, cat, title, alt, c_alt, text, pic, mime_type, adder):
        q = Questao(id, cat, title, alt, c_alt, text, pic, mime_type, adder)
        success = QuestaoDAO.edit_id(id, q)
        return success

    @staticmethod
    def editar_usuario_id(id, nome, email, senha, matematica, portugues, xp_mat, xp_pt, descricao, picture, mime_type, beta):
        u = Usuario(id, nome, senha, matematica, portugues, xp_mat, xp_pt, descricao, picture, mime_type, beta)
        success = UsuarioDAO.edit_id(id, u, email)
        return success

    @staticmethod
    def editar_admin_id(id, nome, email, senha):
        q = Admin(id, nome, senha)
        success = AdminDAO.edit_id(id, q, email)
        return success

    @staticmethod
    def set_course_progress(id, question):
        return UsuarioDAO.add_progress(id, question)

    @staticmethod
    def get_progress(id, question):
        return UsuarioDAO.get_progress(id, question)
    
    @staticmethod
    def set_course(id, course):
        return UsuarioDAO.set_course(id, course)
    
    @staticmethod
    def set_beta(id, value):
        return UsuarioDAO.set_beta(id, value)