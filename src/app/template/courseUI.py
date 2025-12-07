import streamlit as st
from views import View
from pathlib import Path
from math import sin, cos
import json
import io
import base64

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

        if st.button("Voltar"):
            st.session_state.screen = "perfil"
            st.session_state.perfil_id = st.session_state.usuario_id
            st.rerun()

        if st.session_state.course == "mat":
            cls.course(0)
        else:
            cls.course(1)
            
    @classmethod
    def course(cls, cat):
        questoes = View.questoes_listar_categoria(cat)

        if "tutorial" in st.session_state:
            if st.session_state.tutorial == True:
                st.header("Escolha uma questão e faça-a!")
        st.divider()
        for idx, questao in enumerate(questoes):
            _, col1, col2, col3, col4, _ = st.columns([1 + int(max(0, 5 * sin(idx / 3) ** 2)), 4, 5, 5, 4, 1 + int(max(0, 5 * cos(idx / 3) ** 2))])
            
            completed = View.get_progress(st.session_state.usuario_id, questao.get_id())
            
            with col1:
                st.write(f"Questão: {idx + 1}")
            with col2:
                if completed:
                    st.write("Feito!")
                else:
                    st.write("Incompleto...")
            with col3:
                if not questao.get_text() == "":
                    st.write(questao.get_title())
                else:
                    base64_string = questao.get_pic()
                    html_enunciado = f'<img src="data:image/png;base64,{base64_string}" width="120" style="border-radius:15px;">'
                    st.markdown(html_enunciado, unsafe_allow_html=True)
            with col4:
                button_text = "Fazer"
                if completed:
                    button_text = "Refazer"
                if st.button(button_text, key=f'do_q_{idx}'):
                    st.session_state.screen = "questao"
                    st.session_state.question_value = questao.get_id()
                    st.rerun()
            st.divider()

    @classmethod
    def question(cls):
        question = View.questoes_listar_id(st.session_state.question_value)
        if question == None:
            st.header("Questão não encontrada.")
            if st.button("Voltar", key="question-voltar"):
                st.session_state.screen = "course"
                st.rerun()
            
        else:
            mappings = {
                "0": "A",
                "1": "B",
                "2": "C",
                "3": "D",
                "4": "E",
            }
            st.markdown(
                f"<h1 style='text-align: center;'>{question.get_title()}</h1>",
                unsafe_allow_html=True
            )
            st.divider()
            if st.button("Voltar para o curso", key="question-voltar"):
                st.session_state.screen = "course"
                st.rerun()
            st.divider()
            img_bytes = question.get_pic()
            if img_bytes:
                    b64_bytes = img_bytes.encode("utf-8")
                    img_bytes = base64.b64decode(b64_bytes)
                    buffer = io.BytesIO(img_bytes)
                    st.image(buffer)
            st.write(question.get_text())
            alternatives = json.loads(question.get_alt())
            alternative = 0
            for idx, alt in enumerate(alternatives):
                if st.button(f"{mappings[alt]}) {alternatives[alt]}"):
                    alternative = idx + 1
            if alternative != 0:
                if question.get_c_alt() == alternative:
                    st.session_state.screen = "result"
                    st.session_state.correct = True
                else:
                    st.session_state.screen = "result"
                    st.session_state.correct = False
                if View.set_course_progress(st.session_state.usuario_id, st.session_state.question_value):
                    st.rerun()
                else:
                    st.warning("Erro no sistema...")

    def result():
        result_value = st.session_state.correct
        if result_value:
            st.header("Parabéns!")
            st.write("Você acertou a questão!")
        else:
            st.header("Que pena...")
            st.write("Infelizmente você errou a questão...")

        if st.button("Continuar"):
            st.session_state.screen = "course"
            if "tutorial" in st.session_state:
                if st.session_state.tutorial == True:
                    st.session_state.tutorial = None
            st.rerun()