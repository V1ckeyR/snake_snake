const COLORS = {
    'r': 'rgb(255, 0, 0)',
    'R': 'rgb(139, 0, 0)',
    'o': 'rgb(255, 165, 0)',
    'O': 'rgb(255, 140, 0)',
    'y': 'rgb(255, 255, 0)',
    'Y': 'rgb(180, 180, 0)',
    'g': 'rgb(0, 255, 0)',
    'G': 'rgb(109,252,49)',
    'c': 'rgb(0, 255, 255)',
    'C': 'rgb(0, 180, 180)',
    'b': 'rgb(0, 0, 255)',
    'B': 'rgb(0, 0, 139)',
    'v': 'rgb(153, 0, 204)',
    'V': 'rgb(115, 0, 153)',
}

const changeColor = (el, value) => el.style.background = COLORS[value]

var socket = io();
const step = () => socket.emit('game')
var stepInterval = 0

socket.on('field', function (field) {
    console.log('START TO DRAW FIELD', field)
    for (const i in field) for (const j in field) {
        const cell = document.getElementById(`cell (${i}, ${j})`);
        const value = field[i][j].toString();
        cell.removeAttribute('style')
        cell.className = 'cell';  // to clear cell
        changeColor(cell, value)
        if (value === 'A') cell.classList.add('apple');
    }
});

socket.on('personal data', function (color) {
    changeColor(document.getElementById('personal_color'), color);
    document.getElementById('personal_score').innerText = '0';
});

socket.on('personal score', function (score) {
    document.getElementById('personal_score').innerText = score;
});

socket.on('dead', function () {
    // Todo: you can not join started game in private room
    document.getElementById("game_start").classList.remove("off");
    document.getElementById("game_in_progress").className = "off";
});

socket.on('win', function () {
    clearInterval(stepInterval)
    alert('You are win! Congrats!')
})

socket.on('lose', function () {
    clearInterval(stepInterval)
    alert('Game over!')
})

document.addEventListener('keydown', function (e) {
    const progress = document.getElementById("game_in_progress");
    if (progress.classList.contains("off")) {
        const start = document.getElementById("game_start");
        if (e.code === 'KeyW') {
            socket.emit('start game')
            stepInterval = setInterval(step, 1000);
            start.className = "off";
            progress.classList.remove("off");
        }
    } else {
        if (e.code === 'KeyW') socket.emit('key', 'w');
        if (e.code === 'KeyA') socket.emit('key', 'a');
        if (e.code === 'KeyS') socket.emit('key', 's');
        if (e.code === 'KeyD') socket.emit('key', 'd');
    }
});
