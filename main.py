from app import create_app, db
from flask_migrate import Migrate

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        migrate = Migrate(app, db)
        db.create_all()
        app.run(debug=True)
