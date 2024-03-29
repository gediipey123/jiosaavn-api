from flask import Flask, request, jsonify, url_for
import requests
from des import decipher

app = Flask(__name__)

app.add_url_rule('/favicon.ico',
                 redirect_to=url_for('static', filename='favicon.ico'))

@app.route('/')
def index():
    return 'hello'

@app.route('/api/search/songs/')
def searchSongs():
    query = request.args.get('q')
    page = '1' if request.args.get('p') == None or request.args.get('p') == "" else request.args.get('p')
    if query == "" or query == None:
        return jsonify({"Error":"Please Provide a Query"})
    res = requests.get(f'https://www.jiosaavn.com/api.php?__call=search.getResults&_format=json&_marker=0&cc=in&includeMetaTags=1&p={page}&q={query}')
    li = []
    for song in res.json()["results"]:
        li.append({
            "album" : song["album"],
            "artists": song["singers"] if song["singers"] != "" else "Various Artists",
            "id": song["id"],
            "streamUrl": {
              "12kbps" : decipher(song["encrypted_media_url"]).replace("_96", "_12"),
              "48kbps" : decipher(song["encrypted_media_url"]).replace("_96", "_48"),
              "96kbps" : decipher(song["encrypted_media_url"]),
              "160kbps" : decipher(song["encrypted_media_url"]).replace("_96", "_160"),
              "320kbps" : decipher(song["encrypted_media_url"]).replace("_96", "_320") if song["320kbps"] == "true" else "",
            },
            "thumbnailUrl": {
              "50X50" : song["image"].replace('150x150','50x50'),
              "150X150": song["image"],
              "500X500": song["image"].replace('150x150','500x500')  
            },
            "title": song["song"]
        })
    return jsonify({"results": li})

@app.route('/api/search/albums/')
def searchAlbums():
    query = request.args.get('q')
    page = '1' if request.args.get('p') == None or request.args.get('p') == "" else request.args.get('p')
    if query == None or query == "":
        return "Please enter a valid query"
    res = requests.get(f'https://www.jiosaavn.com/api.php?__call=search.getAlbumResults&_format=json&_marker=0&cc=in&includeMetaTags=1&q={query}&p={page}')
    li = []
    for album in res.json()["results"]:
        li.append({
            "album_id": album["albumid"],
            "artists": album["primary_artists"],
            "thumbnailUrl": {
               "50X50": album["image"].replace('150x150','50x50'),
               "150X150": album["image"],
               "500X500": album["image"].replace('150x150','500x500'),
            },
            "title": album["title"],
            "year": album["year"]
        })
    return jsonify(li)

@app.route('/api/search/artists/')
def searchArtists():
    query = request.args.get('q')
    if query == None or query == "":
        return "Please enter a valid query"
    res = requests.get(f'https://www.jiosaavn.com/api.php?__call=search.getArtistResults&_format=json&_marker=0&cc=in&includeMetaTags=1&q={query}')
    return res.json()

@app.route('/api/search/playlists/')
def searchPlaylist():
    query = request.args.get('q')
    if query == None or query == "":
        return "Please enter a valid query"
    res = requests.get(f'https://www.jiosaavn.com/api.php?__call=search.getPlaylistResults&_format=json&_marker=0&cc=in&includeMetaTags=1&q={query}')
    return res.json()

if __name__ == '__main__':
    app.run(debug=True)
