 
![Dashboard Logo](https://raw.githubusercontent.com/mikesmth/pi-dashboard/master/images/pi-dash-logo.jpg)

Pi-Dashboard

![](https://github.com/mikesmth/pi-dashboard/blob/master/images/pi-dashboard.gif?raw=true)

This project is based on a Desktop monitor app named pkmeter, originally written
by [Michael Shepanski](https://github.com/pkkid/pkmeter)

The Pi Dashboard was started as a stand-alone GUI project, aiming to create a
simple yet useful dashboard interface for small touch screen enabled devices
like the Raspberry Pi using a display module add-on.

At home, with our decision to upgrade our old monochrome weather station to
[Netatmo’s version](https://www.netatmo.com/product/weather/), after a while we
started to miss the old habit of looking at the display in the kitchen showing
the current weather information. This initiated the idea to create one myself,
with a Raspberry pi and the 7 inch screen ;-)

Pi Dashboard combined with the Netatmo weather plugin gives us all the info we
need. My test-unit runs with a smaller screen, a 5 inch WaveShare.

 

The plugin system allows creating new meters quickly. I believe the following
features are what makes this app different from the other solutions out there:

-   Quickly create new plugins with Python.

-   Simple html template system.

-   Allows one to use [Font Awesome](http://fontawesome.io/icons/)! and [Weather
    Icons](https://erikflowers.github.io/weather-icons/)  e.g. (Fonts in SVG
    format)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<vframe name='pre_icon' bgimage='fa.battery-three-quarters'>�
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Preferences are set in the app configuration (no hard-coding)

### Available Meters

-   Clock (Default)

-   Page Turner (Default. Plugins are displayed in one or more pages, this
    enables automatic paging)

-   System Monitor

-   Weather Underground

-   Netatmo Weather Stations and Gauges

Coming up (to be ported to a larger resolution):

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

-   Yahoo! Weather

Wannahaves:

-   Ability for a plugin store, linked to this repo, so you can easily
    add/remove plugins.
-   Language Support for English, Russian, Dutch and Polish to begin with.
 

PiDash is based on Python3, Qt5 and PyQt5. It runs on any device supporting
these including the Raspberry Pi. It is designed for a resolution of 800x480 and
is meant to be used with a touchscreen.

Raspberry Pi installation
-------------------------

Installing the PiDash on a Raspberry Pi with all prerequisites is quite simple.
However, I did walk into some trouble getting Python 3.5.2 installed in
combination with Qt5.7 and PyQt5.8.1 on Raspbian. They are not available in the
current repositories. With a few hacks it is fixable though.

 

Use
[Applepi-baker](https://www.tweaking4all.com/software/macosx-software/macosx-apple-pi-baker/)
on MacOS to make yourself a SD card to boot from or go
[here](http://elinux.org/RPi_Easy_SD_Card_Setup) for other platforms.

After booting there are some on-screen instructions to follow. I created a
standard user named pi.

The following instructions assume that you have a raspberry pi running Raspbian
with [a small 5 inch 800xx480 LCD](https://www.youtube.com/watch?v=SbKkR57wpcY).

 

### Enable SSH

Follow these commands and you are ready for remote access:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo raspi-config
# in the menu choose
> Interfacing Options
> SSH > Enable Yes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

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
# Raspbian on Raspberry Pi 3! only (not 2)
wget http://www.waveshare.com/w/upload/7/74/LCD-show-170309.tar.gz
tar -xvf LCD-show-170309.tar.gz
rm LCD-show-170309.tar.gz
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd LCD-show
./LCD5-show
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The device reboots and the screen will already look better.

configuring the touch screen:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
wget http://www.waveshare.com/w/upload/3/37/Xinput-calibrator_0.7.5-1_armhf.zip
unzip Xinput-calibrator_0.7.5-1_armhf.zip
cd xinput-calibrator_0.7.5-1_armhf/
sudo dpkg -i -B xinput-calibrator_0.7.5-1_armhf.deb 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now you can calibrate the screen by starting the calibration app from the menu
in Raspbian or from the Control Center in Ubuntu Mate. It will display the
parameters you need to provide in the calibration config file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Raspbian
sudo nano /usr/share/X11/xorg.conf.d/99-calibration.conf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now enter the previously acquired values:

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

The UI is meant to be used with the finger. This means no mouse cursor is
needed. Also screen blanking is usually not wanted in this case. This can be
accomplished by changing the file `/etc/X11/xinit/xserverrc` like this.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo nano /etc/X11/xinit/xserverrc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#!/bin/sh
exec /usr/bin/X -s 0 dpms -nocursor -nolisten tcp "$@"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

### Locale Settings

In my case I needed to do some extra locale setting

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# locale-gen en_US en_US.UTF-8 ru_RU ru_RU.UTF-8
# dpkg-reconfigure
# above does not seem to work (anymore), locale dafults to en_GB, so 
# we need to configure the ones we need in raspi-config

nano ~/.bashrc
#insert at the end:

export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_TYPE=en_US.UTF-8

# reload:
source ~/.bashrc

# Repeat above steps for root and pi users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

### Python 3.4.2

Fortunately it is installed by default (unfortunately not v 3.5.2)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# check version
python3 --version
# output: "Python 3.4.2"

#upgrade pip and setuptools
sudo pip3 install -U pip
sudo pip3 install -U setuptools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python 3.4.2 has an issue with http requests. For this reason I update
urllib.request to the version of Python 3.4.4

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mv /usr/lib/python3.4/urllib/request.py /usr/lib/python3.4/urllib/request.old
cd /usr/lib/python3.4/urllib/
wget https://raw.githubusercontent.com/mikesmth/pi-dashboard/master/support/request.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

### Qt5 and PyQt5

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo su
# install Qt5 and PyQt5
apt-get install python3-pyqt5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

Now we install essentials for running the Pi-Dashboard

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo su
# for configuration to safely store credentials:
# for mac/windows
pip3 install keyring
# for rasbian
pip3 install keyring
pip3 install keyrings.alt

# install Font Awesomehttp://fontawesome.io/ fonts to use as icons
pip3 install qtawesome

# install xml library
pip3 install xmltodict

# support icalendar plugin
pip3 install icalendar

# support system plugin
pip3 install psutil
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

And another little hack, because in this release, at the current state has a
broken keyring package, which breaks keyrings.alt. Without it, we cannot store
credentials in the keyring.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nano /usr/local/lib/python3.4/dist-packages/keyring/py27compat.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enter above these lines:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
try:
    text_type = unicode
    string_types = unicode, str
except NameError:
    text_type = str
    string_types = str,
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

the following:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
try:
    unicode_str = unicode
except NameError:
    unicode_str = str
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

### Boot PiDash

First place the entire [pidash
directory](https://github.com/harbaum/TouchUI/tree/master/touchui) in the
`/home/pi` directoy.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git clone https://github.com/mikesmth/pi-dashboard.git pidash
cd pidash
# let's try
python3 ./pi-dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Change into it, and set permissions:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd ~/pidash
chmod 777 ./pi-dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

 

Have fun!

 

Greetings,

 

Mike van der Sluis

MyBestTools
