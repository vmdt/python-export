from src import app

app.debug = True
port = app.config.get('PORT', 5000)

if __name__ == '__main__':
    print(f"Running on port {port}")
    app.run(port=port)