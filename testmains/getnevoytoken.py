import json
import httpx
import os
import dotenv
dotenv.load_dotenv("localenv.txt")
user=os.getenv("ENPHASE_USERNAME")
password=os.getenv("ENPHASE_PASSWORD")
envoy_serial=os.getenv("ENPHASE_GWSERIAL")

data = {'user[email]': user, 'user[password]': password}
response = httpx.post('https://enlighten.enphaseenergy.com/login/login.json?', data=data) 
response_data = json.loads(response.text)
data = {'session_id': response_data['session_id'], 'serial_num': envoy_serial, 'username': user}
response = httpx.post('https://entrez.enphaseenergy.com/tokens', json=data)
token_str: str = response.text
print (token_str)