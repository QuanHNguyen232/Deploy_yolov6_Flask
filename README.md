# Deploy-yolov6-Flask

## Future work:
* [X] Deploy on Heroku: Failed (Not idea how to fix)
* [ ] Allow upload multiple files
* [ ] Allow upload mp4

<p align="right"><a href="#deploy-yolov6-flask">[Back to top]</a></p>

## Instruction
* Create virtual environment (suggest using Anaconda): `conda create --name <env-name> python=3.8`
* Clone YOLOv6 github: `git clone https://github.com/meituan/YOLOv6.git`
* Download pretrained weight file: https://github.com/meituan/YOLOv6#benchmark
* Install required libraries: `pip install -r requirements.txt`

<p align="right"><a href="#deploy-yolov6-flask">[Back to top]</a></p>


## Video Walkthrough
Here's a walkthrough of implemented features:

<img src='app-walkthrough.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

GIF created with [ScreenToGif](https://www.screentogif.com/) ver.2.37 portable (x64).  

<p align="right"><a href="#deploy-yolov6-flask">[Back to top]</a></p>

<!-- Follow https://www.youtube.com/watch?v=I9BBGulrOmo
 ==> https://tutorial101.blogspot.com/2021/04/python-flask-upload-and-display-image.html -->

 <!-- Heroku deploy:
 https://www.youtube.com/watch?v=SiCAIRc0pEI or https://www.youtube.com/watch?v=Li0Abz-KT78
 
 ERROR encountered: https://stackoverflow.com/questions/19846342/unable-to-parse-procfile
  -->

<details>
  <summary markdown="span">Error log when deploying heroku</summary>
  
  <ul>
<li>
2022-08-15T03:53:51.606668+00:00 app[web.1]: [2022-08-15 03:53:51 +0000] [4] [WARNING] Worker with pid 10 was terminated due to signal 15
</li>
<li>
2022-08-15T03:53:51.613438+00:00 heroku[router]: at=error code=H13 desc="Connection closed without response" method=GET path="/" host=yolo6-on-flask.herokuapp.com request_id=865d6e02-56ab-4f38-b31b-d3c653c34179 fwd="104.28.213.54" dyno=web.1 connect=0ms service=11ms status=503 bytes=0 protocol=https
</li>
<li>
2022-08-15T03:53:51.704215+00:00 app[web.1]: [2022-08-15 03:53:51 +0000] [4] [INFO] Shutting down: Master
</li>
<li>
2022-08-15T03:53:51.704284+00:00 app[web.1]: [2022-08-15 03:53:51 +0000] [4] [INFO] Reason: Worker failed to boot.
</li>
<li>
2022-08-15T03:53:51.857145+00:00 heroku[web.1]: Process exited with status 3
</li>
<li>
2022-08-15T03:53:52.030370+00:00 heroku[web.1]: State changed from up to crashed
</li>
<li>
2022-08-15T03:53:56.995723+00:00 heroku[router]: at=error code=H10 desc="App crashed" method=GET path="/favicon.ico" host=yolo6-on-flask.herokuapp.com request_id=8b8c72a4-3689-4378-a575-47cf3b2444b5 fwd="104.28.213.54" dyno=web.1 connect=5000ms service= status=503 bytes= protocol=https
</li>
<li>
2022-08-15T03:54:14.479027+00:00 heroku[router]: at=error code=H10 desc="App crashed" method=GET path="/" host=yolo6-on-flask.herokuapp.com request_id=e36efd8a-43b6-4f3e-a120-65c174a251bb fwd="104.28.213.54" dyno= connect= service= status=503 bytes= protocol=https
</li>
<li>
2022-08-15T03:54:15.031981+00:00 heroku[router]: at=error code=H10 desc="App crashed" method=GET path="/favicon.ico" host=yolo6-on-flask.herokuapp.com request_id=6cf9199a-9ce8-4b84-b234-f4da3e78aae8 fwd="104.28.213.54" dyno= connect= service= status=503 bytes= protocol=https
</li>
<li>
2022-08-15T03:54:31.000000+00:00 app[api]: Build succeeded
</li>
</ul>
 
 </details>


<p align="right"><a href="#deploy-yolov6-flask">[Back to top]</a></p>
