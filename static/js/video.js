const video = document.getElementById('videoElement');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
var intervalID;
// Opzioni per l'acquisizione video
const constraints = { video: true };

// Funzione per avviare l'acquisizione video
function startVideo() {
  navigator.mediaDevices.getUserMedia(constraints)
    .then((stream) => {
      document.getElementById('videoElement').srcObject = stream;
    })
    .catch((error) => {
      console.error('Errore nell\'acquisizione video:', error);
    });
    document.getElementById('startButton').classList.add('d-none');
    document.getElementById('stopButton').classList.remove('d-none');
    intervalID = setInterval(takeSnapshot, 20000/4);
}

function takeSnapshot() {
  const canvas = document.createElement('canvas');
  canvas.width = document.getElementById('videoElement').videoWidth;
  canvas.height = document.getElementById('videoElement').videoHeight;

  const context = canvas.getContext('2d');
  context.drawImage(document.getElementById('videoElement'), 0, 0, canvas.width, canvas.height);

  var imageDataURL = canvas.toDataURL()
  //Inserire l'url del servizio
  const url = 'http://127.0.0.1:5001/predict';
   const data = {
    image: imageDataURL
  };
  fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
         },
        body: JSON.stringify(data)

    })
    .then(response => response.json())
    .then(data => {console.log(data)})
    .catch(error => {console.error('Errore: ', error.toString())})

    console.log('foto inviata, bye bye')
}

function stopVideo() {
    clearInterval(intervalID);
    document.getElementById('startButton').classList.remove('d-none');
    document.getElementById('stopButton').classList.add('d-none');
}