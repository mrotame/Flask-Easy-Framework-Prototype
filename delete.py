import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

from src.database.database import Database
from src.models.user import User
from sqlalchemy.orm import Session
from app import App
from datetime import datetime

def oneSession():
    time_start = datetime.now()
    db = Database()
    dbSession: Session = db.session_scoped()

    user = User(login='teste',password='teste')
    dbSession.add(user)
    dbSession.commit()

    user.login = 'teste@teste.com'
    dbSession.commit()
    del user

    user = dbSession.query(User).filter(User.login=='teste@teste.com').first()
    user.password = '123456'
    dbSession.commit()

    dbSession.delete(user)
    dbSession.commit()

    db.session_scoped.remove()
    time_end = datetime.now()
    print('runtime:', time_end - time_start)

def multiSession():
    def getdbSession()-> Session:
        class DatabaseSession(object):
            db: Database = Database()
            def __enter__(self)-> Session:
                return self.db.session_scoped()

            def __exit__(self, exc_type, exc_val, exc_tb)-> None:
                self.db.session_scoped.remove()
        return DatabaseSession()

    time_start = datetime.now()

    with getdbSession() as dbSession:
        user = User(login='teste',password='teste')
        dbSession.add(user)
        dbSession.commit()

    with getdbSession() as dbSession:
        user = dbSession.query(User).filter(User.login=='teste').first()
        user.login = 'teste@teste.com'
        dbSession.commit()
    
    with getdbSession() as dbSession:

        user = dbSession.query(User).filter(User.login=='teste@teste.com').first()
        user.password = '123456'
        dbSession.commit()

    with getdbSession() as dbSession:
        user = dbSession.query(User).filter(User.login=='teste@teste.com').first()
        dbSession.delete(user)
        dbSession.commit()
    
    time_end = datetime.now()
    print('runtime:', time_end - time_start)

if __name__ == "__main__":
    with App().app.test_request_context():
        oneSession()
        multiSession()
