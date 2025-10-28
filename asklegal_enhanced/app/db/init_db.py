from app.db.base import Base, engine
from app.models import user, chat

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully!")