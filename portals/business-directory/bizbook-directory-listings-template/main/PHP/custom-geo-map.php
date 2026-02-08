<?php
//database configuration

$footer_row = getAllFooter(); //Fetch Footer Data
if (isset($_SESSION['lati']) && isset($_SESSION['longi'])) {
    $default_latitude = $_SESSION['lati'];
    $default_longitude = $_SESSION['longi'];
    $default_zoom = 10;
}else{
    if (isset($_SESSION['latitude']) && isset($_SESSION['longitude'])) {
        $default_latitude = $_SESSION['latitude'];
        $default_longitude = $_SESSION['longitude'];
        $default_zoom = 6;
    } else {
        $default_latitude = $footer_row['admin_geo_default_latitude'];
        $default_longitude = $footer_row['admin_geo_default_longitude'];
        $default_zoom = $footer_row['admin_geo_default_zoom'];
    }
}

?>
<script>
    var customLabel = {
        restaurant: {
            label: 'R'
        },
        bar: {
            label: 'B'
        }
    };


    function initMap() {

        var map = new google.maps.Map(document.getElementById('map-view'), {
            center: new google.maps.LatLng(<?php echo $default_latitude; ?>, <?php echo $default_longitude; ?>),
            zoom: <?php echo $default_zoom; ?>
        });
        var infoWindow = new google.maps.InfoWindow;

        // Change this depending on the name of your PHP or XML file
        downloadUrl('<?php echo $webpage_full_link; ?>map-view-process.php', function (data) {

//        downloadUrl('https://storage.googleapis.com/mapsdevsite/json/mapmarkers2.xml', function(data) {

            var xml = data.responseXML;

            if(xml == null){
                document.getElementById("map-error-box").style.display = "block";
            }

            var markers = xml.documentElement.getElementsByTagName('marker');

            Array.prototype.forEach.call(markers, function (markerElem) {

                var id = markerElem.getAttribute('id');
                var code = markerElem.getAttribute('code');
                var name = markerElem.getAttribute('name');
                var slug = markerElem.getAttribute('slug');
                var address = markerElem.getAttribute('address');
                var type = markerElem.getAttribute('type');
                var image = markerElem.getAttribute('image');

                if (image == null) {
                    image = "hot4.jpg";
                } else {
                    image = image;
                }
                var point = new google.maps.LatLng(
                    parseFloat(markerElem.getAttribute('lat')),
                    parseFloat(markerElem.getAttribute('lng')));

                var infowincontent = document.createElement('div');

                var link = document.createElement('a'); // create the link

                var url_name = slug.replace(/\s+/g,"-"); //replace the space with hypen on listing name

                var href_url = 'listing/'+ url_name; //new updated URL for listing details

                link.setAttribute('href', href_url); // set link path


                //Photo elements starts
                var elem = document.createElement("img");

                elem.setAttribute("src", "images/listings/" + image);
                elem.setAttribute("height", "100");
                elem.setAttribute("width", "100");
                elem.setAttribute("alt", name);
                link.appendChild(elem); // append to link
                infowincontent.appendChild(link);
                infowincontent.appendChild(document.createElement('br'));
                //Photo elements ends


                //Name elements starts
                var strong = document.createElement('strong');
                strong.textContent = name;
//                infowincontent.appendChild(strong);
                link.appendChild(strong); // append to link
                infowincontent.appendChild(link);
                infowincontent.appendChild(document.createElement('br'));
                //Name elements ends

                //Address elements starts
                var text = document.createElement('text');
                text.textContent = address;
                infowincontent.appendChild(text);
                //Address elements ends

                var icon = customLabel[type] || {};
                var marker = new google.maps.Marker({
                    map: map,
                    position: point,
                    label: icon.label
                });
                marker.addListener('click', function () {
                    infoWindow.setContent(infowincontent);
                    infoWindow.open(map, marker);
                });
            });
        });
    }


    function downloadUrl(url, callback) {
        var request = window.ActiveXObject ?
            new ActiveXObject('Microsoft.XMLHTTP') :
            new XMLHttpRequest;

        request.onreadystatechange = function () {
            if (request.readyState == 4) {
                request.onreadystatechange = doNothing;
                callback(request, request.status);
            }
        };

        request.open('GET', url, true);
        request.send(null);
    }

    function doNothing() {
    }

</script>
