const express = require("express");
const multer = require("multer");
const path = require("path");
const { spawn } = require("child_process");
const fs = require("fs");

const app = express();
const port = 3000;

// Serve static files
app.use(express.static(path.join(__dirname)));

// Configure multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "./");
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage: storage });
let lastUploadedFile = "";

// Handle file upload
app.post("/upload", upload.single("file"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }
  lastUploadedFile = req.file.originalname;
  res.status(200).send("File uploaded successfully.");
});

// Add a button to trigger processing
app.get("/process", (req, res) => {
  if (!lastUploadedFile) {
    return res.status(400).send("No file to process.");
  }

  const inputPath = path.join(__dirname, lastUploadedFile);
  const outputPath = path.join(__dirname, "processed_file.csv");

  const process = spawn("python", [
    "./python/compte_rezot.py",
    inputPath,
    outputPath,
  ]);

  process.stderr.on("data", (data) => {
    console.error(`Python STDERR: ${data}`);
  });

  process.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    if (code !== 0) {
      return res.status(500).send("Failed to process file.");
    }

    // Send the processed file as a download
    res.download(outputPath, path.basename(outputPath), (err) => {
      if (err) {
        console.log(`Error downloading file: ${err}`);
        res.status(500).send("Could not download the file.");
      } else {
        // Delete the uploaded and processed files
        fs.unlinkSync(inputPath);
        fs.unlinkSync(outputPath);
        lastUploadedFile = ""; // Reset the lastUploadedFile variable
      }
    });
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
