from ...conftest import ModelTest

from flask import Flask
from sqlalchemy.orm import Session

from easy_framework import Database


class TestBaseModel():
    def test_assert_session_is_active_before_closing_it(self, database: Database):
        dbSession: Session = database.getNewSession()
        assert dbSession.is_active
        database.closeSession()

    def test_receive_scoped_session_and_check_if_is_active(self, database:Database):
        with database.getScopedSession() as dbSession:
            assert dbSession.is_active
    
    def test_set_scoped_session_and_check_if_is_active(self, database:Database):
        with database.setScopedSession():
            assert database.dbSession.is_active

    def test_get_session_and_check_if_is_active(self, database:Database):
        dbSession = database.getNewSession()
        assert dbSession.is_active
        database.closeSession()

    def test_set_session_and_check_if_is_active(self, database:Database):
        database.openSession()
        assert database.dbSession.is_active
        database.closeSession()

    def test_getting_scoped_session_save_new_entity_into_database_and_check_if_is_there(self, database: Database, flaskApp:Flask):
        with flaskApp.app_context():
            test_entity = ModelTest(id=1, info="hello there! I'm a testing entity")
            with database.getScopedSession() as dbSession:
                dbSession.add(test_entity)
                dbSession.commit()

            with database.getScopedSession() as dbSession:
                assert dbSession.query(ModelTest).filter(ModelTest.id==1).count() == 1

    def test_setting_scoped_session_save_new_entity_into_database_and_check_if_is_there(self, database: Database, flaskApp:Flask):
        with flaskApp.app_context():
            test_entity = ModelTest(id=1, info="hello there! I'm a testing entity")
            with database.setScopedSession():
                database.dbSession.add(test_entity)
                database.dbSession.commit()

            with database.setScopedSession():
                assert database.dbSession.query(ModelTest).filter(ModelTest.id==1).count() == 1

    def test_getting_session_save_new_entity_into_database_and_check_if_is_there(self, database: Database, flaskApp:Flask):
        with flaskApp.app_context():
            test_entity = ModelTest(id=1, info="hello there! I'm a testing entity")
            dbSession = database.getNewSession()
            dbSession.add(test_entity)
            dbSession.commit()
            database.closeSession()

            dbSession = database.getNewSession()
            assert dbSession.query(ModelTest).filter(ModelTest.id==1).count() == 1
            database.closeSession()

    def test_setting_session_save_new_entity_into_database_and_check_if_is_there(self, database: Database, flaskApp:Flask):
        with flaskApp.app_context():
            test_entity = ModelTest(id=1, info="hello there! I'm a testing entity")
            database.openSession()
            database.dbSession.add(test_entity)
            database.dbSession.commit()
            database.closeSession()

            database.openSession()
            assert database.dbSession.query(ModelTest).filter(ModelTest.id==1).count() == 1
            database.closeSession()
    

        