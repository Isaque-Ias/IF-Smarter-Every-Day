import streamlit as st
from views import View

class LoginUI:
    def main():
        st.header("Entrar")
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Entrar"):
                c, t = View.autenticar(email, senha)
                if c == None: st.write("E-mail ou senha inválidos")
                else:
                    if t == "user":
                        st.session_state.tutorial = False
                        st.session_state.usuario_id = c.get_id()
                        st.session_state.screen = "course"
                    else:
                        st.session_state.adm_id = c.get_id()
                        st.session_state.screen = "adm_hub"

                    st.rerun()

        with col2:
            if st.button("Criar conta"):
                st.session_state.pop("email", "fail")
                st.session_state.pop("senha", "fail")
                st.session_state.pop("nome", "fail")
                st.session_state.pop("descricao", "fail")
                st.session_state.pop("matematica", "fail")
                st.session_state.pop("portugues", "fail")
                st.session_state.pop("beta", "fail")
                st.session_state.pop("sign_step", "fail")
                st.session_state.screen = "signin"
                st.rerun()