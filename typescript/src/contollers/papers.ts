import { Request, Response } from "express";
import multer from "multer";
import axios from "axios";
import fs from "fs";
import path from "path";
import FormData from "form-data"; // Import FormData

// Configure Multer for file uploads
const upload = multer({ dest: "uploads/" });

// Extend Request to include file property
interface MulterRequest extends Request {
    file?: Express.Multer.File;
}

export const qPaperUpload = async (req: MulterRequest, res: Response): Promise<void> => {
    try {
        if (!req.file) {
            res.status(400).json({ message: "No file uploaded" });
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
    } catch (error) {
        console.error("Error sending file to Python backend:", error);
        res.status(500).json({ message: "Error processing file" });
    }
};
    