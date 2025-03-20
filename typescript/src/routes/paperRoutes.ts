import { Router } from "express";
import { qPaperUpload } from "../contollers/papers";
import multer from "multer";

const router = Router();
const upload = multer({ dest: "uploads/" });

router.post("/upload", upload.single("pdf"), qPaperUpload);

export default router;
