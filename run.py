# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app = create_app()
#     app.run(host="0.0.0.0", port=5000)


# from flask import Flask
# from app.routes import bp as routes_bp

# app = Flask(__name__)

# # Register the routes blueprint
# app.register_blueprint(routes_bp)

# if __name__ == "__main__":
#     app.run(debug=True)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
