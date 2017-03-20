 
=

![Dashboard Logo](https://raw.githubusercontent.com/mikesmth/pi-dashboard/master/images/pi-dash-logo.jpg)

Pi-Dashboard

The Pi Dashboard was started as a stand-alone GUI project aiming to create a
simple yet useful dashboard interface for small touch screen enabled devices
like the Raspberry Pi using a display module add-on.

Plugin system allows creating new meters quickly. I believe the following
features are what makes this app different from the other solutions out there:

-   Quickly create new plugins with Python.

-   Simple html template system.

-   Preferences set in the app (no hard-coding).

### Available Meters

-   Clock (Default)

![](https://github.com/mikesmth/pi-dashboard/blob/master/images/pi-dash-clock.png?raw=true)

-   Page Turner (Default. Plugins are displayed in one or more pages, this
    enables automatic paging)

-   System

    ![](https://raw.githubusercontent.com/mikesmth/pi-dashboard/master/images/pi-dash-system.png)

-   Google Calendar

-   LmSensors

-   NVIDIA

-   Network

-   Picasa Images

-   Plex Media (recently added items)

-   Plex Server (currently streaming items)

-   Processes

-   Sickbeard/SickRage

-   Sonarr

-   System Monitor

-   Weather Underground

-   Yahoo! Weather

![Netatmo Plugin](https://raw.githubusercontent.com/mikesmth/pi-dashboard/master/images/pi-dash-netatmo.jpg)

![Weather Underground Plugin](https://raw.githubusercontent.com/mikesmth/pi-dashboard/master/images/pi-dash-weather.jpg)

![Configuration](https://raw.githubusercontent.com/mikesmth/pi-dashboard/master/images/pi-dash-config.jpg)

![About PiDash](https://raw.githubusercontent.com/mikesmth/pi-dashboard/master/images/about.jpg)

PiDash is based on Python3, Qt5 and PyQt5. It runs on any device supporting
these including the Raspberry Pi. It is designed for a resolution 800x480 and is
meant to be used with a touchscreen.

Raspberry Pi installation
-------------------------

Use
[Applepi-baker](https://www.tweaking4all.com/software/macosx-software/macosx-apple-pi-baker/)
on MacOS to make yourself a basic Raspbian SD card to boot from or go
[here](http://elinux.org/RPi_Easy_SD_Card_Setup).

Installing the PiDash on a raspberry pi is quite simple. The following
instructions assume that you have a raspberry pi running raspbian with [a small
5 inch LCD](https://www.youtube.com/watch?v=SbKkR57wpcY).

 

### Display Setup

In my case setting up the display needed to be done with the following steps:

edit boot.txt:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo nano /boot/config.txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

scroll down to the hdmi_drive setting below, and add these values:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# uncomment to force a HDMI mode rather than DVI. This can make audio work in
# DMT (computer monitor) modes
#hdmi_drive=2
hdmi_group=2
hdmi_mode=87
hdmi_cvt 800 480 60 6 0 0 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Without drivers, the screen works, but there is a yellow line visible on the
left side of the screen, so its better to install the proper drivers for the
display and of course to enable the touch function:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
wget http://www.waveshare.com/w/upload/7/74/LCD-show-170309.tar.gz
tar -xvf LCD-show-170309.tar.gz
rm LCD-show-170309.tar.gz
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

install:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd LCD-show
./LCD5-show
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The device reboots and the screen will look better.

configuring the touch screen:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
wget http://www.waveshare.com/w/upload/3/37/Xinput-calibrator_0.7.5-1_armhf.zip
unzip Xinput-calibrator_0.7.5-1_armhf.zip
rm Xinput-calibrator_0.7.5-1_armhf.zip
cd xinput-calibrator_0.7.5-1_armhf/

sudo dpkg -i -B xinput-calibrator_0.7.5-1_armhf.deb 
rm xinput-calibrator_0.7.5-1_armhf.deb
cd ..
rmdir xinput-calibrator_0.7.5-1_armhf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now you can calibrate the screen by starting the calibration app from the menu.

It will display the parameters you need to provide in the calibration config
file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo nano /usr/share/X11/xorg.conf.d/99-calibration.conf 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

now enter the previously acquired values:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section "InputClass"
        Identifier      "calibration"
        MatchProduct    "ADS7846 Touchscreen"
        Option  "Calibration"   "219 4043 161 3953"
        Option  "SwapAxes"      "0"
EndSection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

After a reboot all is well!

 

### Hide mouse cursor and disable screen blanking

The TouchUI is meant to be used with the finger. This no mouse cursor is needed.
Also scren blanking is usually not wanted in this case. This can be accomplished
by changing the file `/etc/X11/xinit/xserverrc` like this.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo nano /etc/X11/xinit/xserverrc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#!/bin/sh
exec /usr/bin/X -s 0 dpms -nocursor -nolisten tcp "$@"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###  

### Boot PiDash

First place the entire [pidash
directory](https://github.com/harbaum/TouchUI/tree/master/touchui) in the
`/home/pi` directoy.

change into it, and set permissions:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd ~/pidash
chmod 777 ./pi-dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

Make sure python3, Qt5 and PyQt5 and other libraries are installed on your Pi
with the following commands:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo su
# install python3 Qt5 and PyQt5
# apt-get install python3-pyqt5
# edit:read below...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

However!, this installs python 3.4 which [generates troubles with ssl
connections](http://stackoverflow.com/questions/28575070/urllib-not-taking-context-as-a-parameter)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TypeError: urlopen() got an unexpected keyword argument 'context'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

so we install python 3.5 alternatively:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# install dependencies for compiling
sudo apt-get install build-essential libc6-dev
sudo apt-get install libncurses5-dev libncursesw5-dev libreadline6-dev
sudo apt-get install libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
sudo apt-get install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev

# install python3.5
# download
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
# unpack
tar -xzvf Python-3.5.2.tgz
rm Python-3.5.2.tgz
cd Python-3.5.2

# this will take a while...
./configure        # 3 minutes...

# we have 4 processor cores, let's use em all.
make -j4           # 9 minutes...
sudo make install  # 4 minutes...

#cleanup
cd ..
sudo rm -fr ./Python-3.5.2*

# check version
python3 --version
# output: "Python 3.5.2"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

\# install awesome fonts to use as icons  
pip3 install qtawesome  
\# install xml library  
pip3 install xmltodict  
\# safely store creds  
\# for mac/windows  
pip3 install keyring  
\# for rasbian  
pip3 install keyring  
pip3 install keyrings.alt

\# support icalendar plugin  
\#support system plugin  
pip3 install psutil

Auto run on x-login

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mkdir ~/.config/autostart
nano ~/.config/autostart/pidash.desktop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Desktop File Contents

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[Desktop Entry]
Name=Pi Dashboard     
Exec=/usr/bin/python3 /home/pi/pidash/pi-dashboard
Type=application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After a reboot the PiDash should show up.

 
