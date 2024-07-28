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

saveSecretsToCookie();

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

$(".actions-container #menuBtn").on("click", function () {
    window.location.href = "/main_menu";
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