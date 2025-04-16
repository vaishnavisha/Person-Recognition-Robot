# import dlib
# import cv2
# import numpy as np
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import base64
# import os
# import pickle
#
# app = Flask(__name__)
# CORS(app)
#
# detector = dlib.get_frontal_face_detector()
# shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
#
# ENCODINGS_DIR = "user-details"
# USER_DETAILS_FILE = "user_details.pkl"
#
# if not os.path.exists(ENCODINGS_DIR):
#     os.makedirs(ENCODINGS_DIR)
#
# def load_user_details():
#     if os.path.exists(USER_DETAILS_FILE):
#         with open(USER_DETAILS_FILE, 'rb') as f:
#             return pickle.load(f)
#     return {}
#
# def save_user_details(user_details):
#     with open(USER_DETAILS_FILE, 'wb') as f:
#         pickle.dump(user_details, f)
#
# def base64_to_image(base64_string):
#     img_data = base64.b64decode(base64_string.split(',')[1])
#     nparr = np.frombuffer(img_data, np.uint8)
#     return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
# def save_face_encoding(user_id, face_encoding):
#     file_path = os.path.join(ENCODINGS_DIR, f"{user_id}.pkl")
#     with open(file_path, 'wb') as f:
#         pickle.dump(face_encoding, f)
#     print(f"Saved encoding for user {user_id} at {file_path}")
#
# def load_face_encoding(user_id):
#     file_path = os.path.join(ENCODINGS_DIR, f"{user_id}.pkl")
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as f:
#             return pickle.load(f)
#     return None
#
# def get_face_encodings(image):
#     dets = detector(image, 1)
#     encodings = []
#     for det in dets:
#         shape = shape_predictor(image, det)
#         face_encoding = np.array(face_rec_model.compute_face_descriptor(image, shape))
#         encodings.append(face_encoding)
#     return encodings
#
# @app.route('/register-user', methods=['POST'])
# def register_user():
#     try:
#         data = request.get_json()
#         user_id = data['user_id']
#         name = data['name']
#         role = data["role"]
#         image_base64 = data['image']
#
#         if not name or not role or not image_base64:
#             return jsonify({"success": False, "message": "Missing required fields: name or role or image"})
#
#         image = base64_to_image(image_base64)
#         rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
#         face_encodings = get_face_encodings(rgb_image)
#         if len(face_encodings) == 0:
#             return jsonify({'success': False, 'message': 'No face detected.'})
#
#         save_face_encoding(user_id, face_encodings[0])
#
#         user_details = load_user_details()
#
#         if role == "student":
#             dob = data["dob"]
#             usn = data["usn"]
#             cgpa = data["cgpa"]
#
#             if not dob or not usn or not cgpa:
#                 return jsonify({'success': False, 'message': 'Missing required student details: dob, usn, or cgpa.'})
#
#             user_details[user_id] = {
#                 'name': name,
#                 'role': role,
#                 'dob': dob,
#                 'usn': usn,
#                 'cgpa': cgpa
#             }
#         elif role == "staff":
#             department = data.get('department')
#             designation = data.get('designation')
#
#             if not department or not designation:
#                 return jsonify({'success': False, 'message': 'Incomplete staff details provided.'})
#
#             user_details[user_id] = {
#                 'name': name,
#                 'department': department,
#                 'designation': designation,
#                 'role': role
#             }
#         else:
#             return jsonify({'success': False, 'message': 'Invalid role provided.'})
#
#         save_user_details(user_details)
#
#         return jsonify({'success': True, 'message': 'User registered successfully.'})
#
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)})
#
#
# @app.route('/identify-user', methods=['POST'])
# def identify_user():
#     try:
#         data = request.get_json()
#         image_base64 = data['image']
#
#         live_image = base64_to_image(image_base64)
#         rgb_live_image = cv2.cvtColor(live_image, cv2.COLOR_BGR2RGB)
#
#         live_encodings = get_face_encodings(rgb_live_image)
#         if len(live_encodings) == 0:
#             return jsonify({'success': False, 'message': 'No face detected.'})
#
#         live_encoding = live_encodings[0]
#
#         user_details = load_user_details()
#         closest_match = None
#         closest_distance = float('inf')
#         threshold = 0.4
#
#         for user_id in user_details:
#             stored_encoding = load_face_encoding(user_id)
#             if stored_encoding is not None:
#                 distance = np.linalg.norm(np.array(stored_encoding) - np.array(live_encoding))
#                 if distance < closest_distance and distance < threshold:
#                     closest_distance = distance
#                     closest_match = user_id
#
#         if closest_match:
#             user_info = user_details[closest_match]
#             return jsonify({
#                 'success': True,
#                 'message': 'User identified successfully!',
#                 'user': user_info
#             })
#         else:
#             return jsonify({'success': False, 'message': 'No matching user found.'})
#
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)})
#
# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# import dlib
# import cv2
# import numpy as np
# import base64
#
# # Flask setup
# app = Flask(__name__)
# CORS(app)
#
# # SQLite DB config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
# # Dlib setup
# detector = dlib.get_frontal_face_detector()
# shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
#
# # SQLAlchemy model
# class User(db.Model):
#     id = db.Column(db.String, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     role = db.Column(db.String, nullable=False)
#     dob = db.Column(db.String)
#     usn = db.Column(db.String)
#     cgpa = db.Column(db.String)
#     department = db.Column(db.String)
#     designation = db.Column(db.String)
#     face_encoding = db.Column(db.PickleType, nullable=False)  # Stores the numpy array
#
# # Utilities
# def base64_to_image(base64_string):
#     img_data = base64.b64decode(base64_string.split(',')[1])
#     nparr = np.frombuffer(img_data, np.uint8)
#     return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
# def get_face_encodings(image):
#     dets = detector(image, 1)
#     encodings = []
#     for det in dets:
#         shape = shape_predictor(image, det)
#         face_encoding = np.array(face_rec_model.compute_face_descriptor(image, shape))
#         encodings.append(face_encoding)
#     return encodings
#
# # Routes
# @app.route('/register-user', methods=['POST'])
# def register_user():
#     try:
#         data = request.get_json()
#         user_id = data['user_id']
#         name = data['name']
#         role = data['role']
#         image_base64 = data['image']
#
#         if not name or not role or not image_base64:
#             return jsonify({"success": False, "message": "Missing required fields."})
#
#         image = base64_to_image(image_base64)
#         rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         face_encodings = get_face_encodings(rgb_image)
#
#         if len(face_encodings) == 0:
#             return jsonify({'success': False, 'message': 'No face detected.'})
#
#         encoding = face_encodings[0]
#
#         if User.query.get(user_id):
#             return jsonify({'success': False, 'message': 'User already exists.'})
#
#         user = User(id=user_id, name=name, role=role, face_encoding=encoding)
#
#         if role == "student":
#             user.dob = data.get("dob")
#             user.usn = data.get("usn")
#             user.cgpa = data.get("cgpa")
#
#             if not user.dob or not user.usn or not user.cgpa:
#                 return jsonify({'success': False, 'message': 'Missing student details.'})
#
#         elif role == "staff":
#             user.department = data.get("department")
#             user.designation = data.get("designation")
#
#             if not user.department or not user.designation:
#                 return jsonify({'success': False, 'message': 'Missing staff details.'})
#
#         else:
#             return jsonify({'success': False, 'message': 'Invalid role provided.'})
#
#         db.session.add(user)
#         db.session.commit()
#
#         return jsonify({'success': True, 'message': 'User registered successfully.'})
#
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)})
#
# @app.route('/identify-user', methods=['POST'])
# def identify_user():
#     try:
#         data = request.get_json()
#         image_base64 = data['image']
#
#         live_image = base64_to_image(image_base64)
#         rgb_image = cv2.cvtColor(live_image, cv2.COLOR_BGR2RGB)
#         live_encodings = get_face_encodings(rgb_image)
#
#         if len(live_encodings) == 0:
#             return jsonify({'success': False, 'message': 'No face detected.'})
#
#         live_encoding = live_encodings[0]
#         users = User.query.all()
#
#         closest_match = None
#         closest_distance = float('inf')
#         threshold = 0.4
#
#         for user in users:
#             distance = np.linalg.norm(np.array(user.face_encoding) - live_encoding)
#             if distance < closest_distance and distance < threshold:
#                 closest_distance = distance
#                 closest_match = user
#
#         if closest_match:
#             user_info = {
#                 "name": closest_match.name,
#                 "role": closest_match.role,
#             }
#             if closest_match.role == "student":
#                 user_info.update({
#                     "dob": closest_match.dob,
#                     "usn": closest_match.usn,
#                     "cgpa": closest_match.cgpa
#                 })
#             elif closest_match.role == "staff":
#                 user_info.update({
#                     "department": closest_match.department,
#                     "designation": closest_match.designation
#                 })
#
#             return jsonify({'success': True, 'message': 'User identified successfully.', 'user': user_info})
#         else:
#             return jsonify({'success': False, 'message': 'No matching user found.'})
#
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)})
#
# # Entry point
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import dlib
import cv2
import numpy as np
import base64

# Flask setup
app = Flask(__name__)
CORS(app)

# SQLite DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Dlib setup
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# SQLAlchemy model
class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    dob = db.Column(db.String)
    usn = db.Column(db.String)
    cgpa = db.Column(db.String)
    department = db.Column(db.String)
    designation = db.Column(db.String)
    face_encoding = db.Column(db.PickleType, nullable=False)  # Stores numpy array

# Utilities
def base64_to_image(base64_string):
    img_data = base64.b64decode(base64_string.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def get_face_encodings(image):
    dets = detector(image, 1)
    encodings = []
    for det in dets:
        shape = shape_predictor(image, det)
        face_encoding = np.array(face_rec_model.compute_face_descriptor(image, shape))
        encodings.append(face_encoding)
    return encodings

# Register route
@app.route('/register-user', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        user_id = data['user_id']
        name = data['name']
        role = data['role']
        image_base64 = data['image']

        if not name or not role or not image_base64:
            return jsonify({"success": False, "message": "Missing required fields."})

        image = base64_to_image(image_base64)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_encodings = get_face_encodings(rgb_image)

        if len(face_encodings) == 0:
            return jsonify({'success': False, 'message': 'No face detected.'})

        encoding = face_encodings[0]

        if User.query.get(user_id):
            return jsonify({'success': False, 'message': 'User already exists.'})

        user = User(id=user_id, name=name, role=role, face_encoding=encoding)

        if role == "student":
            user.dob = data.get("dob")
            user.usn = data.get("usn")
            user.cgpa = data.get("cgpa")

            if not user.dob or not user.usn or not user.cgpa:
                return jsonify({'success': False, 'message': 'Missing student details.'})

        elif role == "staff":
            user.department = data.get("department")
            user.designation = data.get("designation")

            if not user.department or not user.designation:
                return jsonify({'success': False, 'message': 'Missing staff details.'})

        else:
            return jsonify({'success': False, 'message': 'Invalid role provided.'})

        db.session.add(user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'User registered successfully.'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Identify user route
@app.route('/identify-user', methods=['POST'])
def identify_user():
    try:
        data = request.get_json()
        image_base64 = data['image']

        live_image = base64_to_image(image_base64)
        rgb_image = cv2.cvtColor(live_image, cv2.COLOR_BGR2RGB)
        live_encodings = get_face_encodings(rgb_image)

        if len(live_encodings) == 0:
            return jsonify({'success': False, 'message': 'No face detected.'})

        live_encoding = live_encodings[0]
        users = User.query.all()

        closest_match = None
        closest_distance = float('inf')
        threshold = 0.4

        for user in users:
            distance = np.linalg.norm(np.array(user.face_encoding) - live_encoding)
            if distance < closest_distance and distance < threshold:
                closest_distance = distance
                closest_match = user

        if closest_match:
            user_info = {
                "name": closest_match.name,
                "role": closest_match.role,
            }
            if closest_match.role == "student":
                user_info.update({
                    "dob": closest_match.dob,
                    "usn": closest_match.usn,
                    "cgpa": closest_match.cgpa
                })
            elif closest_match.role == "staff":
                user_info.update({
                    "department": closest_match.department,
                    "designation": closest_match.designation
                })

            return jsonify({'success': True, 'message': 'User identified successfully.', 'user': user_info})
        else:
            return jsonify({'success': False, 'message': 'No matching user found.'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Search user route
@app.route('/search-user', methods=['GET'])
def search_user():
    try:
        query = User.query2

        name = request.args.get('name')
        usn = request.args.get('usn')
        department = request.args.get('department')
        designation = request.args.get('designation')
        role = request.args.get('role')

        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))
        if usn:
            query = query.filter(User.usn.ilike(f"%{usn}%"))
        if department:
            query = query.filter(User.department.ilike(f"%{department}%"))
        if designation:
            query = query.filter(User.designation.ilike(f"%{designation}%"))
        if role:
            query = query.filter_by(role=role)

        results = query.all()

        users = []
        for user in results:
            user_info = {
                "id": user.id,
                "name": user.name,
                "role": user.role,
                "dob": user.dob,
                "usn": user.usn,
                "cgpa": user.cgpa,
                "department": user.department,
                "designation": user.designation
            }
            users.append(user_info)

        return jsonify({"success": True, "users": users})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)