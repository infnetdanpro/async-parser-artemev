from sqlalchemy.orm import *
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

db_file = '{}\\test_db.db'.format(os.getcwd())
engine = create_engine('sqlite:///{}'.format(db_file), echo=True)
Base = declarative_base()

class Title(Base):
    __tablename__ = 'title_table'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)

    def __repr__(self):
        return "<Row(id='{}', url='{}', title='{}')>".format(self.id, self.url, self.title)
    

#data_list должен быть списком
def sql_work(data_list):
    if os.path.isfile(db_file) == False:
        Title.metadata.create_all(engine)
    title = Title()
    Session = sessionmaker(bind=engine)
    session = Session()

    temp_obj = []
    for d in data_list:
        print(d)
        temp_obj.append(Title(url=d, title=data_list[d]))

    try:
        session.add_all(temp_obj)
        session.commit()
        print('DB Ok!')
    except:
        session.rollback()

    session.close()