// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see a blank space instead of the map, this
// is probably because you have denied permission for location sharing.

var map;
var driver_markers = [];

function initialize() {
  var mapOptions = {
    zoom: 15
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  // Try HTML5 geolocation
  if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude,
                                       position.coords.longitude);
      var westBusStop = new google.maps.LatLng(36.000936,
                                              -78.938264);

      var eastBusStop = new google.maps.LatLng(36.006035,
                                              -78.914739);

      var distToWest = google.maps.geometry.spherical.computeDistanceBetween (pos, westBusStop);
      var distToEast = google.maps.geometry.spherical.computeDistanceBetween (pos, eastBusStop);

      // var infowindow = new google.maps.InfoWindow({
      //   map: map,
      //   position: pos,
      //   content: 'You\'re here'
      // });
    
    var westWindow = new google.maps.InfoWindow({
      map: map,
      position: westBusStop,
      content: getLocationHTML('West Bus Stop', distToWest)
    });

    var eastWindow = new google.maps.InfoWindow({
      map: map,
      position: eastBusStop,
      content: getLocationHTML('East Bus Stop', distToEast)
    });

    window.setInterval(function(){
      clearDriverMarkers();
      $.ajax({
        type: "GET",
        url: "get_driver_locs"
      }).success(function(data) {
        for(var i = 0; i < data.length; i++) {
          var pos = new google.maps.LatLng(data[i]['lat'],
                                           data[i]['long']);
          var driverMarker = new google.maps.InfoWindow({
            map: map,
            position: pos,
            content: data[i]['name']
          });
          driver_markers.push(driverMarker);
        }
      });
    }, 10000)

      map.setCenter(westBusStop);
      


    }, function() {
      handleNoGeolocation();
    });
  } else {
    // Browser doesn't support Geolocation
    handleNoGeolocation();
  }
}

function clearDriverMarkers() {
  for(var i = 0; i < driver_markers.length; i++) {
    driver_markers[i].setMap(null);
  }
  driver_markers = [];
}


function getLocationHTML(locTitle, dist) {
  var distStatus;
  var color;
  var formHTML = "";
  if(dist > 100) {
    distStatus = 'Click to request ride';
    color = 'green';
    formHTML = "<form method='get' action='/students/dropoff_locations'><input type='hidden' name='pickup' value='" + locTitle + "'><button type='submit' class='btn btn-default btn-lg'>Request Ride</button></form>";
    html += formHTML;
  }
  else {
    distStatus = 'Too far away';
    color = 'red';
  }
  var upperHTML = "<p><strong style='color: "+ color +"'>" + locTitle + "</strong><br />" + 
          distStatus + "<br />0 groups <br />";
  var html = upperHTML + formHTML + "</p>";
  return html;
}

function handleNoGeolocation() {
  window.location = window.location.origin += "/students/pickup_locations"
}

google.maps.event.addDomListener(window, 'load', initialize);