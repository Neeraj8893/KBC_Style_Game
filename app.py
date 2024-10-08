from flask import Flask, jsonify, request, render_template, send_from_directory, flash
import qrcode
import os

app = Flask(__name__)

# Directory to save the QR code images
QR_CODE_DIR = 'static/qr_codes'
os.makedirs(QR_CODE_DIR, exist_ok=True)
# Hardcoded questions and their correct answers
players={}
questions = [
    {
        'question': "What is the capital of France?",
        'options': ['A. Berlin', 'B. Madrid', 'C. Paris', 'D. Rome'],
        'answer': 'C'
    },
    {
        'question': "Which planet is known as the Red Planet?",
        'options': ['A. Earth', 'B. Mars', 'C. Jupiter', 'D. Venus'],
        'answer': 'B'
    },
    {
        'question': "Who wrote 'Hamlet'?",
        'options': ['A. Charles Dickens', 'B. William Shakespeare', 'C. Mark Twain', 'D. Leo Tolstoy'],
        'answer': 'B'
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
    print(players[name1])
    print(players.items())
   # if name:
        # Store the name (you can save it to a database or file if needed)
        # Here we simply flash a message and redirect to the mobile route
        #flash(f"Welcome, {name}!", "success")
        #return redirect(url_for('mobile'))
    #else:
        #flash("Please enter a name.", "error")
        #return redirect(url_for('mobile'))
    return render_template('mobile.html',name=name1)

    

@app.route('/mobile')
def quizMobile():
    return render_template('mobile.html')

@app.route('/questions', methods=['GET'])
def get_questions():
    """Endpoint to fetch the quiz questions."""
    return jsonify(questions)


@app.route('/losePage')
def lose_Page():
    print("lose")
    return render_template('lose.html')


@app.route('/submit', methods=['POST'])
def submit_quiz():
    """Endpoint to process quiz results."""
    data = request.json
    selected_answers = data.get('answers', [])
    correct_count = 0

    # Calculate how many answers are correct
    for i, answer in enumerate(selected_answers):
        if answer == questions[i]['answer']:
            correct_count += 1

    return jsonify({'correct_count': correct_count, 'total': len(questions)})

@app.route('/generate_qr_code')
def generate_qr_code():
    """Generate a QR code for the quiz link and save it as an image."""
     
    # link = "http://localhost:5000"  # Modify to your production URL if needed
    local_ip = '192.168.1.5'  # Replace this with your actual local IP address
    link = f"http://{local_ip}:5000/mobileName"
    
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

#if __name__ == '__main__':
 #   app.run(debug=True)

@app.route('/update_answer', methods=['POST'])
def update_answer():
    print("Inside Update Answer")
    """Update player's answer."""
    
    data = request.get_json()  # Get JSON data sent from frontend
    name = data['name']
   
    print(name)
    players[name]=players[name]+1
    print("Your score")
    print(players)
    
    # Update the player's answer in the dictionary
    if name in players:
        #players[name]['answer'] = answer
      
        return jsonify({"status": "success", "message": f"Answer updated for {name}"})
    else:
        return jsonify({"status": "error", "message": "Name not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
