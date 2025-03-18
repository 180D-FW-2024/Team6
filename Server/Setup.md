# To run server:
First create a MongoDB database called ‘LockDB’ and add the uri key to mongodb.py in Server/.
## As a Docker container:
Start up docker and run:

`docker build . --network=host -t flask_server`

After it has finished building the image, run:

`docker run -p  5002:5002 -it --name flask_server flask_server`

to start the container in interactive mode.

HTTP requests to port 5002 will be forwarded to the flask app.

## Locally:
Create a python environment and install dependencies:
```
python3 -m venv myenv
source myenv/bin/activate
```
```
pip install -r requirements.txt
```

Then run with:
```
python app.py
```

Ensure ngrok is running to forward external traffic from the Rpi.
(`ngrok https 5002 --url <domain>`)

apt-get install ffmpeg libavcodec-extra

# To run web client:
Install dependencies:
```
cd Server/testChakra/myapp
npm install
```
To run:
```
npm run dev
```