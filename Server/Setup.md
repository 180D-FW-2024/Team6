To run server:
    As a Docker container:
        Start up docker.
        Then run:
        $ docker build . --network=host -t flask_server

        After it has finished building the image, run
        $ docker run -p  5002:5002 -it --name flask_server flask_server
        to start the container in interactive mode

        HTTP requests to port 5002 will be forwarded to the flask app.
    
    Locally:
        python3 -m venv myenv
            source myenv/bin/activate

        run pip install -r requirements.txt

        Move the Haar Cascade classifiers to where Deepface can access them
            cp haarcascade_eye.xml <path to myenv>/lib/python<version>/site-packages/data/
            cp haarcascade_frontalface_default.xml <path to myenv>/lib/python<version>/site-packages/data/
        run 
            python app.py


        apt-get install ffmpeg libavcodec-extra