import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base, User, LeaveRequest, LeaveType, FiscalYear, Designation, Allocation

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def import_data_from_file(file_path):
    data = pd.read_json(file_path)
    for _, user_data in data['users'].iterrows():
        user = User(**user_data)
        session.merge(user)
    for _, leave_data in data['leave_requests'].iterrows():
        leave_data['source'] = 'file'
        leave = LeaveRequest(**leave_data)
        session.merge(leave)
    session.commit()

if __name__ == '__main__':
    file_path = 'path_to_your_file.json'
    import_data_from_file(file_path)
