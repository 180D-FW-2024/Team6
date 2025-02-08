To run server:

    create known_faces directory in static directory and populate 
        to populate make subdirectory with name of user and pictures of user

    create recvd_faces directory, also in the static directory,
        to store the faces recieved from the Rpi

    create voice_memos.csv file


    python3 -m venv myenv
        source myenv/bin/activate


    run pip install -r requirements.txt

    Move the Haar Cascade classifiers to where Deepface can access them
        cp haarcascade_eye.xml myenv/lib/python<version>/site-packages/data/
        cp haarcascade_frontalface_default.xml myenv/lib/python<version>/site-packages/data/

    run 
        python app.py


    apt-get install ffmpeg libavcodec-extra