from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.models import Identity

class IdentityService:
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def get_all_identities(self, skip: int = 0, limit: int = 100):
        return self.db.query(Identity).offset(skip).limit(limit).all()
    
    def get_identity_by_id(self, identity_id: int):
        return self.db.query(Identity).filter(Identity.id == identity_id).first()
    
    def get_identity_by_student_id(self, student_id: str):
        return self.db.query(Identity).filter(Identity.student_id == student_id).first()
    
    def get_identity_by_email(self, email: str):
        return self.db.query(Identity).filter(Identity.email == email).first()
    
    def create_identity(self, name: str, email: str, student_id: str, phone: str = None, is_active: bool = True):
        try:
            identity = Identity(
                name=name,
                email=email,
                phone=phone,
                student_id=student_id,
                created_at=datetime.utcnow(),
                is_active=is_active
            )
            self.db.add(identity)
            self.db.commit()
            self.db.refresh(identity)
            return identity
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Identity with this email or student ID already exists")
    
    def create_identity_from_object(self, student_data):
        try:
            if hasattr(student_data, 'to_dict'):
                data_dict = student_data.to_dict()
                return self.create_identity(**data_dict)
            else:
                return self.create_identity(
                    name=getattr(student_data, 'name', None),
                    email=getattr(student_data, 'email', None),
                    student_id=getattr(student_data, 'student_id', None),
                    phone=getattr(student_data, 'phone', None),
                    is_active=getattr(student_data, 'is_active', True)
                )
        except AttributeError as e:
            raise ValueError(f"Invalid student data object: {e}")
    
    def update_identity(self, identity_id: int, **kwargs):
        identity = self.get_identity_by_id(identity_id)
        if not identity:
            raise ValueError(f"Identity with ID {identity_id} does not exist")
            
        for key, value in kwargs.items():
            if hasattr(identity, key):
                setattr(identity, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(identity)
            return identity
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Update failed due to constraint violation")
    
    def update_identity_from_object(self, identity_id: int, student_data):
        if hasattr(student_data, 'to_dict'):
            data_dict = student_data.to_dict()
            return self.update_identity(identity_id, **data_dict)
        else:
            update_dict = {}
            for attr in ['name', 'email', 'student_id', 'phone', 'is_active']:
                if hasattr(student_data, attr):
                    value = getattr(student_data, attr)
                    if value is not None:
                        update_dict[attr] = value
            
            return self.update_identity(identity_id, **update_dict)
    
    def deactivate_identity(self, identity_id: int):
        return self.update_identity(identity_id, is_active=False)
    
    def reactivate_identity(self, identity_id: int):
        return self.update_identity(identity_id, is_active=True)
    
    def delete_identity(self, identity_id: int):
        identity = self.get_identity_by_id(identity_id)
        if not identity:
            raise ValueError(f"Identity with ID {identity_id} does not exist")
        
        self.db.delete(identity)
        self.db.commit()
        return True