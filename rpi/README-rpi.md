This section contains code for running the RPI event loop.

The RPI handles all sensor data for the project and relays it to the server when appropriate. 

The RPI code utilizes OpenCV to classify when a face is present in order to only transmit data when appropriate. 

Overall the code works as expected but error handling in some sections often requires a hard reset which can lead to long wait times. 
