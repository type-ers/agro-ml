document.getElementById('diseaseForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/disease', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = "The disease is<br><span>" + data.prediction + "</span>";
    })
    .catch(error => {
        console.error('Error:', error);
    });
});