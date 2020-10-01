#!/bin/bash

script_version=1.0
python_version=3.7
env_name=py3cv4

echo "Running Raspberry Pi4 setup script version: $script_version"

# clear space if these libraries exist
echo -e "\nClearing random packackes that are not needed\n"
sudo apt-get purge wolfram-engine
sudo apt-get purge libreoffice*
sudo apt-get clean
sudo apt-get autoremove

#update system
echo -e "\nNow update the system\n"
sudo apt-get update
sudo apt-get upgrade

#install dependencies
echo -e "\nInstalling Dependencies\n"
sudo apt-get install build-essential cmake unzip pkg-config
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk-3-dev
sudo apt-get install libcanberra-gtk*
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python3-dev

echo -e "\nInstall OpenCV\n"
cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
unzip opencv.zip
unzip opencv_contrib.zip
rm -rf ./opencv
rm -rf ./opencv_contrib
mv opencv-4.0.0 opencv
mv opencv_contrib-4.0.0 opencv_contrib

echo -e "\nSet-up python env\n"
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/get-pip.py ~/.cache/pip
echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.profile
echo "VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
echo "VIRTUALENVWRAPPER_ENV_BIN_DIR=bin" >> ~/.profile
source ~/.profile

echo -e "\nSetting up the env named: $env_name\n"
mkvirtualenv $env_name -p python3
/home/pi/.virtualenvs/py3cv4/bin/python -m pip install --upgrade pip
workon $env_name
pip install numpy

echo -e "\nCompiling OpenCV Module\n"
# store sizes
default_swapsize=$(grep CONF_SWAPSIZE /etc/dphys-swapfile | awk -F= '{print $2}')
max_swapsize=$(grep CONF_MAXSWAP /etc/dphys-swapfile | awk -F= '{print $2}')
#swap size to maxsize
sudo sed -i "s/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=$max_swapsize/" /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D ENABLE_NEON=ON -D ENABLE_VFPV3=ON -D BUILD_TESTS=OFF -D OPENCV_ENABLE_NONFREE=ON -D INSTALL_PYTHON_EXAMPLES=OFF -D BUILD_EXAMPLES=OFF ..
make -j4
sudo make install
sudo ldconfig
# swap size back to default
sudo sed -i "s/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=$default_swapsize/" /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
