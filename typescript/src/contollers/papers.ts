import { Request, Response } from "express";
import multer from "multer";
import axios from "axios";
import fs from "fs";
import path from "path";
import FormData from "form-data"; 

// Configure Multer for file uploads
const upload = multer({ dest: "uploads/" });

// Extend Request to include file property
interface MulterRequest extends Request {
    file?: Express.Multer.File;
}

export const qPaperUpload = async (req: MulterRequest, res: Response): Promise<void> => {
    console.log("Received file:", req.file);
    try {
        if (!req.file) {
            res.status(400).json({ message: "No file uploaded" });
            return;
        }

        // Validate file type
        const fileExtension = path.extname(req.file.originalname).toLowerCase();
        if (fileExtension !== ".pdf") {
            fs.unlinkSync(req.file.path); // Delete non-PDF file
            res.status(400).json({ message: "Only PDF files are allowed" });
            return;
        }

        const filePath = path.resolve(req.file.path);

        // Prepare FormData to send file to Python backend
        const formData = new FormData();
        formData.append("pdf", fs.createReadStream(filePath));

        // Send file to Python backend
        const response = await axios.post("http://localhost:5000/analyze", formData, {
            headers: {
                ...formData.getHeaders(), // Set correct headers for multipart/form-data
            },
        });

        // Delete the uploaded file after sending
        fs.unlinkSync(filePath);

        // Send Python's response back to the frontend
        res.json(response.data);
        
        console.log("Response from Python backend:", response.data);
    } catch (error) {
        console.error("Error sending file to Python backend:", error);
        res.status(500).json({ message: "Error processing file" });
    }
};
    