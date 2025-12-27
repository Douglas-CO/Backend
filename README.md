# Backend
Backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
sudo apt install postgresql-client

python manage.py makemigrations usuarios inventario venta cliente
python manage.py migrate


python manage.py runserver


USUARIO
token

INVENTARIO
seed

VENTA
Flujo de negocio

CLIENTE
api getaway

CARTERA
