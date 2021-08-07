from os import name
from flask import Flask, redirect, url_for , render_template,request # redirtect-return or redirect from  aspecific function
                                                             # render_template will render html page
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask_googlemaps import icons
import requests
import json
import pandas as pd 
import folium
import io
from pathlib import Path
from PIL import Image

from twilio.rest import Client
from secrets import twilio_sid, twilio_auth, twilio_phone_number, my_phone_number

from secrets import your_api_key 
from secrets import yelp_api_key

import pyimgur
from secrets import imgur_client_id
# easy to use wiht python to access the apu 

account_sid = twilio_sid
auth_token = twilio_auth
client = Client(account_sid, auth_token)

app = Flask(__name__)

NUM_RESTAURANTS = 10

app.config['TEMPLATES_AUTO_RELOAD'] = True
# you can set key as config
GoogleMaps(app, key="your_api_key")
# api keys and url



headers = {'Authorization': 'Bearer %s' % yelp_api_key}
url='https://api.yelp.com/v3/businesses/search'

def yelp(term,location,limit):
    params = {'term': term,# In the dictionary, n take values like food, cafes or businesses like McDonalds
    'location':location , 
    'limit': limit}
    req=requests.get(url, params=params, headers=headers)# Making a get request to the API
    return(json.loads(req.text)['businesses'])

def price_to_int(dollar):
    if dollar == "$":
        return 1
    elif dollar == "$$":
        return 2
    elif dollar == "$$$":
        return 3
    else:
        return 4

# delete all existing maps html 
files = sorted(Path('static/').glob('*.html'))
for file in files:
    if 'restaurant_locations' in str(file):
        Path(file).unlink()

# home page
@app.route("/", methods = ["POST" , "GET"]) #setup login page
def home():
    if request.method == "POST":
        print(request.form)
        if request.form['action'] == 'Search':
            location = request.form["location"]
            term = request.form["term"]
            
            loc_term = pd.DataFrame({'location':[location],
                                     'term':[term]})
            loc_term.to_csv('loc_term.csv',index=False)                     

            api_data = yelp(location=location, term=term, limit=NUM_RESTAURANTS)# api data call, send the request and get back all this necessary info
            #the following lists are to store information about the restaurants

            print(api_data)

            names = []# empty list fill them out with data. all points we need
            images = []
            url = []
            addresses = []
            addresses1 = []
            addresses2 = []
            prices = [] # looks like $, $$, $$$, $$$$
            prices_int = [] # int of price 1,2,3,4
            ratings = []
            categories = []
            latitude = []
            longitude = []

            # little check if we show less than 3 restaurants
            # not needed anymore, but i thought I was going to need it 
            idx = 0
            while len(api_data) < 3: # incase you have less than 3 return then repeat the first one
                api_data.append(api_data[idx])
                idx += 1

            for i in range( min(NUM_RESTAURANTS, len(api_data)) ):# loop through restaurants
                # used a try except here because sometimes some queries dont return a price
                # is a price or some other field doesn't exist in the dictionary then it generates a keyerror
                # at this point try has failed and it goes to the except clause which skips the current step and goes to next iteration of loop
                try:
                    prices_int.append(price_to_int(api_data[i]['price']))#dictionary and loading in panda data frame has rows and col(name, price, rating)
                    prices.append(api_data[i]['price'])
                    ratings.append(api_data[i]['rating'])
                    names.append(api_data[i]['name'])
                    images.append(api_data[i]['image_url'])
                    addresses.append(", ".join(api_data[i]['location']['display_address']))
                    addresses1.append(api_data[i]['location']['display_address'][0] )
                    addresses2.append(api_data[i]['location']['display_address'][1] )
                    categories.append(api_data[i]['categories'])
                    latitude.append(api_data[i]['coordinates']['latitude'])
                    longitude.append(api_data[i]['coordinates']['longitude'])
                    url.append(api_data[i]['url'])
                except KeyError:
                    continue
            
            min_len = min(len(prices), # tryign to fidn the length of the smallest list. since data frame has square object
                          len(ratings),
                          len(names),
                          len(images),
                          len(addresses1))    

            data = pd.DataFrame({ # pandas dataframe. it has column. construct data frame
                'restaurant':names[:min_len],
                'images':images[:min_len],
                'addresses': addresses[:min_len],
                'addresses1': addresses1[:min_len],
                'addresses2': addresses2[:min_len],
                'price': prices[:min_len],
                'price_int': prices_int[:min_len],
                'rating': ratings[:min_len],
                'categories': categories[:min_len],
                'latitude':latitude[:min_len],
                'longitude':longitude[:min_len],
                'url':url[:min_len]
            }) # each row represents data for a different resurant

            # trying to save the images for restaurants in static folder
            for i in range(len(data)):
                r = requests.get(data.loc[i,'images'], allow_redirects=True)
                open('static/image'+ str(i)+'.jpg','wb').write(r.content)

            print(data)# data. csv to dispaly. pandas
            #save the data
            data.to_csv('data.csv',index=False)

            new_data = data[['restaurant', 'price', 'rating']]# basically the 2nd table. We are woking with 3 variabels here
            ##We need to add markers for each campus. We're going to iterate through the rows of dataframe to create the markers:

            ##For each row in the file, we find the latitude, longitude, and name of the campus, and use those to create a new marker which we add to our map. We repeat for each row, until we have made markers for all 23 campuses in the file.
            ##Lastly, let's save our map:

            # only way i got this to work is by saving a new file everytime we run this
            # get file name for map file which looks like static/restaurant_locations3.html
            # replace 3 with 4 and load static/restaurant_locations4.htm
            return render_template("searchpage2.html", # render template with all inputs
                            message = "",
                            location = location,
                            term = term, 
                            your_api_key=your_api_key,
                            latitudes=list(data['latitude']), 
                            longitudes=list(data['longitude']),
                            index = list(data.index), # block content2 iterates over the indices
                            names = list(data['restaurant']),
                            prices = list(data['price']),
                            ratings = list(data['rating']),
                            addresses = list(data['addresses']),
                            urls = list(data['url'])
                            )
        elif request.form['action'] == 'Apply':# load up certain things if apply buttom is hit

            loc_term = pd.read_csv('loc_term.csv') 
            location = loc_term.loc[0,'location']
            term = loc_term.loc[0,'term']

            starrating = request.form["starrating"]
            pricelevel = request.form["pricelevel"]
            
            data = pd.read_csv('data.csv')
            # before restrcting data, check if there is at least one result
            # if we dont do this check then we can get website errors
            message = "Results NOT updated due to search criteria too restrictive!" # incase no match
            if ( (data['rating'] >= int(starrating)) & (data['price_int'] >= int(pricelevel)) ).sum() > 0:
                # restrict data to specified star rating and price level
                data = data.loc[(data['rating'] >= int(starrating)) & (data['price_int'] >= int(pricelevel))]
                data = data.reset_index(drop=True)
                message = f"Results updated to Rating: {starrating} and Price: {pricelevel}!"

            print(data)

            new_data = data[['restaurant', 'price', 'rating']]# basically the 2nd table. We are woking with 3 variabels here

            mapnum = 0

            data.to_csv('data.csv',index=False)

            return render_template("searchpage2.html", 
                            message = message,
                            mapnum = str(mapnum),
                            location = location,
                            term = term, 
                            your_api_key=your_api_key,
                            latitudes=list(data['latitude']), 
                            longitudes=list(data['longitude']),
                            tables=[new_data.to_html(classes='data', 
                                    header="true",
                                    justify="center",
                                    index=False)],
                            index = list(data.index),
                            names = list(data['restaurant']),
                            prices = list(data['price']),
                            ratings = list(data['rating']),
                            addresses = list(data['addresses']),
                            urls = list(data['url'])
                            )   
        elif request.form['action'] == 'Send':
            phone = str(request.form["phone"])
            print('Phone:', phone, len(phone))
            loc_term = pd.read_csv('loc_term.csv') 
            location = loc_term.loc[0,'location']
            term = loc_term.loc[0,'term']
            data = pd.read_csv('data.csv')
            print(data)
            new_data = data[['restaurant', 'price', 'rating']]

            map = folium.Map(location=[ data.loc[0,'latitude'], data.loc[0,'longitude'] ])
            ##We need to add markers for each campus. We're going to iterate through the rows of dataframe to create the markers:

            for index,row in data.iterrows():
                lat = row["latitude"]
                lon = row["longitude"]
                name = row["restaurant"]
                newMarker = folium.Marker([lat, lon], popup=name)
                newMarker.add_to(map)

            img_data = map._to_png(5)
            img = Image.open(io.BytesIO(img_data))
            img.save('static/restaurant_map.png')

            im = pyimgur.Imgur(imgur_client_id)
            uploaded_image = im.upload_image('static/restaurant_map.png', title="Uploaded with PyImgur")
            print(uploaded_image.title)
            print(uploaded_image.link)

            media_url = uploaded_image.link
            
            body_text = ("Let's dine at one of these restaurants: " + 
                        ", \n".join(list( data['restaurant']+
                        '( Rating: '+data['rating'].astype(str) +
                        ' Price: '+ data['price'].astype(str) +')')) 
                        )

            if len(phone.strip()) != 10:
                phone = my_phone_number


            message1 = client.messages \
                            .create(
                                body=body_text,
                                media_url=media_url,
                                from_=twilio_phone_number, 
                                to=phone
                            )
            print(message1.sid)
            mapnum = 0
            return render_template("searchpage2.html", 
                            message = "Text has been sent!",
                            mapnum = str(mapnum),
                            location = location,
                            term = term, 
                            your_api_key=your_api_key,
                            latitudes=list(data['latitude']), 
                            longitudes=list(data['longitude']),
                            tables=[new_data.to_html(classes='data', 
                                        header="true",
                                        justify="center",
                                        index=True)],
                            index = list(data.index),
                            names = list(data['restaurant']),
                            prices = list(data['price']),
                            ratings = list(data['rating']),
                            addresses = list(data['addresses']),
                            urls = list(data['url'])
                            ) 

    else: # GET methos so no sumitting of any input through forms 
        #map = folium.Map(location=[40.7128, -74.0060])
        #map.save(outfile='static/restaurant_locations0.html')
        #mapnum = 0  

        return render_template("searchpage.html", 
                                your_api_key=your_api_key,  
                                latitudes=[40.75961], 
                                longitudes=[-73.9698] )

# home page
@app.route("/about", methods = ["POST" , "GET"]) #setup login page
def aboutus():
    return render_template('aboutus.html')

@app.route("/contact", methods = ["POST" , "GET"]) #setup login page
def contactus():
    return render_template('contactus.html')

    
if __name__ == "__main__":
    app.run(debug=True)