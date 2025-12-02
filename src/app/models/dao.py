from abc import ABC, abstractmethod
import sqlite3
from pathlib import Path
import os
import sys

class DAO(ABC):
    _objetos = []

    @staticmethod
    def get_connection():
        PATH = Path.cwd()
        DB_DIR = PATH / "src" / "app" / "db"
        DB_PATH = DB_DIR / "app.db"

        DB_DIR.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        return conn

    @classmethod
    def setup_db(cls):
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                enrolled_math INTEGER NOT NULL,
                enrolled_pt INTEGER NOT NULL,
                xp_math INTEGER,
                xp_pt INTEGER,
                description TEXT,
                profile_pic BLOB,
                profile_pic_mime VARCHAR(127),
                is_beta INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS following (
                following_id INTEGER NOT NULL,
                follower_id INTEGER NOT NULL,
                PRIMARY KEY (following_id, follower_id)
                FOREIGN KEY (following_id) REFERENCES users(id),
                FOREIGN KEY (follower_id) REFERENCES users(id)
                CHECK(follower_id != following_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS course_progress (
                question_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                course_point INTEGER NOT NULL,
                completion INTEGER NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category INTEGER NOT NULL,
                text TEXT,
                picture BLOB,
                picture_mime_type VARCHAR(127),
                alternatives TEXT NOT NULL,
                correct_alternative INTEGER NOT NULL,
                added_by INTEGER,
                FOREIGN KEY (added_by) REFERENCES admins(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS redaction_topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                body TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS redactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                writer_id INTEGER NOT NULL,
                body TEXT NOT NULL,
                topic_id INTEGER NOT NULL,
                FOREIGN KEY (writer_id) REFERENCES users(id),
                FOREIGN KEY (topic_id) REFERENCES redaction_topics(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS redaction_feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                redaction_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                FOREIGN KEY (redaction_id) REFERENCES redactions(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                email TEXT NOT NULL UNIQUE,
                user_id INT,
                admin_id INT,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (admin_id) REFERENCES admins(id)
            )
        ''')

        conn.commit()

        conn.close()

    @classmethod
    def listar(cls):
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {cls.table}")
        results = cursor.fetchall()
        
        conn.close()

        return results

    @classmethod
    def listar_id(cls, id):
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {cls.table} WHERE id == ?", (id, ))
        results = cursor.fetchone()
        
        conn.close()

        return results

    @classmethod
    def excluir_id(cls, id):
        conn = cls.get_connection()
        cursor = conn.cursor()

        cursor.execute(f"DELETE FROM {cls.table} WHERE id == ?", (id, ))
        result = cursor.rowcount
        
        conn.commit()
        conn.close()

        return result

    @classmethod
    @abstractmethod
    def abrir(cls):
        pass

    @classmethod
    @abstractmethod
    def salvar(cls):
        pass