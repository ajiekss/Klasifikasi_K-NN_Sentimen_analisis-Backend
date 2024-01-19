from app import app

TEMPLATES_AUTO_RELOAD = True

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
    