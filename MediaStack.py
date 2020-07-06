import time, asyncio
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

async def _media_initializtion_process(media_initializer: MediaInitializer) -> None:
    while True:
        media_initializer.initialize_media_from_disk()
        await asyncio.sleep(10)

def cache_serializations(search_manager: SearchManager) -> None:
    result = search_manager.search(None)
    for media in result[0]:
        Serializer.serialize(media)
    for album in result[1]:
        Serializer.serialize(album)

def main():

    session = create_session()

    media_manager = MediaManager(session)
    search_manager = SearchManager(session)
    media_initializer = MediaInitializer(media_manager)

    cache_serializations(search_manager)

    media_initializer.initialize_media_from_disk()
    #loop = asyncio.get_event_loop()
    #loop.create_task(_media_initializtion_process(media_initializer))
    MediaStackAPI(media_manager, search_manager).run()
    #loop.run_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
