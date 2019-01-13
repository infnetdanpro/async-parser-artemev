from sqlalchemy.orm import *
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///D:\\Python37\\Scripts\\async_requests\\test_db.db", echo=True)
Base = declarative_base()

class Title(Base):
    __tablename__ = 'title_table'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)

    def __repr__(self):
        return "<Row(id='{}', url='{}', title='{}')>".format(self.id, self.url, self.title)

    def __init__(self):
        self.metadata.create_all(engine)

#data_list должен быть списком
def sql_work(data_list):
    title = Title()
    Session = sessionmaker(bind=engine)
    session = Session()

    temp_obj = []
    for d in data_list:
        temp_obj.append(Title(url=d, title=data_list[d]))

    try:
        session.add_all(temp_obj)
        session.commit()
        print('DB Ok!')
    except:
        session.rollback()

    session.close()