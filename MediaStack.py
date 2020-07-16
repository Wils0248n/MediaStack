import time
from multiprocessing import Process
import sqlalchemy as sa
from mediastack.api.Serializer import Serializer
from mediastack.model.Base import Base
from mediastack.controller import *
from mediastack.api.MediaStackAPI import MediaStackAPI

def create_session() -> sa.orm.Session:
    engine = sa.create_engine('sqlite:///MediaStack.db', connect_args={'check_same_thread': False})
    Base.metadata.create_all(bind=engine)
    session_maker = sa.orm.sessionmaker(bind=engine)
    return session_maker()

session = create_session()

media_manager = MediaManager(session)
search_manager = SearchManager(session)
media_initializer = MediaInitializer(media_manager)
api = MediaStackAPI(media_manager, search_manager)

def _media_initializtion_process() -> None:
    while True:
        media_initializer.initialize_media_from_disk()
        time.sleep(10)

if __name__ == '__main__':
    try:
        p = Process(target=_media_initializtion_process)
        p.start()

        api.run()

        p.join()
    except KeyboardInterrupt:
        p.terminate()
