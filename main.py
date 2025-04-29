
from flask import Flask, request, redirect, session, jsonify
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure Google OAuth
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = 'AKfycbzqdHNC8UMIdeanZuvjIra9Y8IjPC17JemmbSkcB1LwKR9w_Y1wIQHnIPZLsZn6QSLjIQ'  # You'll need to replace this

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'credentials' not in session:
        return redirect('/authorize')
    
    data = request.json
    credentials = Credentials(**session['credentials'])
    service = build('sheets', 'v4', credentials=credentials)
    
    values = [[
        data['studentName'],
        data['contactNumber'],
        data['parentContact'],
        data['location']
    ]]
    
    body = {'values': values}
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    return jsonify({'status': 'success'})

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect('/')

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host='0.0.0.0', port=5000)
