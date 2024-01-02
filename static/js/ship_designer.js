document.getElementById('menuBtn').addEventListener('click', function () {
    window.location.href = '/';
});

function confirmShip() {
    fetch('/spaceship', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: "spaceship1",
            hull: 10,
            shield: 10,
            id: document.getElementById('shipid').innerHTML,
            operation_system: document.getElementById('os-select').value,
            
        })
    })
        .then(response => response.json())
        .then(data => {
            // Redirect to /main after game is saved
            if (data.success) {
                window.location.href = '/main';
            } else {
                alert('Error saving a game.');
            }
        });
};

document.getElementById('ConfirmBtn').addEventListener('click', function () {
    confirmShip();
});

