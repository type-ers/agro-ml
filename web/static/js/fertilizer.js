document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('fertilizerForm').addEventListener('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        fetch('/fertilizer', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.prediction) {
                document.getElementById('result').innerHTML = "The recommended fertilizer is<br><span>" + data.prediction + "</span>";
            } else {
                document.getElementById('result').innerHTML = "Error: Unable to get fertilizer recommendation.";
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
