 
=

![Dashboard Logo](https://raw.githubusercontent.com/mikesmth/pi-dashboard/master/images/pi-dash-logo.jpg)

Pi-Dashboard

![](https://github.com/mikesmth/pi-dashboard/blob/master/images/pi-dashboard.gif?raw=true)

The Pi Dashboard was started as a stand-alone GUI project aiming to create a
simple yet useful dashboard interface for small touch screen enabled devices
like the Raspberry Pi using a display module add-on.

Plugin system allows creating new meters quickly. I believe the following
features are what makes this app different from the other solutions out there:

-   Quickly create new plugins with Python.

-   Simple html template system.

-   Preferences set in the app (no hard-coding)

### Available Meters

-   Clock (Default)

-   Page Turner (Default. Plugins are displayed in one or more pages, this
    enables automatic paging)

-   System Monitor

-   Weather Underground

-   Netatmo Weather Stations and Gauges

Coming up

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

# we have 4 processor cores, let's use em.
make -j4           # 9 minutes...
sudo make install  # 4 minutes...

#cleanup
cd ..
sudo rm -fr ./Python-3.5.2*

# check version
python3 --version
# output: "Python 3.5.2"
pip3 list
# pip (7.1.2)
# setuptools (18.2)
# You are using pip version 7.1.2, however version 9.0.1 is available.
# You should consider upgrading via the 'pip install --upgrade pip' command.

#upgrade pip and setuptools
sudo pip3 install -U pip
sudo pip3 install -U setuptools

#phew! done.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we need to compile Qt5 because at the moment there is no wheel for the arm
platform

Prepare with libs:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo apt-get -y install libfontconfig1-dev libdbus-1-dev libfreetype6-dev
sudo apt-get -y libudev-dev libicu-dev libsqlite3-dev libxslt1-dev  libssl-dev
sudo apt-get -y libasound2-dev libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get -y libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev 
sudo apt-get -y gstreamer-tools  gstreamer0.10-plugins-good 
sudo apt-get -y gstreamer0.10-plugins-bad libraspberrypi-dev  libpulse-dev 
sudo apt-get -y libx11-dev libglib2.0-dev libcups2-dev freetds-dev  libsqlite0-dev
sudo apt-get -y libpq-dev libiodbc2-dev libmysqlclient-dev firebird-dev  
sudo apt-get -y libpng12-dev libjpeg9-dev libgst-dev libxext-dev libxcb1 
sudo apt-get -y libxcb1-dev  libx11-xcb1 libx11-xcb-dev libxcb-keysyms1 
sudo apt-get -y libxcb-keysyms1-dev  libxcb-image0 libxcb-image0-dev libxcb-shm0
sudo apt-get -y libxcb-shm0-dev  libxcb-icccm4 libxcb-icccm4-dev libxcb-sync-dev 
sudo apt-get -y libxcb-render-util0  libxcb-render-util0-dev libxcb-xfixes0-dev
sudo apt-get -y libxrender-dev  libxcb-shape0-dev libxcb-randr0-dev libxcb-glx0-dev
sudo apt-get -y libxi-dev libdrm-dev  libssl-dev
sudo apt-get install libxcb-xinerama0-dev
sudo apt-get install libffi-dev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make your build directory:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mkdir ~/opt
cd ~/opt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Retrieve qt5 source code from git:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git clone git://code.qt.io/qt/qt5.git
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Retrieve git sources for other components

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd qt5
./init-repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Do not apply any patches that are available out there. They are no longer
necessary with the latest Qt5. The git source should compile with a few tricks
in the configure parameters without any patches.

First make sure you are in the qt5 directory.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd ~/opt/qt5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All output is stored in the file called ‘output’ in case something goes wrong.
At the end of the output file it should say you can run ‘make’, if not look for
errors at the end of the output.

Do not be concerned with some things not building due to missing packages, there
will be errors for those. If it does not mention that you can run make then
check the last error, it is generally the show-stopper. Run configure:

Run configure:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
./configure -v -opengl es2 -device linux-rasp-pi-g''+  -device-option CROSS_COMPILE=/usr/bin/  -opensource -confirm-license  -optimized-qmake -reduce-exports  -release -qt-pcre -qt-libpng -make libs -prefix /usr/local/qt5 &>  output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can tail the logfile during building in another session:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
tail -f ~/opt/qt5/output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The output will look something like:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Configure summary:
Building on: linux-g++ (arm, CPU features: <none>)
Building for: devices/linux-rasp-pi-g++ (arm, CPU features: <none>)
Configuration: cross_compile use_gold_linker compile_examples enable_new_dtags largefile precompile_header shared rpath accessibility release c++11 c++14 concurrent dbus no-pkg-config mremap reduce_exports release_tools stl
Build options:
  Mode ................................... release; optimized tools
  Building shared libraries .............. yes
  Using C++ standard ..................... C++14
  Using gold linker ...................... yes
  Using new DTAGS ........................ yes
  Using precompiled headers .............. yes
  Using LTCG ............................. no
  Target compiler supports:
    NEON ................................. no
  Build parts ............................ libs
Qt modules and options:
  Qt Concurrent .......................... yes
  Qt D-Bus ............................... yes
  Qt D-Bus directly linked to libdbus .... no
  Qt Gui ................................. yes
  Qt Network ............................. yes
  Qt Sql ................................. yes
  Qt Testlib ............................. yes
  Qt Widgets ............................. yes
  Qt Xml ................................. yes
Support enabled for:
  Accessibility .......................... yes
  Using pkg-config ....................... no
  QML debugging .......................... yes
  udev ................................... yes
  Using system zlib ...................... yes
Qt Core:
  DoubleConversion ....................... yes
    Using system DoubleConversion ........ no
  GLib ................................... no
  iconv .................................. no
  ICU .................................... yes
  Logging backends:
    journald ............................. no
    syslog ............................... no
    slog2 ................................ no
  Using system PCRE ...................... no
Qt Network:
  getaddrinfo() .......................... yes
  getifaddrs() ........................... yes
  IPv6 ifname ............................ yes
  libproxy ............................... no
  OpenSSL ................................ yes
    Qt directly linked to OpenSSL ........ no
  SCTP ................................... no
  Use system proxies ..................... yes
Qt Sql:
  DB2 (IBM) .............................. no
  InterBase .............................. no
  MySql .................................. no
  OCI (Oracle) ........................... no
  ODBC ................................... no
  PostgreSQL ............................. no
  SQLite2 ................................ no
  SQLite ................................. yes
    Using system provided SQLite ......... no
  TDS (Sybase) ........................... no
Qt Gui:
  FreeType ............................... yes
    Using system FreeType ................ no
  HarfBuzz ............................... yes
    Using system HarfBuzz ................ no
  Fontconfig ............................. no
  Image formats:
    GIF .................................. yes
    ICO .................................. yes
    JPEG ................................. yes
      Using system libjpeg ............... no
    PNG .................................. yes
      Using system libpng ................ yes
  OpenGL:
    EGL .................................. yes
    Desktop OpenGL ....................... no
    OpenGL ES 2.0 ........................ yes
    OpenGL ES 3.0 ........................ no
    OpenGL ES 3.1 ........................ no
  Session Management ..................... yes
Features used by QPA backends:
  evdev .................................. yes
  libinput ............................... no
  mtdev .................................. no
  tslib .................................. no
  xkbcommon-evdev ........................ no
QPA backends:
  DirectFB ............................... no
  EGLFS .................................. yes
  EGLFS details:
    EGLFS i.Mx6 .......................... no
    EGLFS i.Mx6 Wayland .................. no
    EGLFS EGLDevice ...................... no
    EGLFS GBM ............................ no
    EGLFS Mali ........................... no
    EGLFS Raspberry Pi ................... yes
    EGL on X11 ........................... no
  LinuxFB ................................ yes
  Mir client ............................. no
Qt Widgets:
  GTK+ ................................... no
  Styles ................................. Fusion Windows
Qt PrintSupport:
  CUPS ................................... no
Qt SerialBus:
  Socket CAN ............................. yes
  Socket CAN FD .......................... yes
QtXmlPatterns:
  XML schema support ..................... yes
Qt QML:
  QML interpreter ........................ yes
  QML network support .................... yes
Qt Quick:
  Direct3D 12 ............................ no
  AnimatedImage item ..................... yes
  Canvas item ............................ yes
  Support for Quick Designer ............. yes
  Flipable item .......................... yes
  GridView item .......................... yes
  ListView item .......................... yes
  Path support ........................... yes
  PathView item .......................... yes
  Positioner items ....................... yes
  ShaderEffect item ...................... yes
  Sprite item ............................ yes
Qt Gamepad:
  SDL2 ................................... no
Qt 3D:
  System Assimp .......................... no
Qt Wayland Client ........................ no
Qt Wayland Compositor .................... no
Qt Bluetooth:
  BlueZ .................................. no
  BlueZ Low Energy ....................... no
  Linux Crypto API ....................... no
Qt Sensors:
  sensorfw ............................... no
Qt Multimedia:
  ALSA ................................... yes
  GStreamer 1.0 .......................... no
  GStreamer 0.10 ......................... no
  Video for Linux ........................ yes
  OpenAL ................................. no
  PulseAudio ............................. no
  Resource Policy (libresourceqt5) ....... no
  DirectShow ............................. no
  Windows Media Foundation ............... no
Qt Location:
  Gypsy GPS Daemon ....................... no
  WinRT Geolocation API .................. no
Qt WebEngine:
  Proprietary Codecs ..................... no
  Spellchecker ........................... yes
  ALSA ................................... yes
  PulseAudio ............................. no
Note: Also available for Linux: linux-clang linux-kcc linux-icc linux-cxx
Note: -optimized-tools is not useful in -release mode.
Note: No wayland-egl support detected. Cross-toolkit compatibility disabled.
WARNING: Cross compiling without sysroot. Disabling pkg-config
Qt is now configured for building. Just run 'make'.
Once everything is built, you must run 'make install'.
Qt will be installed into '/usr/local/qt5'.
Prior to reconfiguration, make sure you remove any leftovers from
the previous build.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

And now we run make directly on the device ( and turn off the backlight for a
proper amount of power to the processor ) Note that Qt is a monster to compile,
so it does take some time:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# running on 4 threads on 4 cores takes approximately 3 hours on a Raspberry Pi 3
# we tried running on 8 threads on 4 cores (approximately 4 hours on a Raspberry 
# Pi 3, so that proves it does not make sense to increase threads ;-) )
# let's use 4...
make -j4 &>output-make 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor the progress from a separate ssh session (approximately x hours on a
Raspberry Pi 3):

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
tail -f ~/opt/qt5/output-make 
# when the output file becomes too large, you might want to cancel monitoring 
# after a certain amount of time. The session might become quite unresponsive. 
# Just wait it out, and check the initial command once in a while.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After which we run make install directly on the device:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
make install &>output-make-install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor the progress from a separate ssh session:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
tail -f ~/opt/qt5/output-make-install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 

After this you need to add some lines to your .bashrc file(repeat for users pi
and root):

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nano ~./bashrc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add these to the end:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
export LD_LIBRARY_PATH=/usr/local/qt5/lib/
export PATH=/usr/local/qt5/bin:/usr/local/bin:/usr/bin:/bin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to source your .bashrc file to set-up the above environment variables:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
source ~/.bashrc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Then run this and check that it points to /usr/local/qt5/bin/qmake

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
which qmake
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example output:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pi@raspberrypi$ which qmake
/usr/local/qt5/bin/qmake
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now for PyQt5:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# download / install SIP
wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.1/sip-4.19.1.tar.gz
tar - xvf sip-4.19.1.tar.gz
cd sip-4.19.1
python3 configure.py
make
make install
#cleanup
cd ..
sudo rm -fr ./sip-4.19.1*
rm sip-4.19.1.tar.gz

# download PyQt5 sources:
wget https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.8.1/PyQt5_gpl-5.8.1.tar.gz
tar -xvf PyQt5_gpl-5.8.1.tar.gz
cd PyQt5_gpl-5.8.1
python3 configure.py
make -j4
make install
#cleanup
cd ..
sudo rm -fr ./PyQt5_gpl-5.8.1*
rm PyQt5_gpl-5.8.1.tar.gz
#phew! done it again!
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

# support system plugin
pip3 install psutil

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

 
