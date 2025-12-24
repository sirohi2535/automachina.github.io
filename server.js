const express = require("express");
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Dummy repo API
app.get("/repos", (req, res) => {
    res.json({
        "automachina": {
            files: ["index.html","repo.html","commit.html"]
        }
    });
});

app.listen(8080, () => console.log("Server running on http://localhost:8080"));
