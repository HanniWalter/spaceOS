document.getElementById('menuBtn').addEventListener('click', function () {
    window.location.href = '/';
});

document.getElementById('reloadOssBtn').addEventListener('click', function () {
    fetch('/reload_oss', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/main';
            } else {
                alert('Error reloading OSS');
            }
        });
});

document.getElementById('newShipBtn').addEventListener('click', function () {
    window.location.href = '/ShipDesigner/new';
});
var os_containers = document.getElementsByClassName('os-container');
for (var i = 0; i < os_containers.length; i++) {
    
    var buildOsBtn = os_containers[i].getElementsByClassName('buildOsBtn')[0];
    const id = os_containers[i].id;
    buildOsBtn.addEventListener('click', function () {
        fetch('/build_os/' + id, {
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
                    alert('Error building OS');
                }
            });
    });
}
;

var containers = document.getElementsByClassName("ship-container");
    for (var i = 0; i < containers.length; i++) {
        const id = containers[i].id;

        //for every ship-container, add event listener
        
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