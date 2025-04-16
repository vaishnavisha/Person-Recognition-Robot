const webcamElement = document.getElementById('webcam');
const resultSection = document.getElementById('result');
const captureBtn = document.getElementById("captureButton");
const canvasOverlay = document.createElement('canvas');
const ctx = canvasOverlay.getContext('2d');
resultSection.style.display = "block";

// Append canvas overlay on top of video
webcamElement.parentElement.appendChild(canvasOverlay);

// Adjust canvas size to match the video element
function adjustCanvasSize() {
    canvasOverlay.width = webcamElement.videoWidth;
    canvasOverlay.height = webcamElement.videoHeight;
    canvasOverlay.style.position = 'absolute';
    canvasOverlay.style.top = `${webcamElement.offsetTop}px`;
    canvasOverlay.style.left = `${webcamElement.offsetLeft}px`;
    canvasOverlay.style.pointerEvents = 'none'; // Ensures it doesn't block interaction with the video
}

function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
}

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        webcamElement.srcObject = stream;
        webcamElement.addEventListener('loadeddata', adjustCanvasSize);
    })
    .catch(error => {
        console.error("Error accessing webcam: ", error);
    });

// Function to capture and send frame
function sendFrameForVerification() {
    const canvas = document.createElement('canvas');
    canvas.width = webcamElement.videoWidth;
    canvas.height = webcamElement.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(webcamElement, 0, 0, canvas.width, canvas.height);

    const base64Image = canvas.toDataURL('image/jpeg');
    fetch('http://localhost:5000/identify-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Image }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const user = data.user;
                html = `
                        Role: ${user.role} <br>
                        Name: ${user.name} <br>
                    `;

                if (user.role === "student") {
                    html += `
                            Date Of Birth: ${user.dob} <br>
                            USN: ${user.usn} <br>
                            CGPA: ${user.cgpa}
                        `;
                } else if (user.role === "staff") {
                    html += `
                            Department: ${user.department} <br>
                            Designation: ${user.designation}
                        `;
                }

                resultSection.innerHTML = html;
                drawOverlay(user.name);
                speak(`User Identified: ${user.role}`);
                speak(`Name: ${user.name}`);
                if (user.role === "student") {
                    speak(`Date Of Birth: ${user.dob}`);
                    speak(`USN: ${user.usn}`);
                    speak(`CGPA: ${user.cgpa}`);
                } else if (user.role === "staff") {
                    speak(`Department: ${user.department}`)
                    speak(`Designation: ${user.designation}`)
                }
            } else {
                window.speechSynthesis.cancel();
                resultSection.innerHTML = "No matching user found.";
                speak("No matching user found");
                clearOverlay();
            }
        })
        .catch(error => {
            window.speechSynthesis.cancel();
            resultSection.innerHTML = "Something went wrong!!!"
            speak("Something went wrong!!!")
            console.error('Error:', error)
        });
}

// Function to draw name overlay directly on the video
function drawOverlay(name) {
    ctx.clearRect(0, 0, canvasOverlay.width, canvasOverlay.height);
    ctx.font = '20px Arial';
    ctx.fillStyle = 'red';
    ctx.fillText(name, 10, 30); // Position the name at the top-left corner of the video
}

// Function to clear overlay
function clearOverlay() {
    ctx.clearRect(0, 0, canvasOverlay.width, canvasOverlay.height);
}

captureBtn.addEventListener("click", sendFrameForVerification);