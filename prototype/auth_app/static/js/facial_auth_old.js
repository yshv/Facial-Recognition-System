function initialize() {
    if (typeof cv === 'undefined') {
        setTimeout(initialize, 50);
        return;
    }
    console.log('OpenCV ready');
}

let video = document.getElementById("video");
let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let startButton = document.getElementById("startButton");
let stopButton = document.getElementById("stopButton");

function initCamera() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
                video.play();
            });
    }
}

function startProcessing() {
    initCamera();
    startButton.disabled = true;
    stopButton.disabled = false;
    processVideo();
}

function stopProcessing() {
    startButton.disabled = false;
    stopButton.disabled = true;

    // Stop the camera stream
    if (video.srcObject) {
        let tracks = video.srcObject.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
    }
}


function processVideo() {
    if (stopButton.disabled) {
      return;
    }
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  
    // Process the video frame here using OpenCV functions.
    // For example, detect faces, extract facial features, and perform authentication.
    const facialData = {}; // Replace with actual facial data
  
    submitFacialData(facialData);
  
    setTimeout(processVideo, 1000 / 30); // Call this function again after a delay (e.g., 30 FPS).
  }
  

startButton.addEventListener("click", startProcessing);
stopButton.addEventListener("click", stopProcessing);



function submitFacialData(facialData) {
const loginForm = document.getElementById("loginForm");
const facialDataInput = document.getElementById("facialDataInput");
facialDataInput.value = JSON.stringify(facialData);

if (loginForm) {
    loginForm.submit();
} else {
    const facialAuthForm = document.getElementById("facialAuthForm");
    facialAuthForm.submit();
}
}
  
  



const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const username = urlParams.get('username');
