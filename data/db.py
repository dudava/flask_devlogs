import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
sessionmaker = None


def create_session() -> orm.Session:
	return sessionmaker()


def init(path):
	global Base, sessionmaker

	if not path.strip():
		return
	if sessionmaker:
		return

	engine = sa.create_engine(f'sqlite:///{path}?check_same_thread=False')

	sessionmaker = orm.sessionmaker(bind=engine)
	Base.metadata.create_all(engine)	

	from . import __all_models
	Base.metadata.create_all(engine)
