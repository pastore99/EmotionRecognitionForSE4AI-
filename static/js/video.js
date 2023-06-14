const video = document.getElementById('videoElement');
const startButton = document.getElementById('startButton');

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
}

function takeSnapshot() {
  const canvas = document.createElement('canvas');
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;

  const context = canvas.getContext('2d');
  context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

  const imageDataURL = canvas.toDataURL('image/png');
  //Inserire l'url del servizio
  const url = '';
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
    .catch(error => {console.error('Errore: ', error.toString())})
}