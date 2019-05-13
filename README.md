# timebox
With this code you can control timebox from divoom, sound + image.   
Most of this code is not from me, for real authors take a look on https://github.com/derHeinz/divoom-adapter or https://github.com/jbfuzier/timeboxmini .    

On Domoticz use the wrapper "timebox.sh", you can enable log with it too.   

Somes exemples

- python timebox.py time --sound="son1.wav"   
- python timebox.py text --c 255,0,0 "hello world"   
- python timebox.py temperature --c 0,255,0   
- python timebox.py image mascotte.png   

# Requirement
sudo apt-get install bluealsa   
pip install Pillow   
pip install pybluez   

sudo apt-get install libboost-python-dev libboost-thread-dev libbluetooth-dev libglib2.0-dev   
sudo apt-get install bluealsa   (If you want to use mpg123 for mp3 ou stream).   
