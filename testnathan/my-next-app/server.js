const express = require("express");
const mongoose = require("mongoose");
const dotenv = require("dotenv");
const User = require("@/models/user");
const cors = require("cors");

dotenv.config();
const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// Connect to MongoDB
mongoose
  .connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("MongoDB connection error:", err));

// API Route to Handle Form Data
app.post("/register", async (req, res) => {
  try {
    const { firstName, lastName, password } = req.body;

    // Save the user to the database
    const user = new User({ firstName, lastName, password });
    await user.save();

    res.status(201).json({ message: "User registered successfully!" });
  } catch (error) {
    res.status(500).json({ error: "Failed to register user" });
  }
});

// Start the Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
