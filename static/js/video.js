$(document).ready(function(){
    var webCamElement = document.getElementById("camera");
    var canvasElement = document.getElementById("canvas");
    const webcam = new Webcam(webCamElement, 'user', canvasElement, null);

    //$('#camera').style.display="none";
    //$('#camera').attr('visibility', 'hidden');
    //$('#camera').attr('display', 'block');

    $('#camera').css('visibility', 'hidden');

    webcam.start();

     $('#checker').click(function(){
        picture = webcam.snap();
        alert(picture);
        $.post('TestCamera', {param: picture}, function(response){
            if (response === 'error'){
                alert('Error you should stay in front of camera');
            }else{
                window.location.replace('QuestionAndAnalyze.jsp'); /* redirect*/
            }
        }); /*END servletCall*/
    }); /*END click*/

});/* END ready*/

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

app.onloaded = function () {
	btnTakePicture.addEventListener("click", takePicture_click);
}
function takePicture_click(args) {
	var captureUI = new Windows.Media.Capture.CameraCaptureUI();
	captureUI.captureFileAsync(Windows.Media.Capture.CameraCaptureUIMode.photo)
		.done(function (capturedItem) {
			if (capturedItem) {
				photoMessage.innerHTML = "Immagine catturata.";
			}
			else {
				photoMessage.innerHTML = "Operazione cancellata dall'utente."
			}
		}, function (err) {
			photoMessage.innerHTML = "Qualcosa è andato storto.";
		});
}

