document.getElementById('mainBtn').addEventListener('click', function () {
    window.location.href = '/main';
});

document.getElementById('reloadMapBtn').addEventListener('click', function () {
    window.location.href = '/map';
});

//load when started the map data from /map_image and put it in map image
fetch('/map_image')
    .then(response => response.json())
    .then(data => {
        document.getElementById('map').src = data.image;
    });