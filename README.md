# Capstone-Group7
Repository for Group 7 capstone project.

The goal of this project is to create the tools needed to wirelessly transmit video to a computer from a Stembot 2 via an onboard Raspberry Pi.


The current functionality offered by this repository is a kind of "proof of concept" and contains files that help configure the pi and allow streaming of video over a network to a computer. Currently there are three components in this repository:

  1. rasberryPiSetup: This folder contains a shell script to be run on the Raspberry Pi. This downloads the different libraries needed for the streaming.
  
  2. piServer: This folder contains a Python program that sends camera input to a specified IP address.
  
  3. localClient: This folder contains another Python program that receives the camera input at the designated IP address and displays it using opencv.
  
  
Instuctions for use:

It is the first step is to ensure that the Raspberry Pi is set up correctly and has the camera enabled. After that the user should run the shell script on the pi to download the necessary libraries. Next, configure the running enviornment on the computer, installing dependancies as nessessary. Then modify the ip address of both the client and server side scripts to the IP address of the client. Finally run the scripts and the video should stream to the computer!
