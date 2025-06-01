from .engine import Base, engine, Session
from .models import *

def init_db():
    Base.metadata.create_all(bind = engine)


if __name__ == "__main__":
    init_db()