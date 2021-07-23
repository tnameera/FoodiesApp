from flask import Flask, redirect, url_for , render_template,request # redirtect-return or redirect from  aspecific function
                                                             # render_template will render html page
app = Flask(__name__)

# home page
@app.route("/") # / to make it default to go to homepage:
def home():
    return render_template("index3.html")

@app.route("/login" , methods=["POST","GET"]) 
def login():
    if request.method == "POST":
        user1 = request.form["nameera"]
        user_age1 = request.form["age"]
        return user(user1,user_age1)
        #return redirect(url_for("user", usr=user1, user_age=user_age1)) # calls funtion user(user1,user_age1)
    else:
        return render_template("login2.html")

@app.route("/<usr>/<user_age>") 
def user(usr, user_age):
    return f"<h1>{usr}{user_age}</h1>"
    

if __name__ == "__main__":
    app.run(debug=True)
