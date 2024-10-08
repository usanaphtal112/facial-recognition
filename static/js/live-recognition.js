document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const resultsList = document.getElementById('resultsList');
    const context = canvas.getContext('2d');
    let streaming = false;
    let mediaStream = null;

    // Start video streaming
    startBtn.addEventListener('click', function() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                mediaStream = stream;
                video.srcObject = stream;
                video.play();
                streaming = true;
                startBtn.style.display = 'none';
                stopBtn.style.display = 'block';
                processVideo();
            })
            .catch(function(err) {
                console.error("An error occurred: " + err);
                addAlert("Error accessing camera. Please ensure you've granted camera permissions.");
            });
    });

    // Stop video streaming
    stopBtn.addEventListener('click', function() {
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
        }
        streaming = false;
        video.srcObject = null;
        startBtn.style.display = 'block';
        stopBtn.style.display = 'none';
    });

    function processVideo() {
        if (!streaming) return;

        // Set canvas dimensions to match video
        if (video.videoWidth) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
        }

        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert canvas to blob and send to server
        canvas.toBlob(function(blob) {
            const formData = new FormData();
            formData.append('frame', blob);
            
            fetch('/detection/process-frame/', {  // Adjusted endpoint for your Django view
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                updateResults(data);
                drawBoxes(data.faces);
                if (streaming) {
                    requestAnimationFrame(processVideo);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                addAlert("Error processing video frame.");
            });
        }, 'image/jpeg');
    }

    function updateResults(data) {
        resultsList.innerHTML = '';
        const facesCount = data.faces.length;
        const resultItem = document.createElement('div');
        resultItem.className = 'list-group-item';
        resultItem.innerHTML = `Faces Detected: ${facesCount}`;
        resultsList.appendChild(resultItem);
    }

    function drawBoxes(faces) {
        context.clearRect(0, 0, canvas.width, canvas.height); // Clear previous drawings
        context.drawImage(video, 0, 0, canvas.width, canvas.height); // Redraw video

        faces.forEach(face => {
            context.beginPath();
            context.rect(face.x, face.y, face.width, face.height);
            context.strokeStyle = '#00ff00';
            context.lineWidth = 2;
            context.stroke();

            context.fillStyle = 'rgba(0, 0, 0, 0.5)';
            context.fillRect(face.x, face.y - 25, face.width, 25);
            
            context.fillStyle = '#ffffff';
            context.font = '16px Arial';
            context.fillText(`Face`, face.x + 5, face.y - 5);
        });
    }

    function addAlert(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.card-body').insertBefore(alertDiv, video);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
