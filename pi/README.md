
## poetry 準備
sudo apt-get install python3-distutils
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry install
sudo cp sensor.service /etc/systemd/system/
sudo systemctl enable sensor