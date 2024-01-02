document.getElementById('menuBtn').addEventListener('click', function () {
    window.location.href = '/';
});

document.getElementById('newShipBtn').addEventListener('click', function () {
    window.location.href = '/ShipDesigner/new';
});

var containers = document.getElementsByClassName("ship-container");
    for (var i = 0; i < containers.length; i++) {
        //for every ship-container, add event listener
        var id = containers[i].id;
        //get child button of class inspectShipBtn
        var inspectBtn = containers[i].getElementsByClassName("inspectShipBtn")[0];
        inspectBtn.addEventListener('click', function () {
            alert("Inspecting " + id);
        });
        var modifyBtn = containers[i].getElementsByClassName("modifyShipBtn")[0];
        modifyBtn.addEventListener('click', function () {
            window.location.href = '/ShipDesigner/' + id;
        });
        var consoleBtn = containers[i].getElementsByClassName("consoleShipBtn")[0];
        consoleBtn.addEventListener('click', function () {
            fetch('/attach_console/' + id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = '/main';
                    } else {
                        alert('Error attaching console');
                    }
                });
        });
        var startBtn = containers[i].getElementsByClassName("startShipBtn")[0];
        startBtn.addEventListener('click', function () {
            fetch('/start_spaceship/' + id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = '/main';
                    } else {
                        alert('Error starting spaceship');
                    }
                });
        });
    
    }