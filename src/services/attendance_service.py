from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.models import Attendance, Identity
from services.identity_service import IdentityService

class AttendanceService:
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.identity_service = IdentityService(db_session)
        
    def get_attendance_by_id(self, attendance_id: int):
        return self.db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    def get_attendance_by_date(self, attendance_date: date):
        return self.db.query(Attendance).filter(Attendance.date == attendance_date).all()
    
    def get_attendance_by_identity(self, identity_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(Attendance)\
            .filter(Attendance.identity_id == identity_id)\
            .order_by(Attendance.date.desc())\
            .offset(skip).limit(limit).all()

    def get_attendance_by_date_range(self, identity_id: int, start_date: date, end_date: date):
        return self.db.query(Attendance)\
            .filter(Attendance.identity_id == identity_id)\
            .filter(Attendance.date >= start_date)\
            .filter(Attendance.date <= end_date)\
            .order_by(Attendance.date)\
            .all()
            
    def create_attendance(self, identity_id: int, attendance_date: date, status: str = None):
        identity = self.identity_service.get_identity_by_id(identity_id)
        if not identity:
            raise ValueError(f"Identity with ID {identity_id} does not exist")
            
        existing = self.db.query(Attendance)\
            .filter(Attendance.identity_id == identity_id)\
            .filter(Attendance.date == attendance_date)\
            .first()
            
        if existing:
            raise ValueError(f"Attendance record already exists for identity {identity_id} on {attendance_date}")
            
        attendance = Attendance(
            identity_id=identity_id,
            date=attendance_date,
            status=status
        )
        
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance
        
    def record_check_in(self, identity_id: int, attendance_date: date = None, check_in_time: datetime = None):
        if attendance_date is None:
            attendance_date = date.today()
            
        if check_in_time is None:
            check_in_time = datetime.now()
            
        attendance = self.db.query(Attendance)\
            .filter(Attendance.identity_id == identity_id)\
            .filter(Attendance.date == attendance_date)\
            .first()
            
        if not attendance:
            attendance = Attendance(
                identity_id=identity_id,
                date=attendance_date,
                check_in=check_in_time,
                status="Present"
            )
            self.db.add(attendance)
        else:
            attendance.check_in = check_in_time
            attendance.status = "Present"
            
        self.db.commit()
        self.db.refresh(attendance)
        return attendance
        
    def record_check_out(self, identity_id: int, attendance_date: date = None, check_out_time: datetime = None):
        if attendance_date is None:
            attendance_date = date.today()
            
        if check_out_time is None:
            check_out_time = datetime.now()
            
        attendance = self.db.query(Attendance)\
            .filter(Attendance.identity_id == identity_id)\
            .filter(Attendance.date == attendance_date)\
            .first()
            
        if not attendance:
            raise ValueError(f"No check-in record found for identity {identity_id} on {attendance_date}")
            
        attendance.check_out = check_out_time
        self.db.commit()
        self.db.refresh(attendance)
        return attendance
        
    def update_attendance_status(self, attendance_id: int, status: str):
        attendance = self.get_attendance_by_id(attendance_id)
        if not attendance:
            raise ValueError(f"Attendance record with ID {attendance_id} does not exist")
            
        attendance.status = status
        self.db.commit()
        self.db.refresh(attendance)
        return attendance
        
    def delete_attendance(self, attendance_id: int):
        attendance = self.get_attendance_by_id(attendance_id)
        if not attendance:
            raise ValueError(f"Attendance record with ID {attendance_id} does not exist")
            
        self.db.delete(attendance)
        self.db.commit()
        return True