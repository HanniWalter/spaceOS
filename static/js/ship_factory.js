document.getElementById('mainBtn').addEventListener('click', function () {
    window.location.href = '/main';
});

document.getElementById('shipname').addEventListener('input', function () {
//maybe using oninput instead of onchange
    values_changed();
});

document.getElementById('os-select').addEventListener('change', function () {
    values_changed();
});

function isNewShip() {
    var r = document.getElementById('is new').innerText;
    if (r == 'True') return true;
    else return false
}


function values_changed() {
    var name = document.getElementById('shipname').value;
    var os = document.getElementById('os-select').value;
    var new_ = isNewShip();
    var r = {name: name, new: new_, os: os};
    fetch('/value_changed', {
        method: 'POST',
        body: JSON.stringify(r),
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

function CreateShip() {
    fetch('/create_spaceship', {
        method: 'POST',
    });
};

function CloneShip() {
    fetch('/clone_spaceship', {
        method: 'POST',
    });
}

function ModifyShip() {
    fetch('/modify_spaceship', {
        method: 'POST',
    });
}

var buildBtn = document.getElementById('BuildBtn');
var cloneBtn = document.getElementById('CloneBtn');
var modifyBtn = document.getElementById('ModifyBtn');

if (buildBtn) {
    buildBtn.addEventListener('click', function () {
        CreateShip();
    });
};

if (cloneBtn) {
    cloneBtn.addEventListener('click', function () {
        CloneShip();
    });
};

if (modifyBtn) {
    modifyBtn.addEventListener('click', function () {
        ModifyShip();
    });
};