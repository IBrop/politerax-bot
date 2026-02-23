from flask import Flask
import threading
import time
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "I am alive"

def background_loop():
    while True:
        print("Alive -", time.strftime("%H:%M:%S"), flush=True)
        time.sleep(900)

if __name__ == "__main__":
    threading.Thread(target=background_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
