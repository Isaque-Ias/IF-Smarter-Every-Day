from models.dao import DAO
import json

class Questao:
    def __init__(self, id, cat, alt, c_alt, text="", pic="", mime_type="", added_by=None):
        self.set_id(id)
        self.set_cat(cat)
        self.set_alt(alt)
        self.set_c_alt(c_alt)
        self.set_text(text)
        self.set_pic(pic)
        self.set_mime_type(mime_type)
        self.set_added_by(added_by)
        
    def __str__(self):
        return f"{self.__cat}-{self.__alt}-{self.__c_alt}-{self.__text}-{self.__pic}-{self.__mime_type}-{self.__added_by}"
    
    def get_id(self): return self.__id
    def get_cat(self): return self.__cat
    def get_alt(self): return self.__alt
    def get_c_alt(self): return self.__c_alt
    def get_text(self): return self.__text
    def get_pic(self): return self.__pic
    def get_mime_type(self): return self.__mime_type
    def get_added_by(self): return self.__added_by

    def set_id(self, id): self.__id = id
    def set_cat(self, cat):
        if not isinstance(cat, int): raise TypeError("Categoria inválida")
        self.__cat = cat
    def set_alt(self, alt):
        if alt == "": raise ValueError("Alternativas inválidas")
        self.__alt = alt
    def set_c_alt(self, c_alt):
        if c_alt == "": raise ValueError("Alternativa correta inválida")
        if not isinstance(c_alt, int): raise TypeError("Alternativa não é um número")
        if c_alt <= 0 or c_alt > len(self.get_alt()): raise ValueError("Alternativa não está no alcance das opções")
        self.__c_alt = c_alt
    def set_text(self, text):
        self.__text = text
    def set_pic(self, pic):
        self.__pic = pic
    def set_mime_type(self, mime_type):
        self.__mime_type = mime_type
    def set_added_by(self, added_by):
        self.__added_by = added_by
    
    def to_sqlite(self):
        values_array = [
            self.get_cat(),
            self.get_text(),
            self.get_pic(),
            self.get_mime_type(),
            json.dumps(self.get_alt()),
            self.get_c_alt(),
            self.get_added_by()
        ]
        return values_array

class QuestaoDAO(DAO):
    table = "questions"

    @classmethod
    def salvar(cls, obj):
        conn = cls.get_connection()
        cursor = conn.cursor()

        question_data = obj.to_sqlite()

        cursor.execute(f'INSERT OR IGNORE INTO questions (category, text, picture, picture_mime_type, alternatives, correct_alternative, added_by) VALUES (?, ?, ?, ?, ?, ?, ?)', question_data)

        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            return cursor.lastrowid