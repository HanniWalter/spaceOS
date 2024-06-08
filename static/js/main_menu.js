document.getElementById('newGameBtn')?.addEventListener('click', function () {
    //redo
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

document.getElementById('loadGameBtn')?.addEventListener('click', function () {
    //redo    
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

document.getElementById('saveGameBtn')?.addEventListener('click', function () {
        //redo
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

document.getElementById('continueBtn')?.addEventListener('click', function () {
//redo
    window.location.href = '/main';
});
    
document.getElementById('joinBtn')?.addEventListener('click', function () {
    window.location.href = '/joinMultiplayer';
});

document.getElementById('hostNewGameBtn')?.addEventListener('click', function () {
    window.location.href = '/hostMultiplayer';
});