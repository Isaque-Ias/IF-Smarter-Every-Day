import streamlit as st
from views import View
from PIL import Image
from pathlib import Path

class CourseUI:
    CWD = Path.cwd()
    @staticmethod
    def fill(session_name, default=""):
        if session_name not in st.session_state:
            return default
        return st.session_state[session_name]
    
    @classmethod
    def main(cls):
        cls.usuario = View.usuario_listar_id(st.session_state.usuario_id)
        if not "course" in st.session_state:
            st.session_state.course = "pt"
            if cls.usuario.get_xp_mat() > cls.usuario.get_xp_pt():
                st.session_state.course = "mat"

        if st.button("voltar"):
            st.session_state.screen = "perfil"
            st.rerun()

        if st.session_state.course == "mat":
            cls.course(0)
        else:
            cls.course(1)

    @classmethod
    def perfil(cls):
        st.text(cls.usuario.get_nome())
        img = Image.open(cls.CWD / "src" / "app" / "images" / "no_profile.png")
        st.image(img, caption="Foto de perfil", width=100)

    @classmethod
    def mat(cls):
        st.session_state.course = "mat"
        st.rerun()
        
    @classmethod
    def pt(cls):
        st.session_state.course = "pt"
        st.rerun()
        
    @classmethod
    def course(cls, cat):
        questoes = View.questoes_listar_categoria(cat)
        html_questoes = ""
        for idx, questao in enumerate(questoes):
            message = f"{idx} - {questao.get_text()}"
            html_questoes += f"<li style='margin-left: 0;'>{message}</li>\n"

        st.markdown(f"""
            <ul style='list_style_type: none;'>
                {html_questoes}
            </ul>
""", unsafe_allow_html=True)
        
    @classmethod
    def editar(cls):
        st.text(cls.usuario.get_nome())
        img = Image.open(cls.CWD / "src" / "app" / "images" / "no_profile.png")
        st.image(img, caption="Foto de perfil", width=100)
        
    @classmethod
    def excluir(cls):
        st.text(cls.usuario.get_nome())
        img = Image.open(cls.CWD / "src" / "app" / "images" / "no_profile.png")
        st.image(img, caption="Foto de perfil", width=100)