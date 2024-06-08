document.getElementById('joinGameBtn')?.addEventListener('click', function () {
    var hostIP = document.getElementById('IP').value;
    var hostPort = document.getElementById('port').value; 
    var data = {
        hostIP: hostIP,
        hostPort: hostPort
    };
    //set cookie with hostIP and hostPort
    document.cookie = JSON.stringify(data);
    //redirect to /joinGame on hosturl and hostport
    document.location.href = 'http://'+hostIP+':'+hostPort+'/joinGame';
});

document.getElementById('menuBtn')?.addEventListener('click', function () {
    window.location.href = '/main_menu';
});