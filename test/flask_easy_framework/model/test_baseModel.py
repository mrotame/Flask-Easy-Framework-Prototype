from ...conftest import ModelTest

from flask import Flask

from easy_framework import Database


class TestBasemodel:
    def test_save_model_into_database(self, database: Database, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTest()
            new_entity.save()

            with database.getScopedSession() as dbSession:
                assert dbSession.query(ModelTest).filter(ModelTest.id == new_entity.id).count() == 1

    def test_get_one_model_in_database(self, database: Database, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTest()
            with database.getScopedSession() as dbSession:
                dbSession.add(new_entity)
                dbSession.commit()
                dbSession.refresh(new_entity)

            entity = ModelTest.get.one(ModelTest.id == new_entity.id)
            assert entity is not None

    def test_get_many_model_in_database(self, database:Database, flaskApp: Flask):
        with flaskApp.app_context():
            with database.getScopedSession() as dbSession:
                dbSession.add_all([ModelTest(),ModelTest(),ModelTest()])
                dbSession.commit()

            entities = ModelTest.get.many()
            assert len(entities) == 3

    def test_save_model_into_database_and_check_its_existence(self, database:Database, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTest(id= 1)
            new_entity.save()

            del new_entity

            with database.getScopedSession() as dbSession:
                assert dbSession.query(ModelTest.id == 1).count() == 1


    def test_save_model_into_database_and_check_its_content(self, database:Database, flaskApp: Flask):
        info="hello there! I'm a testing entity! ;D"
        with flaskApp.app_context():
            new_entity = ModelTest(id= 32, info=info)
            new_entity.save()

            del new_entity

            with database.getScopedSession() as dbSession:
                assert dbSession.query(ModelTest).filter(ModelTest.id == 32).first().info == info

    def test_update_model_in_database_and_check_if_it_was_updated(self,database:Database, flaskApp: Flask):
        old_info="hello there! I'm a testing entity! ;D"
        new_info ="I was updated !!!"
        with flaskApp.app_context():
            new_entity = ModelTest(id= 55, info=old_info)
            new_entity.save()

            del new_entity

            entity = ModelTest.get.one(ModelTest.id==55)
            entity.info = new_info
            entity.update()

            del entity

            with database.getScopedSession() as dbSession:
                assert dbSession.query(ModelTest).filter(ModelTest.id == 55).first().info == new_info
    
    def test_hard_delete_model_in_database_and_check_its_non_existance(self,database:Database, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTest(id= 1, info="hello there! I'm a testing entity! ;D")
            new_entity.save()
            del new_entity

            entity = ModelTest.get.one(ModelTest.id==1)
            entity.delete(method='hard')

            with database.getScopedSession() as dbSession:
                assert dbSession.query(ModelTest).filter(ModelTest.id == 1).first() is None

    def test_soft_delete_model_in_database_and_check_if_deleted_field_is_setted_to_1(self,database:Database, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTest(id= 1, info="hello there! I'm a testing entity! ;D")
            new_entity.save()
            del new_entity

            entity = ModelTest.get.one(ModelTest.id==1)
            entity.delete(method='soft')

            with database.getScopedSession() as dbSession:
                assert dbSession.query(ModelTest).filter(ModelTest.id == 1).first().deleted == 1
        
    def test_query_a_hard_deleted_model_and_return_none(self,database:Database, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTest(id= 1, info="hello there! I'm a testing entity! ;D")
            new_entity.save()
            del new_entity

            entity = ModelTest.get.one(ModelTest.id==1)
            entity.delete(method='hard')

            entity = ModelTest.get.one(ModelTest.id==1)
            assert entity is None

    def test_query_a_soft_deleted_model_and_return_none(self,database:Database, flaskApp: Flask):
        with flaskApp.app_context():
            new_entity = ModelTest(id= 1, info="hello there! I'm a testing entity! ;D")
            new_entity.save()
            del new_entity

            entity = ModelTest.get.one(ModelTest.id==1)
            entity.delete(method='soft')

            entity = ModelTest.get.one(ModelTest.id==1)
            assert entity is None 




    