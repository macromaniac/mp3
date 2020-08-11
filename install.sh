wget https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv7l.sh
chmod +x Berryconda3-2.0.0-Linux-armv7l.sh
./Berryconda3-2.0.0-Linux-armv7l.sh


source /home/pi/berryconda3/bin/activate
pip install RPi.GPIO

pip install python-vlc

sudo apt install vlc -y
#not sure if this is needed 🤷‍♀️
sudo apt install python-alsaaudio -y
sudo apt install libasound2-dev -y

pip install pyalsaaudio

#make it a service
cat > /etc/systemd/system/mp3.service <<ENDOFFILE
[Unit]
Description=Mp3 player
After=syslog.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/mp3
ExecStart=/home/pi/berryconda3/bin/python /home/pi/mp3/main.py
StandardOutput=syslog
StandardError=syslog
Restart=always

[Install]
WantedBy=multi-user.target
ENDOFFILE

systemctl enable mp3
systemctl start mp3