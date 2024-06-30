from flask import Flask, request, render_template
import requests
import json
import os

app = Flask(__name__)

# Pastikan data.txt ada
if not os.path.isfile('data.txt'):
    with open('data.txt', 'w') as f:
        pass

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    user_ip = request.remote_addr
    response = requests.get(f'http://ip-api.com/json/{user_ip}')
    location_data = response.json()

    # Menyimpan data ke data.txt
    with open('data.txt', 'a') as f:
        f.write(json.dumps({"ip": user_ip, "location": location_data}) + '\n')

    return render_template('data.html', data={"ip": user_ip, "location": location_data})

@app.route('/data')
def show_data():
    with open('data.txt', 'r') as f:
        data = f.readlines()
    data_list = [json.loads(line) for line in data]
    return render_template('data.html', data_list=data_list)

if __name__ == '__main__':
    app.run(debug=True)
