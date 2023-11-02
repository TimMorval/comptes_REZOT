const express = require("express");
const multer = require("multer");
const path = require("path");
const { spawn } = require("child_process");
const fs = require("fs");

const app = express();
const port = 3000;

// Serve static files
app.use(express.static(path.join(__dirname, "public")));
app.get("/", (req, res) =>
  res.sendFile(path.join(__dirname, "views/index.html"))
);

// Configure multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/"); // Use an 'uploads' folder
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + "-" + file.originalname); // Prefix with a timestamp to avoid overwriting
  },
});

const upload = multer({ storage: storage });

// Handle file upload and processing
app.post("/upload", upload.single("file"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }

  // File path for both input and output
  const inputPath = path.join(__dirname, req.file.path);
  const outputPath = path.join(
    __dirname,
    "uploads/processed_" + req.file.originalname
  );

  // Spawn the Python process
  const process = spawn("python", [
    "./python/compte_rezot.py",
    inputPath,
    outputPath,
  ]);

  process.stderr.on("data", (data) => {
    console.error(`Python STDERR: ${data}`);
  });

  process.on("close", (code) => {
    if (code !== 0) {
      fs.unlinkSync(inputPath); // Clean up uploaded file
      return res.status(500).send("Failed to process file.");
    }

    // Send the processed file as a download
    res.download(outputPath, (err) => {
      if (err) {
        console.error(`Error downloading file: ${err}`);
      }

      // Clean up files after sending
      fs.unlinkSync(inputPath);
      fs.unlinkSync(outputPath);
    });
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
