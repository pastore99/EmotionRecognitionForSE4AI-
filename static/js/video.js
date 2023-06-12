const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const constraints = {
    audio: true;
    video: {
        width: 1280, height: 720
    }
};
const url = 'http:localhost:5000/preprocess';
const intervalID;

async function init() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream);

        intervalID = setInterval(estrapolaImmagine, 20000);
    } catch (e) {
        console.log(e.toString())
    }
}

function handleSuccess(stream) {
    window.stream = stream;
    video.srcObject = stream;
}

init();

var context = canvas.getContext('2d');
startBtn.addEventListener("click", function() {
    context.drawImage(video, 0, 0, 640, 480);
})


stopBtn.addEventListener('click', function () {
  mediaRecorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
  clearInterval(intervalID);
});


function estrapolaImmagine() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Disegna il frame corrente del video sul canvas
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Ottieni l'URL dell'immagine dal canvas
    const imageURL = canvas.toDataURL();
    fetch(url, {
        method: 'POST',
        headers: {
            'Cotnent-type': 'application/json'
        },
        body: {
            'Image': imageURL
        }
    })
    .then(response => response.json())
    .then(data => {console.log(data)})
    ,catch(error => {console.error('Errore: ', error)})
}

