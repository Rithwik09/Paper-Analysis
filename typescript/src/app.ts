import express from "express";
import dotenv from "dotenv";
import userRoutes from "./routes/userRoutes";
import pdfRoutes from "./routes/paperRoutes";

dotenv.config();
const app = express();
const PORT = process.env.PORT || 4000;

app.use(express.json());

app.use("/users", userRoutes);
app.use("/pdf", pdfRoutes);

app.get("/", (req, res) => {
  res.send("Prisma with PostgreSQL in Express!");
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
