const video = document.getElementById('video');
const startBtn = document.getElementById('startBtn');
const canvas = document.getElementById('canvas');
const constraints = {
    audio: true
    video: {
        width: 1280, height: 720
    }
};
const url = 'http:localhost:5000/preprocess';
var intervalID;

async function init() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream);
    } catch(e) {
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
    startBtn.disabled = true;
    stopBtn.disabled = false;
    intervalID = setInterval(estrapolaImmagine, 20000);
})

stopBtn.addEventListener('click', function () {
  mediaRecorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
  clearInterval(intervalID);
});

mediaRecorder.onstop = function () {
  var blob = new Blob(chunks, { type: 'video/webm' });
  chunks = [];

  var videoURL = URL.createObjectURL(blob);
  var downloadLink = document.createElement('a');
  downloadLink.href = videoURL;
  downloadLink.setAttribute('download', 'registrato.webm');
  downloadLink.innerHTML = 'Download del video registrato';
  document.body.appendChild(downloadLink);
};
})
.catch(function (error) {
    console.error('Errore durante l\'accesso alla webcam:', error);
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

