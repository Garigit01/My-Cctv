import requests

# Yahan apna token aur chat id bhariye
TOKEN = "8085719035:AAEJEcOV8ryEJgPU5EY34OeaoW2BbuvL9II"
CHAT_ID = "8522771910"

message = "Hello! Main aapka CCTV bot hoon. Main ready hoon."
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"

response = requests.get(url)

if response.status_code == 200:
    print("Mubarak ho! Telegram par message aa gaya.")
else:
    print("Kuch gadbad hai, token check karein.")
    print(response.json()) # Ye batayega ki Telegram ne kya error bheja hai