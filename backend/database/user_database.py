from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .entities.user_entity import Base, UserEntity

# 创建数据库引擎
engine = create_engine("sqlite:///cotrip.db")

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化数据库（创建表）
def init_db():
    Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 数据库操作类
class UserDatabase:
    def __init__(self, db):
        self.db = db
    
    def create_user(self, user_data):
        """创建新用户"""
        db_user = UserEntity(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_by_email(self, email):
        """通过邮箱获取用户"""
        return self.db.query(UserEntity).filter(UserEntity.email == email).first()
    
    def get_user_by_username(self, username):
        """通过用户名获取用户"""
        return self.db.query(UserEntity).filter(UserEntity.username == username).first()
    
    def get_user_by_id(self, user_id):
        """通过ID获取用户"""
        return self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
    
    def update_user(self, user_id, user_data):
        """更新用户信息"""
        db_user = self.get_user_by_id(user_id)
        if db_user:
            for key, value in user_data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
