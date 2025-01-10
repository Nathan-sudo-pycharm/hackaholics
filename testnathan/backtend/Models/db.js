const mongoose = require("mongoose");
const mongo_url = process.env.MONGODB_URL;

mongoose
  .connect(mongo_url, {
    useNewUrlParser: true, // Optional but recommended
    useUnifiedTopology: true, // Optional but recommended
  })
  .then(() => {
    console.log("MongoDB connected...");
  })
  .catch((err) => console.log("MongoDB connection error:", err));
