import os
import requests
import aiohttp
import yt_dlp

from pyrogram import filters, Client
from youtube_search import YoutubeSearch

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.command('song') & ~filters.private & ~filters.channel)
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('๐๐ถ๐ป๐ฑ๐ถ๐ป๐ด ๐ง๐ต๐ฒ ๐ฆ๐ผ๐ป๐ด ๐๐ผ๐ฟ๐บ ๐ฆ๐ฒ๐ฟ๐๐ฒ๐ฟ...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "๐ฆ๐ผ๐ป๐ด ๐ก๐ผ๐ ๐๐ผ๐๐ป๐ฑ..."
        )
        print(str(e))
        return
    m.edit("๐๐ผ๐๐ป๐น๐ผ๐ฎ๐ฑ ๐ฆ๐ผ๐ป๐ด ๐๐ฟ๐ผ๐บ ๐ฆ๐ฒ๐ฟ๐๐ฒ๐ฟ...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = '**๐ต ๐จ๐ฝ๐น๐ผ๐ฎ๐ฑ๐ฒ๐ฑ ๐๐ : @AboutHexor๏ธ**'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit('๐๐ฒ๐๐ผ๐ฟ ๐ก๐ผ๐ ๐๐ถ๐๐ฒ ๐ฃ๐ฒ๐ฟ๐บ๐ถ๐๐๐ถ๐ผ๐ป ๐๐ผ๐ฟ ๐๐ถ๐๐ถ๐ป๐ด ๐ฌ๐ผ๐ ๐ฆ๐ผ๐ป๐ด ๐๐ฟ๐ผ๐บ ๐ฆ๐ฒ๐ฟ๐๐ฒ๐ฟ...')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
