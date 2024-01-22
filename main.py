from app import routes

if __name__ == '__main__':
    app = routes.create_server()
    app.run(debug=True, host="0.0.0.0", port=5000)