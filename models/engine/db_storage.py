#!/usr/bin/python3
'''
    Database Storage Module
'''

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from models.base_model import Base


class DBStorage():
    '''
    '''

    __engine = None
    __session = None

    def __init__(self):
        '''
        '''
        from models.base_model import Base
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if ('HBNB_ENV' == 'test'):
            Base.metadata.drop_all(self.__engine)
#            self.save()

    def all(self, cls=None):
        '''queries on current database session'''
        import models
        class_list = []
        if cls == None:
            for key, value in models.classes.items():
                class_list.append(value)
        else:
            print("IN HERE")
            if cls in models.classes:
                class_list = [cls]
        new_dict = {}
        print(class_list)
        for search in class_list:
            print(search)
            capture = self.__session.query(search).all()
            for objects in capture:
                key = str(objects.__class__.__name__) + '.' + objects.id
                new_dict[key] = objects
        return new_dict

    def new(self, obj):
        '''adds the object to current db session'''
        self.__session.add(obj)

    def save(self):
        '''commits all changes of the current db session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''deletes from current db session'''
        if obj is None:
            return
        delete_obj = self.__session.query(type(obj)).filter(type(obj).id )
        self.__session.delete(delete_obj)
        self.save()

    def reload(self):
        '''creates all tables in database'''
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
