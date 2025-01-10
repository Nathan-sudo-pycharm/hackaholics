const mongoose = require("mongoose");
const mongo_url =
  "mongodb+srv://nathan2:q7Bmm0OBvBp1mygC@cluster0.ppdcq.mongodb.net/testdb?retryWrites=true&w=majority&appName=Cluster0";

mongoose
  .connect(mongo_url, {
    useNewUrlParser: true, // Optional but recommended
    useUnifiedTopology: true, // Optional but recommended
  })
  .then(() => {
    console.log("MongoDB connected...");
  })
  .catch((err) => console.log("MongoDB connection error:", err));
