#windows
python -m venv venv
venv\Scripts\activate

#linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt


alembic revision --autogenerate -m "create users table"
alembic upgrade head


py -m uvicorn app.main:app --reload --port 8100