from fastapi import FastAPI,UploadFile, File
from jinja2 import Template
from PyPDF2 import PdfReader
import requests
import os
import json
import zipfile


app= FastAPI()

apikey=""

prompt=""" please extract informations like name,summery,skills,education, experience from the content given and return a structured json in the example as 
{
'name': 'Rahul Roy',
'summ':'I am Rahul the great philosopher',
'item2s':{{'name':'xyz institute','value':'96% --2022-- MBA'},{'name':'abc institute','value':'86% --2020-- BBA'}},
'item3s':{{'name':'xyz Company','value':'I work here for experience'},{'name':'abc Company','value':'I love to work here.'}},
'item1s':{{'value':'Power BI'},{'value':'sql'}}

}.donot give any extra text.I only want json """


temp1="""<!DOCTYPE html>
<html>
<head>
    <title>index</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container text-center" style="margin:0px;">
    <div class="row">
        <div class="col-3" style="background-color: #5DBE95;height:100vh ; color:whitesmoke">
            <br>
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQBFy0j_72yEKBKNRbPbCzxfNxq1H9Y57ygg&s" class="rounded float-start" alt="..." style="border-radius:100px; height:20vh;width:15vw; margin-left:3vw">
            <p>_</p>
            
            <h5 style="padding-left:0px;margin-top:10px"><i><b>Skills</b></i></h5>
            {% for item in item1s %}
            <p>{{item.value}}</p>
            {% endfor %}
        </div>
        <div class="col-9" style="height:max-content; text-align: left;">
                <h2 style="margin:10px;">{{name}}</h2>
                <p style="margin-left:10px">{{summ}}</p>
                <h4 style="margin-left:10px">Education</h4>
                    {% for item in item2s %}
                    <h5 style="margin-left:15px">{{item.name}}</h5>
                    <p style="margin-left:15px">{{item.value}}</p>
                    {% endfor %}
        <h4 style="margin-left:10px">Experience</h4>
        <div class="d-flex flex-row">
            {% for item in item3s %}
            <div class="card" style="width: 18rem; margin-left: 10px;">
                <div class="card-body">
                <h6 class="card-subtitle mb-2 text-body-secondary">{{item.name}}</h6>
                <p class="card-text">{{item.name}}</p>
                </div>
            </div>
            {% endfor %}
        </div>

    </div>
</div>"""

temp2="""<!DOCTYPE html>
<html>
<head>
    <title>index</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body style="background-color: #3c3c3c;">
     <h1 style="color: #c0c0c0; width:10vw; font-size:15vh; margin-left:5vw; margin-top:2vh;line-height: 1;"><b>{{name}}</b></h1>
     <p style="color:#171717de;margin-left:5.2vw;font-size:large"><b>{{summ}}</b></p>
     <h3 style="margin-left:70vw;color:whitesmoke;margin-top:-25vh"><b>EDUCATION</b></h3>
     {% for item in item2s %}
     <p style="color:#c7c5c5de;margin-left:70vw;font-size:small;width:15vw"><b>{{item.name}} {{item.value}}</b></p>
    {% endfor %}
     <img src="https://i.postimg.cc/tRBK8c1S/Screenshot-2025-07-20-211012.png" style="margin-left:59vw;height:30vh;">
 
    <div class="d-flex flex-row">
            <div class="card" style="width: 18rem; margin-top:0vh;margin-left: 10vh; background-color:#161616c2">
                <div class="card-body">
                {% for item in item3s %}
                <h6 class="card-subtitle mb-2 text-body-secondary" style="color:rgb(14, 241, 146) !important;">{{item.name}}</h6>
                <p class="card-text" style="color:rgb(137, 136, 136)">{{item.value}}</p>
                {% endfor %}
                </div>
            </div>
    </div>
    <p style="color:rgb(14, 241, 146) !important; margin-left:90vw;"><b>SKILLS</b></p>
    {% for item in item1s %}
    <p style="color:rgb(192, 194, 194) !important; margin-left:90vw;margin-top:-3vh;">{{item.value}}</p>
    {% endfor %}
    
</body>
</html>
"""
@app.post("/resumeP/{choices}")
async def read(choices,file: UploadFile = File(...)):
    reader=PdfReader(file.file)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
    "Authorization": f"Bearer {apikey}",
    "Content-Type": "application/json"}
    data = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
    ]}

    res = requests.post(url, headers=headers, json=data)
    L=res.json()['choices'][0]['message']['content']
    L2=json.loads(L)
    if choices== "Template1":
        new_temp=Template(temp1)
    else:
        new_temp=Template(temp2)
        
    abcd=new_temp.render(name=L2["name"],summ=L2["summ"],item1s=L2["item1s"],item2s=L2["item2s"],item3s=L2["item3s"])
    os.makedirs("site", exist_ok=True)
    path = "site/index.html"
    with open(path, "w") as f:
        f.write(abcd)


    zip_path = "site.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(path, arcname="index.html")

    NETLIFY_TOKEN = ""  
    headers = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}
    files = {"file": open(zip_path, "rb")}
    resp = requests.post("https://api.netlify.com/api/v1/sites", headers=headers)

    if resp.status_code == 201:
        site_id = resp.json()["id"]
        deploy_url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"

        deploy_resp = requests.post(deploy_url, headers=headers, files=files)

        if deploy_resp.status_code == 200:
            deploy_data = deploy_resp.json()
            print(deploy_data["deploy_ssl_url"])
        else:
            print(deploy_resp.text)
    else:
        print(resp.text)    



    return deploy_data["deploy_ssl_url"]



