import streamlit as st
from views import View
from pathlib import Path
import pandas as pd
import json
from PIL import Image
import io
import base64

class AdminUI:
    CWD = Path.cwd()
    @staticmethod
    def fill(session_name, default=""):
        if session_name not in st.session_state:
            return default
        return st.session_state[session_name]
    
    @classmethod
    def main(cls):
        tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Gerenciar Questões", "Gerenciar Administradores", "Sair"])
        with tab1: cls.visao_geral()
        with tab2: cls.questoes()
        with tab3: cls.admins()
        with tab4: cls.sair()

    @classmethod
    def visao_geral(cls):
        categoria = st.selectbox("Categoria", ["Matemática", "Português", "Administradores"], key="cat_geral")

        if categoria == "Administradores":
            entradas = View.admin_listar()
            cls.generate_adm_table(entradas)
        else:
            entradas = View.questoes_listar_categoria(1 if categoria == "Português" else 0)
            if len(entradas) == 0: st.write("Nenhuma questão cadastrada")
            else:
                cls.generate_question_table(entradas)
                
    @classmethod
    def questoes(cls):
        tab1, tab2, tab3 = st.tabs(["Criar", "Editar", "Excluir"])
        with tab1: cls.questoes_add()
        with tab2: cls.questoes_edit()
        with tab3: cls.questoes_del()

    @classmethod
    def questoes_add(cls):
        cls.questao_form()

    @classmethod
    def questoes_edit(cls):
        id_val = st.text_input("insira o ID da questão", key="edit_id")
        if id_val:
            questoes = View.questoes_listar_id(int(id_val))
            if questoes == None: st.write("Nenhuma questão com esse ID")
            else:
                cls.questao_form(id_val, questoes)

    @classmethod
    def questoes_del(cls):
        id_val = st.text_input("insira o ID da questão", key="del_id")
        if id_val:
            questoes = View.questoes_listar_id(int(id_val))

            if questoes == None: st.write("Nenhuma questão com esse ID")
            else:
                cls.generate_question_table([questoes])
            if st.button("Deletar", key="del_q"):
                if View.questoes_excluir_id(int(id_val)):
                    st.success("Questão removida.")
                else:
                    st.warning("Questão não foi removida.")

    @classmethod
    def questao_form(cls, id=None, obj=None):
        categoria = st.selectbox("Categoria", ["Matemática", "Português"], index=obj.get_cat() if not obj is None else 0, key=f"cat-{id}")
        texto = st.text_area("Texto", key=f"text-{id}", value=obj.get_text() if not obj is None else "")
        has_img = False
        if not obj is None:
            col1, col2 = st.columns(2)
            with col1:
                imagem = st.file_uploader("Imagem", ["png", "jpg", "jpeg"], False, key=f"img-{id}",)
            with col2:
                img_bytes = obj.get_pic()
                if img_bytes:
                    b64_bytes = img_bytes.encode("utf-8")
                    img_bytes = base64.b64decode(b64_bytes)
                    buffer = io.BytesIO(img_bytes)
                    st.write("Imagem:")
                    st.image(buffer, width=100)
                    has_img = True
            obj_dict = json.loads(obj.get_alt())
        else:
            imagem = st.file_uploader("Imagem", ["png", "jpg", "jpeg"], False, key=f"img-{id}",)

        qa = st.text_input("Alternativa 1", key=f"alt1-{id}", value=obj_dict.get("0") if not obj is None else "")
        qb = st.text_input("Alternativa 2", key=f"alt2-{id}", value=obj_dict.get("1") if not obj is None else "")
        qc = st.text_input("Alternativa 3", key=f"alt3-{id}", value=obj_dict.get("2") if not obj is None else "")
        qd = st.text_input("Alternativa 4", key=f"alt4-{id}", value=obj_dict.get("3") if not obj is None else "")
        qe = st.text_input("Alternativa 5", key=f"alt5-{id}", value=obj_dict.get("4") if not obj is None else "")
        alternativa_correta = st.number_input("Alternativa Correta", 1, 5, key=f"c-{id}", value=obj.get_c_alt() if not obj is None else 1)

        if st.button("Enviar", key=f"sub-{id}"):
            fail = ""
            if categoria == "Matemática":
                categoria = 0
            else:
                categoria = 1

            final_image = ""
            mime_type = ""
            if imagem:
                image = Image.open(imagem)
                mime_type = image.format.lower()
                buffer = io.BytesIO()
                image.save(buffer, format=image.format)
                blob_image = buffer.getvalue()
                final_image = base64.b64encode(blob_image).decode("utf-8")
                
            json_alt = {}
            can_fail = False
            for idx, alt in enumerate([qa, qb, qc, qd, qe]):
                if alt:
                    if can_fail:
                        fail = "Preencha na ordem correta"
                    json_alt[idx] = alt
                else:
                    can_fail = True
            
            if alternativa_correta > len(json_alt):
                fail = "Alternativa deve estar entre o total de opções"

            if not texto and not (imagem) and not has_img:
                fail = "Informe pelo menos um texto ou uma imagem"

            if len(json_alt) <= 1:
                fail = "Insira pelo menos duas alternativas"

            if fail:
                st.warning(fail)
            else:
                if id == None:
                    if View.inserir_questao(categoria, json_alt, alternativa_correta, texto, final_image, mime_type, st.session_state.adm_id):
                        st.success("Questão adicionada!")
                    else:
                        st.warning("Questão não foi criada.")
                else:
                    if View.editar_questao_id(id, categoria, json_alt, alternativa_correta, texto, final_image, mime_type, st.session_state.adm_id):
                        st.success("Questão editada!")
                    else:
                        st.warning("Questão não foi editada.")

    @classmethod
    def admins(cls):
        tab1, tab2, tab3 = st.tabs(["Criar", "Editar", "Excluir"])
        with tab1: cls.admins_add()
        with tab2: cls.admins_edit()
        with tab3: cls.admins_del()

    @classmethod
    def admins_add(cls):
        cls.admin_form()

    @classmethod
    def admins_edit(cls):
        id_val = st.text_input("insira o ID do usuário", key="edit_usuario")
        if id_val:
            admins = View.admin_listar_id(int(id_val))
            if admins == None: st.write("Nenhum administrador com esse ID")
            else:
                cls.admin_form(int(id_val), admins)
            
    @classmethod
    def admins_del(cls):
        id_val = st.text_input("insira o ID do usuário", key="del_usuario")
        if id_val:
            admins = View.admin_listar_id(int(id_val))

            if admins == None: st.write("Nenhum administrador com esse ID")
            else:
                cls.generate_adm_table([admins])
            if st.button("Deletar", key="d_usuario"):
                if id_val == "1":
                    st.warning("Não pode deletar o ADMIN ROOT")
                else:
                    if View.admins_excluir_id(int(id_val)):
                        st.success("Administrador excluído.")
                    else:
                        st.warning("Administrador não foi excluido.")

    @classmethod
    def admin_form(cls, id=None, obj=None):
        defemail = ""
        if not obj is None:
            defemail = View.admin_email(id).get_email()
        nome = st.text_input("Nome", key=f"nome-{id}", value=obj.get_nome() if not obj is None else "")
        if not id == 1:
            email = st.text_input("E-mail", key=f"admemail-{id}", value=defemail if not obj is None else "")
        else:
            email = "admin@mail.com"
        senha = st.text_input("Senha", type="password", key=f"senha-{id}")

        if st.button("Enviar", key=f"enviar_usuario-{id}"):
            if senha == "":
                st.warning("Insira uma senha")
            else:
                if nome == "":
                    st.warning("Insira um nome")
                else:
                    if id == None:
                        email_obj = View.email_listar(email)
                        if not email_obj is None:
                            st.warning("Email em uso")
                        else:
                            if View.inserir_admin(nome, email, senha):
                                st.success("Administrador criado!")
                            else:
                                st.warning("Administrador não criado.")
                    else:
                        if View.editar_admin_id(id, nome, email, senha):
                            st.success("Administrador editado!")
                        else:
                            st.warning("Administrador não foi editado.")

    @staticmethod
    def sair():
        if st.button("Sair"):
            st.session_state.screen = "login"

    @staticmethod
    def generate_question_table(questoes, filter=lambda x: False):
        mapping = {
            "0": "A",
            "1": "B",
            "2": "C",
            "3": "D",
            "4": "E",
        }

        rows = ""
        for obj in questoes:
            if filter(obj):
                continue
            base64_string = obj.get_pic()
            if obj.get_text():
                text = obj.get_text()
                if len(text) > 30:
                    html_enunciado = text[:30] + "..."
                else:
                    html_enunciado = text
            else:
                html_enunciado = f'<img src="data:image/png;base64,{base64_string}" width="120">'
            
            obj_alts = json.loads(obj.get_alt())
            values = ""
            for i in obj_alts:
                attr = "background-color:rgba(0,255,0,0.3); border-radius:15px;" if int(i) + 1 == obj.get_c_alt() else ""
                values += f'<li style="margin-left:0;{attr}">{mapping[i]}) {obj_alts[i]}</li>'
            alternativas = f"""<ul style='list-style-type:none;'>
                {values}
            </ul>"""
            
            c = View.admin_listar_id(obj.get_added_by())
            rows += f"""<tr>
                <td>{obj.get_id()}</td>
                <td>{"Matemática" if obj.get_cat() == 0 else "Português"}</td>
                <td>{html_enunciado}</td>
                <td>{alternativas}</td>
                <td>{c.get_nome()}</td>
            </tr>\n"""
            
        code = f"""<table style='width: 100%;'>
                        <tr>
                            <th>ID</th>
                            <th>Categoria</th>
                            <th>Enunciado</th>
                            <th>Alternativas</th>
                            <th>Criador</th>
                        </tr>
                        {rows}
</table>"""
        st.markdown(code, unsafe_allow_html=True)

    @staticmethod
    def generate_adm_table(adms, filter=lambda x: False):
        rows = ""
        for obj in adms:
            if filter(obj):
                continue
            
            email = View.admin_email(obj.get_id())

            rows += f"""<tr>
                <td>{obj.get_id()}</td>
                <td>{obj.get_nome()}</td>
                <td>{email.get_email()}</td>
            </tr>\n"""
            
        code = f"""<table style='width: 100%;'>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Email</th>
                        </tr>
                        {rows}
</table>"""
        st.markdown(code, unsafe_allow_html=True)