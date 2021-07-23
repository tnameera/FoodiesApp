from flask import Flask, redirect, url_for , render_template,request # redirtect-return or redirect from  aspecific function
                                                             # render_template will render html page
import requests
import json
from secrets import your_api_key

app = Flask(__name__)

# api keys and url
api_key= 'pilIhjv7ECYrFIT26sJrGYNbqE_S3guFNHCkj-r3Dc3dVlXe1D8B6t1DcCLffVVuHGTlAr2w6f2q_fylv_dAvbqjmmseD8hu4tvEaxUbrSKpt_0jcJS2moYAhK71YHYx'
headers = {'Authorization': 'Bearer %s' % api_key}
url='https://api.yelp.com/v3/businesses/search'

# home page


def nameera_yelp_api(location, price, term):
    print('nameera')
    return str(location) + str(price) + str(term) 

# function call for yelp api
def api_balsal(term,location,price,limit):
    params = {'term': term,# In the dictionary, n take values like food, cafes or businesses like McDonalds
    'location':location , 
    'price': price,
    'limit': limit}
    req=requests.get(url, params=params, headers=headers)# Making a get request to the API
    return(json.loads(req.text))

@app.route("/", methods = ["POST" , "GET"]) #setup login page
def home():
    if request.method == "POST":
        location = request.form["location"]
        #rating = request.form["rating"]
        price = request.form["price"]
        term = request.form["term"]
        # call yelp api to get buiness information
        print (location, term, price)
        # api key
        #nameera_yelp_api(location, cusine, price) this returns the whol json text
      
        # print for each business name, address and image url
        api_data = api_balsal(location=location, price=price, term=term, limit=5) 
        api_data_string = ":::".join([api_data['businesses'][0]['name'],api_data['businesses'][1]['name'],api_data['businesses'][2]['name']])
        api_data_image_list = [api_data['businesses'][0]['image_url'],api_data['businesses'][1]['image_url'],api_data['businesses'][2]['image_url']]

        for i, url in enumerate(api_data_image_list):
            r = requests.get(url, allow_redirects=True)
            open('static/image'+ str(i)+'.jpg','wb').write(r.content)

            
        api_data_rating = ":::".join([str(api_data['businesses'][0]['rating']),str(api_data['businesses'][1]['rating']),str(api_data['businesses'][2]['rating'])])
        api_data_location = (",".join(api_data['businesses'][0]['location']['display_address']) + ":::" 
            + ",".join(api_data['businesses'][1]['location']['display_address']) + ":::"  
                + ",".join(api_data['businesses'][2]['location']['display_address']) )
        api_data_all_params = "<p>" + api_data_string + "</p>"+"<p>" + api_data_rating + "</p>"+"<p>" + api_data_location + "</p>"
        return redirect(url_for("codedaylabs", 
                                names = api_data_string,
                                locations = api_data_location,
                                your_api_key = your_api_key
        )) # calls funtion user(user1,user_age1)
    else:
        return render_template("base2.html", your_api_key=your_api_key)

@app.route("/<names>/<locations>/", methods = ["POST" , "GET"]) ##setup user page
def codedaylabs(names, locations):
    if request.method == "POST":
        location = request.form["location"]
        #rating = request.form["rating"]
        price = request.form["price"]
        term = request.form["term"]
        # call yelp api to get buiness information
        print (location, term, price)
        # api key
        #nameera_yelp_api(location, cusine, price) this returns the whol json text
      
        # print for each business name, address and image url
        api_data = api_balsal(location=location, price=price, term=term, limit=5) 
        api_data_string = ":::".join([api_data['businesses'][0]['name'],api_data['businesses'][1]['name'],api_data['businesses'][2]['name']])
        api_data_image_list = [api_data['businesses'][0]['image_url'],api_data['businesses'][1]['image_url'],api_data['businesses'][2]['image_url']]

        for i, url in enumerate(api_data_image_list):
            r = requests.get(url, allow_redirects=True)
            open('static/image'+ str(i)+'.jpg','wb').write(r.content)

            
        api_data_rating = ":::".join([str(api_data['businesses'][0]['rating']),str(api_data['businesses'][1]['rating']),str(api_data['businesses'][2]['rating'])])
        api_data_location = (",".join(api_data['businesses'][0]['location']['display_address']) + ":::" 
            + ",".join(api_data['businesses'][1]['location']['display_address']) + ":::"  
                + ",".join(api_data['businesses'][2]['location']['display_address']) )
        api_data_all_params = "<p>" + api_data_string + "</p>"+"<p>" + api_data_rating + "</p>"+"<p>" + api_data_location + "</p>"
        return redirect(url_for("codedaylabs", 
                                names = api_data_string,
                                locations = api_data_location
        )) # calls funtion user(user1,user_age1)
    else:
        names = names.split(':::')
        name1 = names[0]
        name2 = names[1]
        name3 = names[2]

        locations = locations.split(':::')
        locations1 = locations[0]
        locations2 = locations[1]
        locations3 = locations[2]
        return render_template("login3.html", 
                                name1=name1, 
                                name2=name2, 
                                name3=name3,
                                locations1=locations1, 
                                locations2=locations2, 
                                locations3=locations3,
                                your_api_key=your_api_key)# return html
    
if __name__ == "__main__":
    app.run(debug=True)