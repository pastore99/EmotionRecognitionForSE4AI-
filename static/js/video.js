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
    intervalID = setInterval(takeSnapshot(0), 20000/4);
}

function takeSnapshot(stato) {

  const canvas = document.createElement('canvas');
  canvas.width = document.getElementById('videoElement').videoWidth;
  canvas.height = document.getElementById('videoElement').videoHeight;

  const context = canvas.getContext('2d');
  context.drawImage(document.getElementById('videoElement'), 0, 0, canvas.width, canvas.height);

  var imageDataURL = canvas.toDataURL()
  //Inserire l'url del servizio
  const url = 'http://127.0.0.1:5001/predict';
   const data = {
    image: imageDataURL,
       status: stato
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
    takeSnapshot(1)
    document.getElementById('startButton').classList.remove('d-none');
    document.getElementById('stopButton').classList.add('d-none');
}

function richiediDati(){
    var data = document.getElementById('inputData').value;
    data = data.replaceAll("-", "_")
    console.log(data)
     const url = 'http://127.0.0.1:5001/fileSpecifico';
     var options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ report: data }),
  };

     fetch(url, options).then(function (response){
         if(response.ok){
             return response.json();
         }else {
             throw new Error('Errore nella richiesta');
         }
     }).then(function (data) {
         console.log(data);
         creaGrafico(data);
    })
    .catch(function (error) {
      console.log(error);
    });


}

function richiediDatiGenerale(){
    var data = document.getElementById('inputData').value;
    data = data.replaceAll("-", "_")
    console.log(data)
     const url = 'http://127.0.0.1:5001/fileGenerale';
     var options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ report: data }),
  };

     fetch(url, options).then(function (response){
         if(response.ok){
             return response.json();
         }else {
             throw new Error('Errore nella richiesta');
         }
     }).then(function (data) {
         console.log(data);
         creaGraficoGenerale(data);
    })
    .catch(function (error) {
      console.log(error);
    });


}

function creaGrafico(data) {
  var chartData = [['Orario', 'Alunno 1']];

  data.forEach(function (element) {
      if (element.hasOwnProperty('surprise')) {
           try {
               var dataString = element.surprise;
               console.log(dataString);
               var parts = dataString.split(":");
               var ore = parseInt(parts[0], 10);
               var minuti = parseInt(parts[1], 10);
               var secondi = parseInt(parts[2], 10);
               var date = new Date();
               date.setHours(ore, minuti, secondi);
               var orario = date; // Primo elemento come valore sull'asse x
               var dato = 1; // Secondo elemento come valore sull'asse y
               chartData.push([orario, dato]);
           } catch (e) {
               console.log(e)
           }
      } else if (element.hasOwnProperty('happy')) {
           try {
               var dataString = element.happy;
               console.log(dataString);
               var parts = dataString.split(":");
               var ore = parseInt(parts[0], 10);
               var minuti = parseInt(parts[1], 10);
               var secondi = parseInt(parts[2], 10);
               var date = new Date();
               date.setHours(ore, minuti, secondi);
               var orario = date; // Primo elemento come valore sull'asse x
               var dato = 2; // Secondo elemento come valore sull'asse y
               chartData.push([orario, dato]);
           } catch (e) {
               console.log(e)
           }
      } else if (element.hasOwnProperty('sad')) {
           try {
               var dataString = element.sad;
               console.log(dataString);
               var parts = dataString.split(":");
               var ore = parseInt(parts[0], 10);
               var minuti = parseInt(parts[1], 10);
               var secondi = parseInt(parts[2], 10);
               var date = new Date();
               date.setHours(ore, minuti, secondi);
               var orario = date; // Primo elemento come valore sull'asse x
               var dato = 3; // Secondo elemento come valore sull'asse y
               chartData.push([orario, dato]);
           } catch (e) {
               console.log(e)
           }
      } else if (element.hasOwnProperty('neutral')) {
          try {
              var dataString = element.neutral;
              console.log(dataString);
              var parts = dataString.split(":");
              var ore = parseInt(parts[0], 10);
              var minuti = parseInt(parts[1], 10);
              var secondi = parseInt(parts[2], 10);
              var date = new Date();
              date.setHours(ore, minuti, secondi);
              var orario = date; // Primo elemento come valore sull'asse x
              var dato = 4; // Secondo elemento come valore sull'asse y
              chartData.push([orario, dato]);
          } catch (e) {
              console.log(e)
          }
      } else if (element.hasOwnProperty('fear')) {
          try {
              var dataString = element.fear;
              console.log(dataString);
              var parts = dataString.split(":");
              var ore = parseInt(parts[0], 10);
              var minuti = parseInt(parts[1], 10);
              var secondi = parseInt(parts[2], 10);
              var date = new Date();
              date.setHours(ore, minuti, secondi);
              var orario = date; // Primo elemento come valore sull'asse x
              var dato = 5; // Secondo elemento come valore sull'asse y
              chartData.push([orario, dato]);
          } catch (e) {
              console.log(e)
          }
      } else if (element.hasOwnProperty('disgust')) {
          try {
              var dataString = element.disgust;
              console.log(dataString);
              var parts = dataString.split(":");
              var ore = parseInt(parts[0], 10);
              var minuti = parseInt(parts[1], 10);
              var secondi = parseInt(parts[2], 10);
              var date = new Date();
              date.setHours(ore, minuti, secondi);
              var orario = date; // Primo elemento come valore sull'asse x
              var dato = 6; // Secondo elemento come valore sull'asse y
              chartData.push([orario, dato]);
          } catch (e) {
              console.log(e)
          }
      } else if (element.hasOwnProperty('angry')) {
          try {
              var dataString = element.angry;
              console.log(dataString);
              var parts = dataString.split(":");
              var ore = parseInt(parts[0], 10);
              var minuti = parseInt(parts[1], 10);
              var secondi = parseInt(parts[2], 10);
              date.setHours(ore, minuti, secondi);
              var orario = date; // Primo elemento come valore sull'asse x
              var dato = 7; // Secondo elemento come valore sull'asse y
              chartData.push([orario, dato]);
          } catch (e) {
              console.log(e)
          }
      }
  });

  var emozioni = ["Sorpreso", "Felice", "Triste", "Neutrale", "Spaventato", "Disgustato", "Arrabbiato"];

  // Carica la libreria Google Charts
  google.charts.load('current', { packages: ['corechart'] });
  google.charts.setOnLoadCallback(function() {
    // Crea e disegna il grafico
    var data = google.visualization.arrayToDataTable(chartData);
    var options = {
      title: 'Andamento emozione alunno durante lezione',
      hAxis: { title: 'Orario',
      format: 'HH:mm:ss'},
      vAxis: { title: 'Emozione' ,
        ticks: [
      {v: 1, f: 'Sorpreso'},
      {v: 2, f: 'Felice'},
      {v: 3, f: 'Triste'},
      {v: 4, f: 'Neutrale'},
      {v: 5, f: 'Spaventato'},
      {v: 6, f: 'Disgustato'},
      {v: 7, f: 'Arrabbiato'}
    ]},
      width: 1200,
      height: 400,

    };
    var chart = new google.visualization.LineChart(document.getElementById('chartContainer'));

    chart.draw(data, options);
  });
}

function creaGraficoGenerale(jsonData) {
  // Converte l'oggetto JSON in un array di coppie chiave-valore
  var data = Object.entries(jsonData);

  // Crea un array di array per i dati del grafico
  var chartData = [['Chiave', 'Valore']];

  // Aggiunge ogni coppia chiave-valore all'array dei dati del grafico
  data.forEach(function (item) {
    chartData.push(item);
  });

  // Carica la libreria Google Charts
  google.charts.load('current', { packages: ['corechart'] });

  // Chiamata di callback una volta che la libreria è stata caricata
  google.charts.setOnLoadCallback(drawChart);

  // Funzione per disegnare il grafico
  function drawChart() {
    // Crea un'istanza del grafico a colonne
    var chart = new google.visualization.ColumnChart(document.getElementById('chartContainer'));

    // Crea un oggetto DataTable e imposta i dati del grafico
    var dataTable = google.visualization.arrayToDataTable(chartData);

    // Opzioni del grafico
    var options = {
      title: 'Grafico Generale',
      width: 1200,
      height: 300
    };

    // Disegna il grafico utilizzando i dati e le opzioni specificate
    chart.draw(dataTable, options);
  }
}

