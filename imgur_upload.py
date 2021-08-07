import pyimgur
from secrets import imgur_client_id

CLIENT_ID = imgur_client_id
PATH = "static/restaurant_map.png"

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.size)
print(uploaded_image.type)