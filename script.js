document.addEventListener("DOMContentLoaded", function () {
  const dropZone = document.getElementById("drop-zone");
  const fileList = document.getElementById("file-list");
  const processButton = document.getElementById("process-button");
  const cancelButton = document.getElementById("cancel-button");

  // Function to clear the file list
  function clearFileList() {
    fileList.innerHTML = "";
  }

  dropZone.addEventListener("dragover", function (event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  });

  dropZone.addEventListener("drop", function (event) {
    event.preventDefault();
    clearFileList(); // Clear previous status

    const files = event.dataTransfer.files;
    if (files.length > 1) {
      alert("Please drop only one file at a time.");
      return;
    }

    const file = files[0];
    const formData = new FormData();
    formData.append("file", file);

    // Use XMLHttpRequest to upload the file
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        fileList.innerHTML = `File uploaded successfully: ${file.name}`;
        processButton.removeAttribute("disabled");
        cancelButton.removeAttribute("disabled");
      }
    };
    xhr.send(formData);
  });

  processButton.addEventListener("click", function () {
    fetch("/process")
      .then((response) => response.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        a.download = "processed_file.xlsx"; // You can name this whatever you want
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      });
  });

  cancelButton.addEventListener("click", function () {
    clearFileList(); // Clear the file list
    processButton.setAttribute("disabled", true);
    cancelButton.setAttribute("disabled", true);
    // You can also add code here to cancel the upload on the server if needed.
  });
});
