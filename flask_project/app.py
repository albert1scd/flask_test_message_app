from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Required for flashing messages
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

messages = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            messages.append({'text': message, 'timestamp': timestamp})
            flash('Message posted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', messages=messages)

@app.route('/delete/<int:message_id>')
def delete_message(message_id):
    if 0 <= message_id < len(messages):
        del messages[message_id]
        flash('Message deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/api/messages')
def get_messages():
    return jsonify(messages)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(413)
def file_too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

if __name__ == '__main__':
    app.run(debug=True)