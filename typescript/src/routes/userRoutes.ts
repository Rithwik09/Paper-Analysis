import express from "express";
import { createUser, getUsers } from "../contollers/user";

const router = express.Router();

router.post("/", createUser);
router.get("/", getUsers);

export default router;
