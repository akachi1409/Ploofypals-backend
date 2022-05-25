const express = require('express');
const router = express.Router();
const fs = require('fs');

const app = express();

const trait = "";

router.post('/', (req, res) => {
    trait = req.body.trait;
    res.send("hello");
});

router.post('/cancel', (req, res) => {
    const dir = "./uploads/" + req.body.traitId;
    fs.rmdir(dir, { recursive: true }, (err) => {
        if (err) {
            throw err;
        }
    });
})
module.exports = router;