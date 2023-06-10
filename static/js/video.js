var video = document.getElementById('video');
var startBtn = document.getElementById('startBtn');
var stopBtn = document.getElementById('stopBtn');
var stream;
var mediaRecorder;
var chunks = [];
const intervalID;

navigator.mediaDevices.getUserMedia({ video: true })
.then(function (stream) {
video.srcObject = stream;
mediaRecorder = new MediaRecorder(stream);

startBtn.addEventListener('click', function () {
  mediaRecorder.start();
  startBtn.disabled = true;
  stopBtn.disabled = false;
  intervalID = setInterval(estrapolaImmagine, 20000);
});

stopBtn.addEventListener('click', function () {
  mediaRecorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
  clearInterval(intervalID);
});

mediaRecorder.ondataavailable = function (e) {
  chunks.push(e.data);
};

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
    const imageURL = canvas.toDataURL('image/png');

    // Crea un link per il download dell'immagine
    const downloadLink = document.createElement('a');
    downloadLink.href = imageURL;
    downloadLink.download = 'immagine.png';
    downloadLink.click();
}

