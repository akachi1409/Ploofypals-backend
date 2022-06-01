const express = require("express");
const { spawn } = require("child_process");
const fs = require("fs");
const fse = require("fs-extra")
const path = require('path');

const fileUpload = require("express-fileupload");

const app = express();
const PORT = 80;

// default options
app.use(fileUpload());
app.use("/trait", require("./routes/trait"));
app.use("/result/rare", express.static(path.join(__dirname, "result/rare")))
app.use("/result/normal", express.static(path.join(__dirname, "result/normal")))

app.get("/images/normal", function(req, res){
  const dir = "./result/normal";
  fs.readdir(dir, function (err,files){
    if (err){
      console.log("err:",err);
      return res.status(500).send(err);
    }
    res.set('Access-Control-Allow-Origin', '*');
    res.status(200).send(files)
  })
})

app.get("/images/rare", function(req, res){
  const dir = "./result/rare";
  fs.readdir(dir, function (err,files){
    if (err){
      console.log("err:",err);
      return res.status(500).send(err);
    }
    res.set('Access-Control-Allow-Origin', '*');
    res.status(200).send(files)
  })
})

app.get("/images/legendary", function(req, res){
  const dir = "./result/legendary";
  fs.readdir(dir, function (err,files){
    if (err){
      console.log("err:",err);
      return res.status(500).send(err);
    }
    res.set('Access-Control-Allow-Origin', '*');
    res.status(200).send(files)
  })
})
app.get("/generate", function (req, res){
  try{
    console.log("------")
    const python = spawn('python', ['./art.py']);
    python.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    python.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });

    python.on('close', (code) => {
        res.set('Access-Control-Allow-Origin', '*');
        res.send("Art Collection is generated!")
        console.log(`child process exited with code ${code}`);
    });
  }catch(err){
    console.log(err);
    return res.status(500).send(err);
  }
})

app.get("/refresh", function (req, res){
  const dir1 = "./result/legendary";
  const dir2 = "./uploads";
  const dir3 = "./result/rare";
  const dir4 = "./result/normal"
  fse.emptyDir(dir1, ( err )=> {
    if (err){
      console.log("err:",err);
      return res.status(500).send(err);
    }
  })
  fse.emptyDir(dir2, (err) => {
    if (err){
      console.log("err:",err);
      return res.status(500).send(err);
    }
  })
  fse.emptyDir(dir3, (err) => {
    if (err){
      console.log("err:",err);
      return res.status(500).send(err);
    }
  })
  fse.emptyDir(dir4, (err) => {
    if (err){
      console.log("err:",err);
      return res.status(500).send(err);
    }
  })
  res.set('Access-Control-Allow-Origin', '*');
  res.send("Refreshed all the data.");
})
app.post("/upload", function (req, res) {
  const formData = req.files;
  const names = req.body.names.split(",");
  const rarity = req.body.rarity;
  const types = req.body.types;
  const trait = req.body.trait;
  console.log("rarity:", rarity, types);
  const dir = "./uploads/" + trait;
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir);
  }
  const data = {
    rarity:rarity,
    types: types,
    names: req.body.names,
    length: names.length,
    trait: trait
  }
  var jsonContent = JSON.stringify(data);
  fs.writeFile(dir+"/data.json", jsonContent, function(err){
    if(err){
      console.log("err:", err);
      return res.status(500).send(err);
    }
    console.log("The file was saved!")
  })
  names.map((name, index)=>{
    console.log("name", name);
    var file = formData[name];
    uploadPath = dir + "/" + file.name; //+ "(" + req.body.option + ")";
    // console.log("file", file);
    file.mv(uploadPath, function (err) {
      if (err) {
        console.log("err:", err);
        return res.status(500).send(err);
      }
    });
    // console.log(formData[name]);
  })
  res.set('Access-Control-Allow-Origin', '*');
  res.send("File uploaded!")
});

app.listen(PORT, (error) => {
  if (!error) {
    console.log(
      "Server is Successfully Running, and App is listening on port " + PORT
    );
    
  } else console.log("Error occurred, server can't start", error);
});

// https.createServer(
//   {
//     key: fs.readFileSync("server.key"),
//     cert: fs.readFileSync("server.cert"),
//   },
//   app
// ).listen(PORT,(error) => {
//   if (!error) {
//     console.log(
//       "Server is Successfully Running, and App is listening on port " + PORT
//     );
    
//   } else console.log("Error occurred, server can't start", error);
// });