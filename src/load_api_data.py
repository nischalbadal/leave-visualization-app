import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base, User, LeaveRequest, LeaveType, FiscalYear, Designation, Allocation

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def fetch_data_from_api(api_url):
    response = requests.get(api_url)
    return response.json()

def import_data(data):
    for user_data in data['users']:
        user = User(**user_data)
        session.merge(user)
    for leave_data in data['leave_requests']:
        leave_data['source'] = 'api'
        leave = LeaveRequest(**leave_data)
        session.merge(leave)
    session.commit()

if __name__ == '__main__':
    api_url = 'https://example.com/api/data'
    data = fetch_data_from_api(api_url)
    import_data(data)
