from flask import Flask, request, render_template, redirect
import requests
import json
import os

app = Flask(__name__)

# Cek dan buat data.txt jika tidak ada
if not os.path.isfile('data.txt'):
    open('data.txt', 'w').close()

# Endpoint untuk halaman utama
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint untuk menangkap IP dan lokasi
@app.route('/track', methods=['POST'])
def track():
    user_ip = request.remote_addr
    response = requests.get(f'http://ip-api.com/json/{user_ip}')
    location_data = response.json()

    # Menyimpan data ke data.txt
    with open('data.txt', 'a') as f:
        f.write(json.dumps({"ip": user_ip, "location": location_data}) + '\n')

    # Menampilkan data
    return render_template('data.html', data={"ip": user_ip, "location": location_data})

# Endpoint untuk menampilkan data yang tersimpan
@app.route('/data')
def show_data():
    with open('data.txt', 'r') as f:
        data = f.readlines()
    data_list = [json.loads(line) for line in data]
    return render_template('data.html', data_list=data_list)

if __name__ == '__main__':
    app.run(debug=True)
