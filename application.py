from flask import Flask, render_template, Response, request
application = Flask(__name__)

@application.route('/')
def index():
  return render_template('index.html')

@application.route('/about.html')
def about():
  return render_template('about.html')

@application.route('/my-link/')
def my_link():
  return render_template('result.html', data=data)

@application.route('/my-link/', methods=['GET', 'POST'])
def give_result():

    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

    client_id = ####
    client_secret = ####

    pop_list = list()
    song_list = list()
    related_list = list()
    genres_list = list()


    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    #using the Spotipy library in order to use the Spotify API
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    artist_name = request.form['artist']
    song_name = request.form['song']
    track_results = spotify.search(q=artist_name, type='artist', limit=50)
    artist_list = track_results['artists']
    items = artist_list['items']
    if len(items) != 0:
      the_artist = items[0] 
    else:
      data = "There was an error in either the name of the artist or the name of the song, please try again."
      chosen_url = "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
      return render_template('result.html', data=data, chosen_image=chosen_url, songs=song_list)
    
    artist_id = the_artist['id']
    track_object = spotify.artist_top_tracks(artist_id)
    tracks = track_object['tracks']
    images = the_artist['images']
    chosen_image = images[0]
    chosen_url = chosen_image['url']
    popularity = the_artist['popularity']
    genres = the_artist['genres']
    followers = the_artist['followers']
    num_followers = followers['total']

    related_artists = spotify.artist_related_artists(artist_id)
    nonunique = 0

    #checks if the artist has at least 5 songs
    if len(tracks) > 4:
        for i in range(5):
            curr_track = tracks[i]
            pop_list.append(curr_track['popularity'])
            song_list.append(curr_track['name'])        
    else:
        data = "This artist has fewer than 5 songs so it cannot be determined if they are a one hit wonder."
        return render_template('result.html', data=data, chosen_image=chosen_url, songs=song_list)

    first_track = tracks[0]
    artist_list = related_artists['artists']
    length = len(artist_list)

    #gets list of related artists
    for i in range(length):
      curr_artist = artist_list[i]
      curr_name = curr_artist['name']
      related_list.append(curr_name)
    length2 = len(genres)

    #gets list of genres for artist
    for i in range(length2):
      curr_genre = genres[i]
      genres_list.append(curr_genre)
    pop_sum = 0
    pop_num = 0

    if first_track['name'].find(song_name) != -1 and first_track['name'] != song_name:
      data = "This song is not a one hit wonder as it is not the artist's most popular song."
      diff = "N/A as it is not the artist's most popular song."
      return render_template('result.html', data=data, chosen_image=chosen_url, songs=song_list, pop=popularity, genre=genres_list, num=num_followers, related=related_list, diff_score=diff)
    else: #checks whether the artist has at least 5 songs none of which are different version of the same song
        for x in song_list:
          if x.find(song_name) != -1:
            nonunique += 1
        if nonunique > 1:
          for i in range(1,len(song_list)):
            if song_list[i].find(song_name) != -1:
              pop_sum += pop_list[i]
              pop_num += 1
          diff = pop_list[0] - (pop_sum/pop_num)
          if diff > 17.25: #17.25 is the diff number corresponding to the 85th percentile based on the diffs scores calculated in percentile.py
            data = "This song is a one hit wonder."
            return render_template('result.html', data=data, chosen_image=chosen_url, songs=song_list, pop=popularity, genre=genres_list, num=num_followers, related=related_list, diff_score=diff)
          else:
            data = "This song is not a one hit wonder."
            return render_template('result.html', data=data, chosen_image=chosen_url, songs=song_list, pop=popularity, genre=genres_list, num=num_followers, related=related_list, diff_score=diff)
        
        
    diff = pop_list[0] - (pop_list[1] + pop_list[2] + pop_list[3] + pop_list[4])/4
    if diff > 17.25:
        data = "This song is a one hit wonder."
        return render_template('result.html', data=data, chosen_image=chosen_url, songs=song_list, pop=popularity, genre=genres_list, num=num_followers, related=related_list, diff_score=diff)
    else:
        data = "This song is not a one hit wonder."
        return render_template('result.html', data=data, chosen_image=chosen_url, songs=song_list, pop=popularity, genre=genres_list, num=num_followers, related=related_list,diff_score=diff)
    chosen_url = "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80"
    #displays the data
    return render_template('result.html', data=data, chosen_image=chosen_url, songs=song_list, pop=popularity, genre=genres_list, num=num_followers, related=related_list, diff_score=diff)

if __name__ == '__main__':
  application.run(debug=True)