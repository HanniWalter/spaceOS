document.addEventListener('DOMContentLoaded', function () {
    // Fetch status for load and save buttons
    fetch('/savegames')
        .then(response => response.json())
        .then(data => {
            if (data.savegames.length == 0) {
                document.getElementById('loadGameBtn').disabled = true;
            }
        });

    fetch('/game')
        .then(response => response.json())
        .then(data => {
            if (data.initiated == false) {
                document.getElementById('saveGameBtn').disabled = true;
                document.getElementById('continueBtn').disabled = true;
            }
        });

    // Add event listeners to buttons
    document.getElementById('newGameBtn').addEventListener('click', function () {
        // Call API endpoint for new game newgame with POST method

        fetch('/newgame', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                // Redirect to /main after new game is created
                if (data.success) {
                    window.location.href = '/main';
                } else {
                    alert('Error creating a new game.');
                }
            });
        
    });

    document.getElementById('loadGameBtn').addEventListener('click', function () {
        // Call API endpoint for loading game loadgame with POST method
        fetch('/loadgame', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                // Redirect to /main after game is loaded
                if (data.success) {
                    window.location.href = '/main';
                } else {
                    alert('Error loading a game.');
                }
            });
    });

    document.getElementById('saveGameBtn').addEventListener('click', function () {
        // Call API endpoint for saving game savegame with POST method
        fetch('/savegame', {
            method: 'POST'
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
    });

    document.getElementById('continueBtn').addEventListener('click', function () {
        window.location.href = '/main';
    });
    
    document.getElementById('guideBtn').addEventListener('click', function () {
        // Add guide functionality here
        alert('Guide button clicked.');
    });

});