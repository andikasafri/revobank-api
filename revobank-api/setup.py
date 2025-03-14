from setuptools import setup, find_packages

setup(
    name="revobank-api",
    version="0.1.0",
    packages=find_packages(include=["revobank-api", "app", "migrations"]),
    install_requires=[
        "flask==3.0.2",
        "flask-jwt-extended==4.6.0",
        "flask-sqlalchemy==3.1.1",
        "flask-migrate==4.0.5",
        "sqlalchemy==2.0.25",
        "mysqlclient==2.2.7",
        "python-dotenv==1.0.1",
        "werkzeug==3.0.3",
        "pytest==7.4.0",
        "pytest-cov==4.1.0",
        "httpie==3.2.2",
        "gunicorn==20.1.0"
    ],
)