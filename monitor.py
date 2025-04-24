import google.generativeai as genai
import datetime
import requests
import subprocess

# Konfigurasi API Gemini
genai.configure(api_key="AIzaSyBfcUSvoz6hX-9Ve4R-o_GjQWGmu17DfSE")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_ssh_attempts():
    result = subprocess.check_output("grep 'Failed password' /var/log/auth.log | tail -n 10", shell=True)
    return result.decode()

def get_gemini_analysis(log_text):
    try:
        response = model.generate_content(f"Ada percobaan login brute force:\n{log_text}\nApa yang sebaiknya saya lakukan?. responnya jangan terlalu panjang")
        return response.text
    except Exception as e:
        return "⚠️ Gagal mendapatkan analisis dari Gemini: " + str(e)

def send_whatsapp(message):
    token = "6JG1L6KBgeuvtVSp1b5W"
    payload = {
        "target": "6281211945840",
        "message": message,
    }
    headers = {"Authorization": token}
    r = requests.post("https://api.fonnte.com/send", data=payload, headers=headers)
    return r.status_code

# Eksekusi semua
log = get_ssh_attempts()
ai_response = get_gemini_analysis(log)
full_message = f"[{datetime.datetime.now()}] ⚠️ Percobaan Login Detected!\n\n{log}\n\n🤖 Gemini says:\n{ai_response}"
send_whatsapp(full_message)
