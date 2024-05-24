document.getElementById('mainBtn').addEventListener('click', function () {
    window.location.href = '/main';
});

document.getElementById('reloadMapBtn').addEventListener('click', function () {
    window.location.href = '/map';
});


display_config = {
    "width": 800,
    "height": 600,
    "scale": 4,
    "central_location": {"x" : 0, "y" : 0},
};

//load when started the map data from /map_image and put it in map image
fetch('/map_image', {
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(display_config),
    method: 'POST',})
    .then(response => response.json())
    .then(data => {
        document.getElementById('map').src = data.image;
    });