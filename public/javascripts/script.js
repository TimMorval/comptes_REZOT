document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("file-input");
  const processButton = document.getElementById("process-button");
  const cancelButton = document.getElementById("cancel-button");

  // Enable or disable buttons based on file input
  fileInput.addEventListener("change", function () {
    if (this.files.length > 0) {
      processButton.disabled = false;
      cancelButton.disabled = false;
    } else {
      processButton.disabled = true;
      cancelButton.disabled = true;
    }
  });

  // Process button event
  processButton.addEventListener("click", function () {
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    // Send the file to the server
    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.blob();
      })
      .then((blob) => {
        // Create a link to download the processed file
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        a.download = "processed_file.csv"; // Update with actual file name if needed
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    // Reset the UI
    fileInput.value = ""; // Clear the file input
    processButton.disabled = true; // Disable the process button
    cancelButton.disabled = true; // Disable the cancel button
  });

  // Cancel button event
  cancelButton.addEventListener("click", function () {
    fileInput.value = ""; // Clear the file input
    processButton.disabled = true; // Disable the process button
    cancelButton.disabled = true; // Disable the cancel button
  });
});
