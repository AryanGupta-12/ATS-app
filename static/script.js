document.addEventListener('DOMContentLoaded', () => {
    const resumeInput = document.getElementById('resume-input');
    const resumeList = document.getElementById('resume-list');
    const jdInput = document.getElementById('jd-input');
    const jdList = document.getElementById('jd-list');
    function updateFileList(input, list) {
        list.innerHTML = '';
        Array.from(input.files).forEach((file, index) => {
            const listItem = document.createElement('li');
            const fileName = document.createElement('span');
            fileName.textContent = file.name;
            const removeButton = document.createElement('button');
            removeButton.textContent = '×';
            removeButton.addEventListener('click', () => {
                const dt = new DataTransfer();
                const files = Array.from(input.files).filter((_, i) => i !== index);
                files.forEach(file => dt.items.add(file));
                input.files = dt.files;
                updateFileList(input, list);
            });
            listItem.appendChild(fileName);
            listItem.appendChild(removeButton);
            list.appendChild(listItem);
        });
    }

    resumeInput.addEventListener('change', () => updateFileList(resumeInput, resumeList));
    jdInput.addEventListener('change', () => updateFileList(jdInput, jdList));

    document.getElementById('resume-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/upload_resume', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            var modal = document.getElementById("resume-modal");
            var modalMessage = document.getElementById("resume-modalMessage");
            modalMessage.textContent = data.message;
            modal.style.display = "block";
            modal.querySelector(".close").onclick = function() {
                modal.style.display = "none";
            };
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            };
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    document.getElementById('jd-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/upload_jd', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            var modal = document.getElementById("jd-modal");
            var modalMessage = document.getElementById("jd-modalMessage");
            modalMessage.textContent = data.message;
            modal.style.display = "block";
            modal.querySelector(".close").onclick = function() {
                modal.style.display = "none";
            };
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            };
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    document.getElementById('process-button').addEventListener('click', function() {
        const output = document.getElementById('output');
        output.textContent = '';
        const startTime = Date.now();
        let waitingTime = 0;
        output.textContent = `Waiting time: ${waitingTime} seconds`;
        const intervalId = setInterval(() => {
            waitingTime = ((Date.now() - startTime) / 1000).toFixed(0); 
            output.textContent = `Waiting time: ${waitingTime} seconds`;
        }, 1000);
        fetch('/check_files',{
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Files are uploaded. Processing will start now.") {
                var modal = document.getElementById("process-modal");
                var modalMessage = document.getElementById("process-modalMessage");
                modalMessage.textContent = "Processing, please wait...";
                modal.style.display = "block";
                modal.querySelector(".close").onclick = function() {
                    modal.style.display = "none";
                };
                window.onclick = function(event) {
                    if (event.target == modal) {
                        modal.style.display = "none";
                    }
                };
                fetch('/process', {
                    method: 'POST'
                })
                .then(response => response.text())
                .then(text => {
                    clearInterval(intervalId);
                    output.textContent = text;
                    const finalWaitingTime = ((Date.now() - startTime) / 1000).toFixed(2); 
                    output.textContent += `\n\nTotal waiting time: ${finalWaitingTime} seconds`;

                })
                .catch(error => {
                    console.error('Error:', error);
                    modalMessage.textContent = "An error occurred during processing. Please try again.";
                    modal.querySelector(".close").onclick = function() {
                        modal.style.display = "none";
                    };
                    window.onclick = function(event) {
                        if (event.target == modal) {
                            modal.style.display = "none";
                        }
                    };
                });
            } else{
                var modal = document.getElementById("process-modal");
                var modalMessage = document.getElementById("process-modalMessage");
                modalMessage.textContent = data.message;
                modal.style.display = "block";
                modal.querySelector(".close").onclick = function() {
                    modal.style.display = "none";
                };
                window.onclick = function(event) {
                    if (event.target == modal) {
                        modal.style.display = "none";
                    }
                };
            }
        })
        .catch(error=>{
            console.error('Error:', error);
            alert("An error occurred while checking files.");
        });
    });
});