import datetime as dt
import json
import sqlalchemy as sqla
from sqlalchemy import Column, DateTime, ForeignKey, \
    Float, Integer, JSON, String, Sequence, Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists

from .abstractdb import AbstractDB
from .db_registrator import DatabaseRegistrator
from .exceptions import DBConnectionError

@DatabaseRegistrator.register('postgresql')
class PostgresDB(AbstractDB):
    
    Base = declarative_base()
    
    class Users(Base):
        __tablename__ = 'users'
        __table_args__ = {'extend_existing': True}
        id = Column('id', Integer, primary_key=True)
        name = Column('name', String, nullable=False)
        gender = Column('gender', String(1), nullable=False)
        birthdate = Column('birthdate', DateTime)

        def __repr__(self):
            repr = f'User(id: {self.id}, name: {self.name}, '
            repr += f'gender: {self.gender}, birthdate: {self.birthdate})'
            return repr

    class Snapshots(Base):
        __tablename__ = 'snapshots'
        __table_args__ = {'extend_existing': True}
        id = Column('id', Integer, Sequence('snapshot_id_seq'), primary_key=True)
        user_id = Column('user_id', ForeignKey('users.id'))
        timestamp = Column('timestamp', DateTime)
        translation = Column('translation', JSON)
        rotation = Column('rotation', JSON)
        feelings = Column('feelings', JSON)
        color_image = Column('color_image', String) # path
        depth_image = Column('depth_image', String) # path

        def __repr__(self):
            repr = f'Snapshot(id: {self.id}, user_id: {self.user_id}, '
            repr += f'timestamp: {self.timestamp}, '
            repr += f'translation: {self.translation}, '
            repr += f'rotation: {self.rotation}, '
            repr += f'feelings: {self.feelings}, '
            repr += f'color_image: {self.color_image}, '
            repr += f'depth_image: {self.depth_image})'
            return repr

    def __init__(self, engine, connection):
        self.engine = engine
        self.conn = connection
        self.session = sqla.orm.sessionmaker(bind=engine)()
        PostgresDB.Base.metadata.create_all(engine)

    @classmethod
    def connect(cls, url):
        engine = sqla.create_engine(url)
        try:
            db_exists = database_exists(engine.url)
        except sqla.exc.OperationalError as e:
            raise DBConnectionError(e)
        if not db_exists:
            raise DBConnectionError(f'cannot connect to specified database')
        conn = engine.connect()
        return cls(engine, conn)

    def save_data(self, req_data_name, data: dict):
        user_id = data['user_id']
        self.save_user(data)
        timestamp = dt.datetime.fromtimestamp(data['timestamp']/1000)
        new_data = data[req_data_name]
        if isinstance(new_data, list):
            new_data = json.dumps(new_data)
        row = self.session.query(self.Snapshots).filter_by(
            user_id=user_id, timestamp=timestamp).first()
        if row is not None: # snapshot already in db
            # update row
            setattr(row, req_data_name, new_data)
            self.session.commit()
            return
        insert_data = {'user_id': user_id,
                       'timestamp': timestamp,
                       req_data_name: new_data}
        insert = self.Snapshots.__table__.insert().values(**insert_data)
        self.conn.execute(insert)

    def save_user(self, data: dict):
        user_id = data['user_id']
        if self._is_user_in_db(user_id):
            return
        name = data['username']
        gender = data['gender']
        birthdate = dt.datetime.fromtimestamp(data['birthdate'])
        insert = self.Users.__table__.insert().values(
            id=user_id,
            name=name,
            gender=gender,
            birthdate=birthdate)
        self.conn.execute(insert)

    def get_users(self):
        users = self.session.query(self.Users).all()
        ret = []
        for user in users:
            ret.append(user)
        return ret

    def get_user(self, user_id):
        user = self.session.query(self.Users).get(user_id)
        return user

    def get_user_snapshots(self, user_id):
        snapshots = self.session.query(self.Snapshots).filter_by(
            user_id=user_id)
        ret = []
        for snapshot in snapshots:
            ret.append(snapshot)
        return ret

    def get_snapshot(self, user_id, snapshot_id):
        snapshot = self.session.query(self.Snapshots).filter_by(
            id=snapshot_id,
            user_id=user_id
        ).first()
        return snapshot

    def get_data(self, user_id, snapshot_id, result_name):
        snapshot = self.get_snapshot(user_id, snapshot_id)
        if snapshot is None:
            return None
        return getattr(snapshot, result_name)

    def _is_user_in_db(self, user_id):
        return self.session.query(self.Users).get(user_id) is not None


def _object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
        for c in sqla.inspect(obj).mapper.column_attrs}
