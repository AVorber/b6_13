from bottle import HTTPError
from bottle import request
from bottle import route
from bottle import run

import album


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {}:<br>".format(artist)
        result += "<br>".join(album_names)
        result += f'<br>Всего {len(albums_list)} альбомов.'
    return result


@route("/albums", method="POST")
def create_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    if not isinstance(year, int) or isinstance(artist, str) or isinstance(genre, str) or isinstance(album, str):
        raise HTTPError(400, "Указан некорректный год альбома")
    if not isinstance(artist, str):
        raise HTTPError(400, "Указано некорректное имя артиста")
    if not isinstance(genre, str):
        raise HTTPError(400, "Указан некорректный жанр альбома")
    if not isinstance(album, str):
        raise HTTPError(400, "Указано некорректный название альбома")

    try:
        new_album = album.save(year, artist, genre, album_name)
    except album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:
        print("New #{} album successfully saved".format(new_album.id))
        result = "Альбом #{} успешно сохранен".format(new_album.id)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
