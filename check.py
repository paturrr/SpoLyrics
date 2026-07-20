import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as SM

async def main():
    m = await SM.request_async()
    s = m.get_current_session()
    if s:
        print('Session:', s.source_app_user_model_id)
        info = await s.try_get_media_properties_async()
        print('Title:', info.title)
    else:
        print('No media session active')

asyncio.run(main())
