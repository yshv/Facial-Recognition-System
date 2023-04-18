// JavaScript
let video = document.getElementById('video');
let canvas = document.getElementById('overlay');
let startBtn = document.getElementById('startButton');
let snapBtn = document.getElementById('captureButton');
let imageInput = document.getElementById('facialDataInput');
let captureCount = document.getElementById('captureCount');
let username = document.getElementById('username');
let ctx = canvas.getContext('2d');
let count = 0;
let maxCount = 5;
let photoUrls = [];
let isCameraOn = false;



function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        video.srcObject = stream;
        video.onplay();
        isCameraOn = true;
        console.log('Camera initialized');
    })
    .catch(function(error) {
        console.log('Error accessing camera:', error);
    });
}

function stopCamera() {
    let stream = video.srcObject;
    let tracks = stream.getTracks();
    tracks.forEach(function(track) {
        track.stop();
    });
    video.srcObject = null;
}

function savePhotos(photoUrls) {
    // Send the photoUrls to the server using AJAX
    console.log('5 photos collected')
    console.log(photoUrls);
}


console.log('Camera initialized')
startBtn.addEventListener('click', function() {
    console.log(isCameraOn)
    if (isCameraOn) {
        stopCamera();
        isCameraOn = false;
        startBtn.innerHTML = 'Start Camera';
    } else {
        startCamera();
        isCameraOn = true;
        startBtn.innerHTML = 'Stop Camera';
    }
});

snapBtn.addEventListener('click', function() {
    if (!isCameraOn) {
        alert('Please start the camera first');
        return;
    }
    else{
         console.log('Taking photo', count+1)
        captureCount.textContent = (count + 1).toString();
        if (count < maxCount) {
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            let photoUrl = canvas.toDataURL('image/jpeg');
            photoUrls.push(photoUrl);
            // console.log(photoUrl);
            // console.log(photoUrls);
            count++;
        }
        if (count === maxCount) {
            // Save the photos to the server using AJAX
            console.log(photoUrls.length)
            const facialData = { 
                username : username.value,
                images: photoUrls,
            }; 
            imageInput.value = JSON.stringify(facialData);
            // imageInput.value = photoUrls;
            console.log('5 photos collected')
            console.log(imageInput.value)
        }
    }
   
});



