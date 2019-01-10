navigator.getUserMedia = ( navigator.getUserMedia ||
navigator.webkitGetUserMedia ||
navigator.mozGetUserMedia ||
navigator.msGetUserMedia);

navigator.vibrate = navigator.vibrate || navigator.webkitVibrate || navigator.mozVibrate || navigator.msVibrate;
if (navigator.vibrate) {
	console.log('Vibration Supported');
}
var video;
var webcamStream;
var videoDeviceSelected;
var screenShotImage;
var socket = io.connect('http://beb27026.ngrok.io');
//var socket = io.connect('http://bellchen.me:26854');
//constantly send pictures back
setInterval(function() {
	sendimageback();
  }, 5000);
function sendimageback(){
	console.log('imageprocess');
	snapshot();
	socket.emit('imageprocessing',screenShotImage);
}
function speak(text, callback) {
	var u = new SpeechSynthesisUtterance();
	u.text = text;
	u.lang = 'en-US';
	u.onend = function () {
		if (callback) {
			callback();
		}
	};
	u.onerror = function (e) {
		if (callback) {
			callback(e);
		}
	};
	speechSynthesis.speak(u);
}
function getDevices(deviceInfos){
    var allVideoDevices=[]
    for (var i = 0; i !== deviceInfos.length; ++i) {
        var deviceInfo = deviceInfos[i];
        var option = document.createElement('option');
        option.value = deviceInfo.deviceId;
        if (deviceInfo.kind === 'videoinput') {
        option.text = deviceInfo;
        allVideoDevices.push(option);
        break;
        } else {
        console.log('Non video device: ', deviceInfo);
        }
    }
    if (allVideoDevices.length>=1){
        videoDeviceSelected=allVideoDevices[0];
    }
}
function startWebcam() {
if (navigator.getUserMedia) {
navigator.mediaDevices.enumerateDevices().then(getDevices)
navigator.getUserMedia (

// constraints
{
video: {
deviceId: {exact: videoDeviceSelected}
},
audio: false
},

// successCallback
function(localMediaStream) {
video = document.querySelector('video');
video.src = window.URL.createObjectURL(localMediaStream);
webcamStream = localMediaStream;
},

// errorCallback
function(err) {
console.log("The following error occured: " + err);
}
);
} else {
console.log("getUserMedia not supported");
}  
}

function stopWebcam() {
webcamStream.stop();
}
//---------------------
// TAKE A SNAPSHOT CODE
//---------------------
var canvas, ctx;

function init() {
// Get the canvas and obtain a context for
// drawing in it
	canvas = document.getElementById("myCanvas");
	ctx = canvas.getContext('2d');
	speak('Please make sure the rear camera on your cell phone is facing forward.')
}

// function snapshot() {
//    // Draws current image from the video element into the canvas
//   ctx.drawImage(video, 0,0, canvas.width, canvas.height);
// }
function snapshot(){
var hidden_canvas = document.querySelector('canvas');
image = document.querySelector('img.photo');

// Get the exact size of the video element.
width = video.videoWidth;
height = video.videoHeight;

// Context object for working with the canvas.
context = hidden_canvas.getContext('2d');
// Set the canvas to the same dimensions as the video.
hidden_canvas.width = width;
hidden_canvas.height = height;

// Draw a copy of the current frame from the video on the canvas.
context.drawImage(video, 0, 0, width, height);

// Get an image dataURL from the canvas.
var imageDataURL = hidden_canvas.toDataURL('image/png');
screenShotImage=imageDataURL;
console.log(imageDataURL);
// Set the dataURL as source of an image element, showing the captured photo.
}

$(document).ready(function() {
    //var socket = io.connect('http://127.0.0.1:5000');
    //var socket = io.connect('http://bellchen.me:26854');

	socket.on('connect', function() {
		//socket.send('User has connected!');
	});

	socket.on('message', function (msg) {
		console.log('Received message',msg);
	});
	socket.on('playsound',function (msg) {
		console.log('Received message',msg);
		speak(msg);
	});
	socket.on('vibrate',function(msg){
		switch(msg){
			case '0':
				navigator.vibrate(50);
			case '1':
				navigator.vibrate(100);
			case '2':
				navigator.vibrate(200);
			case '3':
			navigator.vibrate([300,200,300,200]);
			case '4':
			navigator.vibrate([500,200,500,200]);
			case '5':
			navigator.vibrate([200, 100, 200, 100, 200, 100, 200, 100]);
			case '6':
			navigator.vibrate([100,60,100,60,100,60,100,60,100,60,100,60,100,60,100]);
			default:
				console.log('No vib length')
		}
	})
	$('#describebutton').on('click', function () {
		console.log('Describe');
		snapshot();
		socket.emit('describe',screenShotImage);
	});
	
	// socket.on('describe', function (msg) {
	// 	console.log('Received message',msg);
	// });

	socket.on('my response', function (msg) {
		console.log('Received message',msg);
	});

	$('#sendbutton').on('click', function() {
		console.log(screenShotImage)
		socket.send(screenShotImage);
	});

    /*
	$('#clearBtn').on('click', function () {
	    $('#messages').val('');
	});
    */

});