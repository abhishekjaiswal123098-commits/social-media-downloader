from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os
import re

app = Flask(__name__)

DOWNLOAD_FOLDER="downloads"
os.makedirs(DOWNLOAD_FOLDER,exist_ok=True)

last_file=None

HTML="""

<!DOCTYPE html>
<html>
<head>

<title>All Social Media Downloader</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

body{
margin:0;
font-family:Arial;
background:linear-gradient(-45deg,#0f172a,#1e293b,#0ea5e9,#9333ea);
background-size:400% 400%;
animation:bgmove 12s ease infinite;
color:white;
text-align:center;
}

@keyframes bgmove{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

.popup{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:black;
display:flex;
justify-content:center;
align-items:center;
z-index:1000;
}

.popup-box{
background:#111827;
padding:40px;
border-radius:20px;
}

.container{
width:90%;
max-width:600px;
margin:auto;
margin-top:70px;
padding:35px;
border-radius:20px;
background:rgba(255,255,255,0.08);
backdrop-filter:blur(15px);
}

.creator{
font-size:26px;
font-weight:bold;
margin-bottom:10px;
background:linear-gradient(90deg,#22c55e,#38bdf8,#f43f5e,#facc15);
background-size:300%;
-webkit-background-clip:text;
color:transparent;
animation:textmove 6s linear infinite;
}

@keyframes textmove{
0%{background-position:0%;}
100%{background-position:300%;}
}

.title{
font-size:32px;
font-weight:bold;
margin-bottom:15px;
}

.social{
display:flex;
justify-content:center;
gap:10px;
flex-wrap:wrap;
margin-bottom:20px;
}

.social span{
padding:8px 14px;
border-radius:8px;
background:rgba(255,255,255,0.1);
}

input{
width:85%;
padding:14px;
border-radius:8px;
border:2px solid transparent;
outline:none;
}

.valid{
border-color:#22c55e;
}

.invalid{
border-color:#ef4444;
}

button{
padding:12px 25px;
border:none;
border-radius:8px;
background:#22c55e;
color:white;
cursor:pointer;
}

button:hover{
background:#16a34a;
}

.message{
margin-top:8px;
font-size:14px;
}

.thumbnail{
width:100%;
margin-top:20px;
border-radius:10px;
}

video{
width:100%;
margin-top:20px;
border-radius:10px;
}

</style>

</head>

<body>

<div class="popup" id="popup">

<div class="popup-box">

<h1>Welcome</h1>
<h2>Abhishek Jaiswal</h2>
<p>All Social Media Downloader</p>

<button onclick="enterSite()">Enter Website</button>

</div>

</div>

<div class="container">

<div class="creator">
Creator : Abhishek Jaiswal
</div>

<div class="title">
All Social Media Downloader
</div>

<div class="social">
<span>▶ YouTube</span>
<span>📸 Instagram</span>
<span>👍 Facebook</span>
<span>🎵 TikTok</span>
</div>

<form method="post" onsubmit="return validateSubmit()">

<input type="text" id="url" name="url"
placeholder="Paste social media video link..."
onkeyup="checkLink()" required>

<div id="msg" class="message"></div>

<br>

<button type="submit">Get Video</button>

</form>

{{result|safe}}

</div>

<script>

function enterSite(){
document.getElementById("popup").style.display="none";
}

function checkLink(){

let url=document.getElementById("url");
let msg=document.getElementById("msg");

let value=url.value.toLowerCase();

let supported=[
"youtube.com",
"youtu.be",
"instagram.com",
"facebook.com",
"fb.watch",
"tiktok.com"
];

let valid=false;

for(let i=0;i<supported.length;i++){

if(value.includes(supported[i])){
valid=true;
break;
}

}

if(value.length<5){
url.classList.remove("valid","invalid");
msg.innerHTML="";
return;
}

if(valid){

url.classList.remove("invalid");
url.classList.add("valid");

msg.style.color="#22c55e";
msg.innerHTML="Supported link";

}else{

url.classList.remove("valid");
url.classList.add("invalid");

msg.style.color="#ef4444";
msg.innerHTML="Unsupported link";

}

}

function validateSubmit(){

let url=document.getElementById("url").value.toLowerCase();

let supported=[
"youtube.com",
"youtu.be",
"instagram.com",
"facebook.com",
"fb.watch",
"tiktok.com"
];

for(let i=0;i<supported.length;i++){

if(url.includes(supported[i])){
return true;
}

}

alert("Sirf YouTube, Instagram, Facebook, TikTok link dale");
return false;

}

</script>

</body>
</html>

"""

@app.route("/",methods=["GET","POST"])
def home():

    global last_file
    result=""

    if request.method=="POST":

        url=request.form.get("url")

        try:

            ydl_opts={
            "format":"best",
            "outtmpl":f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s"
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                info=ydl.extract_info(url,download=True)

                last_file=ydl.prepare_filename(info)

                title=info.get("title","Video")
                thumb=info.get("thumbnail","")

            result=f'''

            <h3>{title}</h3>

            <img src="{thumb}" class="thumbnail">

            <video controls>
            <source src="/download">
            </video>

            <br><br>

            <a href="/download">
            <button>Download Video</button>
            </a>

            '''

        except:

            result="<h3 style='color:red'>Video download error</h3>"

    return render_template_string(HTML,result=result)


@app.route("/download")
def download():

    global last_file

    if last_file and os.path.exists(last_file):

        return send_file(last_file,as_attachment=True)

    return "File not found"


app.run(host="0.0.0.0",port=5000)