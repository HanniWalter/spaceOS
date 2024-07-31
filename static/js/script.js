function saveSecretsToCookie() {
    var localIp = $('#secrets #local_ip').text();
    var localPort = $('#secrets #local_port').text();
    var admin  = $('#secrets #admin').text();
    var adminPassword = $('#secrets #admin_password').text();
    if (localIp){
        document.cookie = "local_ip=" + localIp + ";path=/" + ";SameSite=Strict";
    }
    if (localPort){
        document.cookie = "local_port=" + localPort + ";path=/" + ";SameSite=Strict";
    }
    if (admin){
        document.cookie = "admin=" + admin + ";path=/" + ";SameSite=Strict";
    }
    if (adminPassword){
        document.cookie = "admin_password=" + adminPassword + ";path=/" + ";SameSite=Strict";
    }
}

function getCookie(name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value ? value[2] : null;
}

saveSecretsToCookie();

$("#continueGameBtn").on("click", function () {
    player_id = getCookie('player_id');
    session_id = getCookie('session_id');
    if (player_id){
        window.location.href = "/main";
    }
    else{
        window.location.href = "/loginMenu";   
    }
});

$("#newGameBtn").on("click", function () {
    $.post("/newgame", function (data) {
        if (data.success) {
            //getting ip and port from the url
            var url = window.location.href;
            var ip = url.split('/')[2].split(':')[0];
            var port = url.split('/')[2].split(':')[1];
            if (data.admin_passwort){
                // open joinGameAdmin with admin_passwort
                window.location.href = "http://" + ip + ":" + port + "/joinGameAdmin/" + ip + "/" + port+"/"+data.admin_passwort;
            }else{
                window.location.href = "http://" + ip + ":" + port + "/joinGame/" + ip + "/" + port;
            }
        } else {
            alert('cannot create new game');
        }
    });
});

$("#joinMPBtn").on("click", function () {
    window.location.href = "/joinMultiplayer";
});

$("#saveGameBtn").on("click", function () {
    window.location.href = "/saveGameMenu";
});

$("#menu-container #loadGameBtn").on("click", function () {
    window.location.href = "/loadGameMenu";
});

$("#menu-container #deleteGameBtn").on("click", function () {
    $.post("/deleteGame", function (data) {
        if (data.success) {
            alert('game deleted');
            window.location.href = "/mainMenu";
        } else {
            alert('could not delete game');
        }
    });	
});  


$(".actions-container #menuBtn").on("click", function () {
    window.location.href = "/mainMenu";
});

$("#join-game-container #joinGameBtn").on("click", function () {
    var ip = $("#join-game-container #ip").val();
    var port = $("#join-game-container #port").val();
    var url = window.location.href;
    var local_ip = url.split('/')[2].split(':')[0];
    var local_port = url.split('/')[2].split(':')[1];
    window.location.href = "http://" + ip + ":" + port + "/joinGame/" + local_ip + "/" + local_port;
});

function continueToGame(player_id, session_id){
    //cookie
    document.cookie = "player_id=" + player_id + ";path=/" + ";SameSite=Strict";
    document.cookie = "session_id=" + session_id + ";path=/" + ";SameSite=Strict";
    window.location.href = "/main";
}

$("#loginContainer #loginBtn").on("click", function () {
    var name = $("#loginContainer #name").val();
    var password = $("#loginContainer #password").val();
    $.ajax({
        type: 'POST',
        url: '/login',
        data: JSON.stringify({name: name, password: password}),
        contentType: 'application/json',
        success: function (data) {
            continueToGame(data.player_id, data.session_id);
        },
        error: function (data) {
            if (data.status == 401) {
                alert('wrong password');
            }
            if (data.status == 404) {
                alert('user not found');
            }
        }
    });
});

$("#registerContainer #registerBtn").on("click", function () {
    var name = $("#registerContainer #name").val();
    var password = $("#registerContainer #password").val();
    //send as json
    $.ajax({
        type: 'POST',
        url: '/register',
        data: JSON.stringify({name: name, password: password}),
        contentType: 'application/json',
        success: function (data) {
            continueToGame(data.player_id, data.session_id);
        },
        error: function (data) {
            if (data.status == 409) {
                alert('user already exists');
            }
        }
    });
});

savegameselector = $("#savegame-select-container");
if (savegameselector.length) {
    var local_ip = getCookie('local_ip');
    var local_port = getCookie('local_port');
    var url = "http://" + local_ip + ":" + local_port + "/getSavegameData";
    $.ajax({
        type: 'GET',
        url: url,
        contentType: 'application/json',
        success: function (data) {
            if (data.success) {
                var savegames = data.savegame_data;
                if (savegames.length == 0) {
                    //hide savegame selector
                    savegameselector.hide();
                }
                else {
                    $("#nogame-container").hide();
                    savegames.forEach(function (savegame) {
                        $("#savegame-select-container #savegameSelect").append('<option value="' + savegame.name + '">' + savegame.name + '</option>');
                    });
                }
            }
        },
        error: function (data) {
            alert('could not get savegames');
        }
    });
};

function saveGame(name) {
    $.ajax({
        type: 'POST',
        url: '/getSavegame',
        data: JSON.stringify({savegame_name: name}),
        contentType: 'application/json',
        success: function (data) {
            if (data.success) {
                savegame = data.savegame;
                localIp = getCookie('local_ip');
                localPort = getCookie('local_port');
                localurl = "http://"+localIp + ":" + localPort + "/saveSavegame";
                $.ajax({
                    type: 'POST',
                    url: localurl,
                    data: JSON.stringify({savegame: savegame}),
                    contentType: 'application/json',
                    success: function (data) {
                        if (data.success) {
                            alert('game saved');
                            window.location.href = "/mainMenu";
                        } else {
                            alert('could not save savegame to file');
                        }
                    }
                });
            } else {
                alert('could not create savegame');
            }
        }
    });
}

$("#save-container #overwirteBtn").on("click", function () {
    alert("overwrite");
    var name = $("#save-container #savegameSelect").val();
    saveGame(name);
});

$("#save-container #createNewBtn").on("click", function () {
    var name = $("#save-container #name").val();
    saveGame(name);
});

$("#load-container #loadGameBtn").on("click", function () {
    var name = $("#load-container #savegameSelect").val();
    // /loadGame
    $.ajax({
        type: 'POST',
        url: '/loadGame',
        data: JSON.stringify({savegame_name: name}),
        contentType: 'application/json',
        success: function (data) {
            if (data.success) {
                ip = getCookie('local_ip');
                port = getCookie('local_port');
                window.location.href = "http://" + ip + ":" + port + "/joinGame/" + ip + "/" + port;
            } else {
                alert("can't load savegame");
            }
        }
    });
})
