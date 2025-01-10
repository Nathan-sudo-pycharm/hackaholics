"use client";

import { connectToDatabase } from "@/utils/dbConnect";
import User from "@/models/user";

export default async function handler(req, res) {
  await connectToDatabase();

  if (req.method === "POST") {
    try {
      const { name, email, password } = req.body;

      // Validate input data
      if (!name || !email || !password) {
        return res.status(400).json({ message: "All fields are required." });
      }

      // Check if user already exists
      const existingUser = await User.findOne({ email });
      if (existingUser) {
        return res.status(400).json({ message: "User already exists." });
      }

      // Save new user
      const newUser = new User({ name, email, password });
      await newUser.save();

      res.status(201).json({ message: "User registered successfully." });
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: "Internal server error." });
    }
  } else {
    res.setHeader("Allow", ["POST"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
