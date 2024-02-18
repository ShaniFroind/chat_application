from datetime import datetime
from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)


def loading_data_into_file(room, name, message):
    if os.path.exists('data.json'):
        with open('data.json', 'r') as data:
            messages_data = json.load(data)
    else:
        messages_data = []

    room_found = False

    for r in messages_data:
        if r['room_name'] == room:
            r['messages'].append({
                'name': name,
                'message': message,
                'date_of_message': datetime.now().isoformat()
            })
            room_found = True
            break

    if not room_found:
        new_room = {
            'room_name': room,
            'messages': [{
                'name': name,
                'message': message,
                'date_of_message': datetime.now().isoformat()
            }]
        }
        messages_data.append(new_room)

    with open('data.json', 'w') as file:
        json.dump(messages_data, file, indent=2)


def loading_data_from_file(room_name):
    if os.path.exists('data.json'):
        with open('data.json', 'r') as file:
            room_information = json.load(file)
            for room in room_information:
                if room['room_name'] == room_name:
                    formatted_chat = [
                        f"[{datetime.strptime(message['date_of_message'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"{message['name']}: {message['message']}"
                        for message in room['messages']
                    ]
                    return '\n'.join(formatted_chat)
    return "There is not such a room"\


def read_file(path):
    with open(path,'r') as file:
        return file.read()



@app.route('/', methods=['GET'])
def welcome():
   return read_file('Welcome.html')


@app.route('/<room>', methods=['GET'])
def create_chat(room):
   return  read_file('index.html')

@app.route('/api/chat/<room>', methods=['POST'])
def save_data(room):
    name = request.form.get('username')
    message = request.form.get('msg')
    loading_data_into_file(room, name, message)
    return jsonify({'success': True, 'message': f'The message "{message}" added into room: {room}'})


@app.route('/api/chat/<room_name>')
def show_chat(room_name):
    chat_messages = loading_data_from_file(room_name)
    return chat_messages


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(dhost='0.0.0.0', port=5000)
