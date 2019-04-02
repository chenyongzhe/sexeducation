//send diagnostic output to console
//(Ctrl-Shift-J in Chromium & Firefox to reveal console)

//info variables

var amazelist = ["Amazebowls", "A healthy vegan truck serving a variety of smoothie bowls and drinks", "Monday-Friday, 8am-6pm", "am"];
var armandolist = ["Armando's Lunch Truck", "A hearty lunch truck serving sandwiches, fries, burritos, burgers", "Monday-Friday, 7am-7pm", "ar"]
var truckmanlist = ["Food-Truck Man", "Asian fusion served from a bright pink truck", "Monday-Friday, 9am-5pm", "tr"]

var masterList = [amazelist, armandolist, truckmanlist];

//map

var mymap = L.map("mapid").setView([34.025, -118.285], 16);

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>', Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
    id: "mapbox.streets",
    accessToken: "pk.eyJ1Ijoia2F0ZWx5aiIsImEiOiJjanJqbDM1azcwZHQ3NDNvM3kyYzcyYmxkIn0.9mj3cfrLubaTrN9pm1jazw"
}).addTo(mymap);

//popups

var amaze = L.marker([34.024204, -118.283840]).addTo(mymap);
amaze.bindPopup("<b>Amazebowls</b><br>Smoothies and Acai Bowls<br><a href='#' onclick='infoDisplay(0)'>[More Info]</a>");

var armando = L.marker([34.023895, -118.283992]).addTo(mymap);
armando.bindPopup("<b>Armando's Lunch Truck (Location #1)</b><br>Sandwiches, Burritos, and More<br><a href='#' onclick='infoDisplay(1)'>[More Info]</a>");
var armando2 = L.marker([34.025743, -118.286648]).addTo(mymap);
armando2.bindPopup("<b>Armando's Lunch Truck (Location #2)</b><br>Sandwiches, Burritos, and More<br><a href='#' onclick='infoDisplay(1)'>[More Info]</a>");

var truckman = L.marker([34.025798, -118.288564]).addTo(mymap);
truckman.bindPopup("<b>Food Truck-Man</b><br>Asian Fusion<br><a href='#' onclick='infoDisplay(2)'>[More Info]</a>");

//info links

var infoDisplay = function(num) {

    document.getElementById("infoArea").innerHTML = "";

    //name
    var n = document.createElement("H2");
    n.innerHTML = "<br>" + masterList[num][0];
    //description
    var b = document.createElement("P");
    b.innerHTML = "<i>" + masterList[num][1] + "</i>";
    //hours
    var h = document.createElement("P");
    h.innerHTML = "<b>Hours:<br></b>" + masterList[num][2];
    //link
    var l = document.createElement("P")
    l.innerHTML = "<a href=#" + masterList[num][3] + " class='scrollLink'>Read More</a><br><br><br></center>";

    document.getElementById("infoArea").appendChild(n);
    document.getElementById("infoArea").appendChild(b);
    document.getElementById("infoArea").appendChild(h);
    document.getElementById("infoArea").appendChild(l);

}

//scrolling to a section

$(document).ready(function(){
    $( "a.scrollLink" ).click(function( event ) {
        event.preventDefault();
        $("html, body").animate({ scrollTop: $($(this).attr("href")).offset().top }, 5000);
    });
});