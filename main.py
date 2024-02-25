from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3
from pathlib import Path
from create_database import setup_database
import secrets
import hashlib

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)
jwt = JWTManager(app)

class Database:
    DB_NAME = 'progress_tracker.db'

    def __init__(self):
        db_location = Path(self.DB_NAME)

        if not db_location.exists():
            setup_database()

    def connect(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        self.connect()
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        return result

class API:
    def __init__(self, db: Database):
        self.db: Database = db
    
    def get_name(self, id, query):
        try:
            result = self.db.execute_query(query, (str(id)))
            return {'name': result[0][0]}, 200
        except Exception as e:
            return {'error': str(e)}, 500

class SubjectsAPI(API):
    def get_name(self, id):
        query = "SELECT SubjectName FROM Subjects WHERE SubjectID=?"

        return super().get_name(id, query)

    def get_all_subjects(self):
        query = "SELECT * FROM Subjects"
        result = self.db.execute_query(query)
        return {'subjects': result}, 200

class TopicsAPI(API):
    def get_name(self, id):
        query = "SELECT TopicName FROM Topics WHERE TopicID=?"

        return super().get_name(id, query)

    def get_topics(self, subject_id):
        query = "SELECT TopicID, TopicName FROM Topics WHERE SubjectID=?"
        result = self.db.execute_query(query, (subject_id))

class UsersAPI(API):
    # def get_all_users(self):
    #     query = "SELECT * FROM Users"
    #     result = self.db.execute_query(query)
    #     return {'data': result}, 200

    def __generate_salt(self):
        return secrets.token_hex(16)

    def __hash_password(self, password: str, salt: str):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

    def create_user(self, username: str, password: str):
        salt = self.__generate_salt()
        password_hash = self.__hash_password(password, salt)
        query = """
            INSERT INTO Users (Username, PasswordHash, Salt)
            VALUES (?, ?, ?)
        """
        try:
            self.db.execute_query(query, (username, password_hash, salt))
            return {'message': f'User {username} created successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

    def login(self, username: str, password: str):
        query = "SELECT PasswordHash, Salt FROM Users WHERE Username=?"
        try:
            result = self.db.execute_query(query, (username,))
            real_password_hash = result[0][0]
            salt = result[0][1]
        except Exception as e:
            return {'error': str(e)}, 500
        
        password_hash = self.__hash_password(password, salt)
        if password_hash == real_password_hash:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        else:
            return {'message': 'Invalid username or password'}, 401
        

class UserSubjectsAPI(API):
    def create_user_subject(self, user_id: int, subject_ids: tuple):
        query = """
            INSERT INTO User_Subjects (UserID, SubjectID, ConfidenceLevel, DateLastReviewed, SubjectCompleted)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (data['UserID'], data['SubjectID'], data['ConfidenceLevel'], data['DateLastReviewed'], data['SubjectCompleted'])
        try:
            self.db.execute_query(query, params)
            return {'message': 'User_Subject created successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

    def get_user_subjects(self, user_id):
        query = "SELECT * FROM User_Subjects WHERE UserID = ?"
        result = self.db.execute_query(query, (user_id,))
        if not result:
            return {'error': 'User not found'}, 404
        return {'data': result}, 200

class UserTopicProgress(API):
    def add_topic_progress(self, user_id: int, subject_id: int, topics: dict):
        pass

    def get_ordered_list(self, user_id: int, subject_id: int):
        pass


db = Database()
subjects_api = SubjectsAPI(db)
users_api = UsersAPI(db)
topics_api = TopicsAPI(db)
user_subjects_api = UserSubjectsAPI(db)
user_topic_progress_api = UserTopicProgress(db)

@app.route('/get_subject_name/<int:subject_id>', methods=['GET'])
def get_subject_name(subject_id: int):
    return subjects_api.get_name(subject_id)

@app.route('/get_all_subjects', methods=['GET'])
def get_all_subjects():
    return subjects_api.get_all_subjects()

@app.route('/get_topic_name/<int:subject_id>', methods=['GET'])
def get_topic_name(subject_id: int):
    return topics_api.get_name(subject_id)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    return users_api.create_user(data['username'], data['password'])

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    return users_api.login(data['username'], data['password'])

# @app.route('/user_subjects', methods=['POST'])
# def create_user_subject():
#     data = request.json
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400
#     return user_subjects_api.create_user_subject(data)

# @app.route('/user_subjects/<int:user_id>', methods=['GET'])
# def get_user_subjects(user_id):
#     return user_subjects_api.get_user_subjects(user_id)

if __name__ == '__main__':
    app.run(debug=True)
