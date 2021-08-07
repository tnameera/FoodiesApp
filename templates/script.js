// var axios = require('axios');
// const jquery = require('jquery');

// fetch('https://foodiesapi.siddhantpor.repl.co/')
//   .then(response => response.json())
//   .then(data => console.log(data));

// // i'm currently working on foodies api itself and then once it is working for sure will edit the script ~siddhant

    // axios('https://foodiesapi.siddhantpor.repl.co/', {
    //   method: 'GET',
    //   params: {
    //     place: /*restPlc*/'seattle',    // REMOVED PLACEHOLDER SEATTLE
    //     name: /*restName*/'starbucks',    // discuss user should define
    //     open_now: true, // default -- user input doesn't define this
    //     price: 2, // user should define 
    //     rating: 4,    // user should define  
    //     categories: 'coffee' // user should define  
    //   },
    //   mode: "cors"
    // }).then((data) => {

      
    //   /*
    //    code to add to google map + code for showing the data on ui as options (?)
       
    //    i think google map/leaflet api should use the coordinates of each restaurant in the data received and then plot it.... maybe implementing the entire address is hard, so since the data gives coordinates, we can just give the google map api the coordinates and say "plot these coordinates: {coordinates}" 
    //   */
    //   console.log(data.data)
    // });