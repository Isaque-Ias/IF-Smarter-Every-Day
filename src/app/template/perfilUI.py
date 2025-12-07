import streamlit as st
from views import View
from PIL import Image
from pathlib import Path
import io
import base64

class PerfilUI:
    CWD = Path.cwd()
    @staticmethod
    def fill(session_name, default=""):
        if session_name not in st.session_state:
            return default
        return st.session_state[session_name]
    
    @classmethod
    def main(cls):
        if "perfil_id" not in st.session_state:
            cls.usuario = None
        else:
            cls.usuario = View.usuario_listar_id(st.session_state.perfil_id)
        if cls.usuario == None:
            st.header("Usuário não encontrado...")
            if st.button("Ir para meu perfil"):
                st.session_state.perfil_id = st.session_state.usuario_id
            if st.button("Deslogar"):
                st.session_state.usuario_id = None
                st.session_state.screen = "login"
        else:
            opcoes = ["Perfil", "Amizades"]
            if cls.usuario.get_beta():
                opcoes.append("Sair do Beta")
            else:
                opcoes.append("Virar Beta")

            if "tutorial" in st.session_state and st.session_state.tutorial == True:
                st.header(f"Olá, {cls.usuario.get_nome()}! Escolha um dos seus cursos nas abas!")
            else:
                opcoes.extend(["Editar Perfil", "Excluir Perfil"])
                if not cls.usuario.get_mat() or not cls.usuario.get_pt():
                    opcoes.append("Novo Curso")
            if cls.usuario.get_mat():
                opcoes.append("Matemática")
            if cls.usuario.get_pt():
                opcoes.append("Português")

            tabs = st.tabs(opcoes)
            for tab_name, tab in zip(opcoes, tabs):
                with tab:
                    if tab_name == "Perfil":
                        PerfilUI.perfil()
                    elif tab_name == "Matemática":
                        PerfilUI.mat()
                    elif tab_name == "Português":
                        PerfilUI.pt()
                    elif tab_name == "Editar Perfil":
                        PerfilUI.editar()
                    elif tab_name == "Excluir Perfil":
                        PerfilUI.excluir()
                    elif tab_name == "Novo Curso":
                        PerfilUI.new_course()
                    elif tab_name == "Amizades":
                        PerfilUI.friends()
                    elif tab_name == "Virar Beta":
                        PerfilUI.beta()
                    elif tab_name == "Sair do Beta":
                        PerfilUI.beta()
                    
    @classmethod
    def perfil(cls):
        st.text(cls.usuario.get_nome())
        img_bytes = cls.usuario.get_pic()
        if img_bytes:
            b64_bytes = img_bytes.encode("utf-8")
            img_bytes = base64.b64decode(b64_bytes)
            img = io.BytesIO(img_bytes)
        else:
            img = Image.open(cls.CWD / "src" / "app" / "images" / "no_profile.png")
        st.image(img, caption="Foto de perfil", width=100)
        if st.button("Sair da conta", key="perfil-sair"):
            st.session_state.usuario_id = None
            st.session_state.screen = "login"
            st.rerun()

    @classmethod
    def mat(cls):
        if st.button("Ir para o curso de matemática"):
            st.session_state.course = "mat"
            st.session_state.screen = "course"
            st.rerun()
        
    @classmethod
    def pt(cls):
        if st.button("Ir para o curso de português"):
            st.session_state.course = "pt"
            st.session_state.screen = "course"
            st.rerun()
        
    @classmethod
    def editar(cls):
        st.text(cls.usuario.get_nome())
        img_bytes = cls.usuario.get_pic()
        if img_bytes:
            b64_bytes = img_bytes.encode("utf-8")
            img_bytes = base64.b64decode(b64_bytes)
            img = io.BytesIO(img_bytes)
        else:
            img = Image.open(cls.CWD / "src" / "app" / "images" / "no_profile.png")
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(img, caption="Foto de perfil", width=100)
        with col2:
            imagem = st.file_uploader("Mova Foto de perfil", ["png", "jpg", "jpeg"], False, key=f"img")
        nome = st.text_input("Trocar meu nome", cls.usuario.get_nome())
        descricao = st.text_area("Descrição", cls.usuario.get_desc(), max_chars=100)
        if st.button("Salvar"):
            final_image = ""
            mime_type = ""
            if imagem:
                image = Image.open(imagem)
                mime_type = image.format.lower()
                buffer = io.BytesIO()
                image.save(buffer, format=image.format)
                blob_image = buffer.getvalue()
                final_image = base64.b64encode(blob_image).decode("utf-8")
            email = View.user_email(st.session_state.usuario_id)
            nome_in_system = View.usuario_listar_nome(nome)
            if nome_in_system == None or nome_in_system.get_id() == cls.usuario.get_id():
                if email == None:
                    st.error("Email indisponível")
                else:
                    if View.editar_usuario_id(st.session_state.usuario_id,
                                        nome,
                                        email.get_email(),
                                        cls.usuario.get_senha(),
                                        cls.usuario.get_mat(),
                                        cls.usuario.get_pt(),
                                        cls.usuario.get_xp_mat(),
                                        cls.usuario.get_xp_pt(),
                                        descricao,
                                        final_image,
                                        mime_type,
                                        cls.usuario.get_beta()
                                        ):
                        st.success("Dados atualizados!")
                    else:
                        st.error("Usuário não foi adicioando")
            else:
                st.warning("Nome já está em uso")
        
    @classmethod
    def excluir(cls):
        if st.button("Excluir perfil"):
            if View.users_excluir_id(st.session_state.usuario_id):
                st.session_state.screen = "login"
                st.rerun()
            else:
                st.warning("Erro no sistema...")

    @classmethod
    def new_course(cls):
        if not cls.usuario.get_mat():
            if st.button("Entrar em matemática"):
                View.set_course(cls.usuario.get_id(), 0)
                st.rerun()

        if not cls.usuario.get_pt():
            if st.button("Entrar em português"):
                View.set_course(cls.usuario.get_id(), 1)
                st.rerun()

    @classmethod
    def friends(cls):
        pass

    @classmethod
    def beta(cls):
        beta_val = cls.usuario.get_beta()
        if beta_val:
            if st.button("Deixar de ser Beta"):
                View.set_beta(cls.usuario.get_id(), 0)
                st.rerun()
        else:
            if st.button("Virar Beta"):
                View.set_beta(cls.usuario.get_id(), 1)
                st.rerun()