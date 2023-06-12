const webCamElement = document.getElementById("webCam");
const canvasElement = document.getElementById("canvas");
const webCam = new Webcam(webCamElement, "user", canvasElement);
webcam.start();

function takePicture() {
    let picture = webcam.snap();
    document.querySelector("a").href = picture;
}

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

