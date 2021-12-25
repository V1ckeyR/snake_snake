function changeColor(el, value) {
    switch (value) {
        case 'R': el.style.backgroundColor = "darkred"; break;
        case 'r': el.style.backgroundColor = "red"; break;
        case 'B': el.style.backgroundColor = "darkblue"; break;
        case 'b': el.style.backgroundColor = "blue"; break;
    }
}

var socket = io();
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

socket.on('personal color', function (color) {
    changeColor(document.getElementById('personal_color'), color)
})

document.addEventListener('keydown', function (e) {
    const progress = document.getElementById("game_in_progress");
    if (progress.classList.contains("off")) {
        const start = document.getElementById("game_start");
        if (e.code === 'KeyW') {
            socket.emit('start game')
            start.className = "off";
            progress.classList.remove("off");
        }
    } else {
        if (e.code === 'KeyW') socket.emit('game', 'w');
        if (e.code === 'KeyA') socket.emit('game', 'a');
        if (e.code === 'KeyS') socket.emit('game', 's');
        if (e.code === 'KeyD') socket.emit('game', 'd');
    }
});
