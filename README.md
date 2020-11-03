# Capstone-Group7

Repository for Group 7 capstone project.

The goal of this project is to create the tools needed to wirelessly transmit video to a computer from a Stembot 2 via an onboard Raspberry Pi.

The current functionality offered by this repository is a kind of "proof of concept" and contains files that help configure the pi and allow streaming of video over a network to a computer. Currently there are three components in this repository:

1. rasberryPiSetup: This folder contains a shell script to be run on the Raspberry Pi. This downloads the different libraries needed for the streaming.

2. piServer: This folder contains a Python program that sends camera input to the Unity application.

3. localClient (outdated from Milestone 1 proof of concept): This folder contains another Python program that receives the camera input at the designated IP address and displays it using opencv.

4. unityIntegration: This folder contains the Unity portion of the application integration.

Instuctions for use:

It is the first step is to ensure that the Raspberry Pi is set up correctly and has the camera enabled. After that the user should run the shell script on the pi to download the necessary libraries. Next, configure the running enviornment on the computer by installing unity hub and importing the project. You then must install the version of Unity it prompts. Then modify the ip address within the Unity application (this is the IP address of the raspberry PI). Finally run the script on the raspberry PI and then start the scene within Unity. You should now see video being streamed to the Unity Application!

Docs are located at:
https://thazlett16.github.io/Capstone-Group7-Docs/
