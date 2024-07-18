class Config:
    SECRET_KEY = 'your_strong_secret_key'
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    JWT_TOKEN_LOCATION = ['headers']
