import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = '92063bc773b277535cf8e466a8e6d15812b1f5001b216c10c75d915e3bd79e1a'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for development

# Initialize SocketIO client for tkinter GUI
from socketio.client import Client

sio = Client()

# Connect to the Flask-SocketIO server
@sio.event
def connect():
    print('Connected to server')
    sio.emit('join', {'username': 'User'})  # Emit a join event upon connection

# Handle incoming messages
@sio.on('message')
def message(data):
    msg_listbox.insert(tk.END, data)

# Function to send message
def send_message():
    global entry_message
    message_text = entry_message.get()
    if sio.connected:
        sio.emit('message', message_text)
        entry_message.delete(0, tk.END)
    else:
        print('SocketIO client is not connected.')

# Flask routes and socket handling
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)
    emit('message', message, broadcast=True)

# GUI Setup with tkinter
def setup_gui():
    global entry_message, msg_listbox_left, msg_listbox_right

    root = tk.Tk()
    root.title('Chat Application')

    # Left Chat Box
    left_frame = tk.Frame(root, width=300, height=400)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    msg_listbox_left = Text(left_frame, width=50, height=20)
    msg_listbox_left.pack(pady=10)
    scrollbar_left = Scrollbar(left_frame, command=msg_listbox_left.yview)
    scrollbar_left.pack(side=tk.RIGHT, fill=tk.Y)
    msg_listbox_left.config(yscrollcommand=scrollbar_left.set)

    # Right Chat Box
    right_frame = tk.Frame(root, width=300, height=400)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    msg_listbox_right = Text(right_frame, width=50, height=20)
    msg_listbox_right.pack(pady=10)
    scrollbar_right = Scrollbar(right_frame, command=msg_listbox_right.yview)
    scrollbar_right.pack(side=tk.RIGHT, fill=tk.Y)
    msg_listbox_right.config(yscrollcommand=scrollbar_right.set)

    entry_message = Entry(root, width=50)
    entry_message.pack(pady=10)

    send_button = Button(root, text='Send', command=send_message)
    send_button.pack(pady=10)

    root.mainloop()

# Start Flask-SocketIO server and run GUI in separate threads
if __name__ == '__main__':
    # Flask-SocketIO server in a separate thread
    flask_thread = Thread(target=socketio.run, args=(app,), kwargs={'host': 'localhost', 'port': 5000})
    flask_thread.start()

    # tkinter GUI in another separate thread
    gui_thread = Thread(target=setup_gui)
    gui_thread.start()

    flask_thread.join()
    gui_thread.join()
