from flask import Flask, jsonify, request, render_template, send_from_directory, flash
import qrcode
import os
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Directory to save the QR code images
QR_CODE_DIR = 'static/qr_codes'
os.makedirs(QR_CODE_DIR, exist_ok=True)

players={}
# Hardcoded questions and their correct answers
questions = [
    {
        'question': "What is the official currency of Japan?",
        'options': ['A. Won', 'B. Yuan', 'C. Yen', 'D. Dollar'],
        'answer': 'C'
    },
    {
        'question': "What is the name of the process by which plants convert sunlight into energy?",
        'options': ['A. Respiration', 'B. Photosynthesis', 'C. Oxidation', 'D. Evolution'],
        'answer': 'B'
    },
    {
        'question': "Which river is the longest in the world?",
        'options': ['A. Amazon', 'B. Mississippi', 'C. Nile', 'D. Yangtze'],
        'answer': 'C'
    },
        {
        'question': "What is the next prime number after 5?",
        'options': ['A. 7', 'B. 6', 'C. 9', 'D. 11'],
        'answer': 'A'
    },
        {
        'question': "Which of these animals cannot jump?",
        'options': ['A. Cat', 'B. Horse', 'C. Kangaroo', 'D. Snake'],
        'answer': 'D'
    }
]

@app.route('/')
def quiz():
    return render_template('quiz.html')

@app.route('/mobileName')
def mobileName():
    return render_template('name.html')

@app.route('/submit_name', methods=['POST'])
def submit_name():
    """Handle name submission."""
    name1 = request.form.get('name')
    
    players[name1]=0
    return render_template('mobile.html',name=name1)

@app.route('/players')
def get_players():
    return jsonify(players)    

@app.route('/results')
def results():
    return render_template('results.html')   

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')   


@app.route('/mobile')
def quizMobile():
    return render_template('mobile.html')

@app.route('/questions', methods=['GET'])
def get_questions():
    """Endpoint to fetch the quiz questions."""
    return jsonify(questions)


@app.route('/losePage')
def lose_Page():
    return render_template('lose.html')

@app.route('/generate_qr_code')
def generate_qr_code():
    """Generate a QR code for the quiz link and save it as an image."""
    players={}
    local_ip = '192.168.1.5'  # Replace this with your actual local IP address
    link = f"http://{local_ip}:5000/mobileName"
    # link = f"https://kbc-style-game.onrender.com/mobileName"
    
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Save the image to a file
    qr_code_path = os.path.join(QR_CODE_DIR, 'quiz_qr_code.png')
    img.save(qr_code_path)

    return jsonify({'message': 'QR Code generated and saved.', 'path': qr_code_path})

@app.route('/qr_code/<filename>')
def qr_code(filename):
    """Serve the QR code image."""
    return send_from_directory(QR_CODE_DIR, filename)


@app.route('/update_answer', methods=['POST'])
def update_answer():
    """Update player's answer."""
    
    data = request.get_json()  # Get JSON data sent from frontend
    name = data['name']
    index = data['i']
    players[name]=players[name]+1
    socketio.emit('variable_change', {'value': name,'index':data['i']+1})  # Notify clients
    socketio.emit('timer', {'value': 500})  # Notify clients

    # Update the player's answer in the dictionary
    if name in players:
        return jsonify({"status": "success", "message": f"Answer updated for {name}"})
    else:
        return jsonify({"status": "error", "message": "Name not found"}), 404

   
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000, debug=True)


# if __name__ == '__main__':
#     socketio.run(app,debug=True)