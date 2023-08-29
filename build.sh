
rm -rf ./**/__pycache__ __pycache__

pip install pyinstaller -q --no-color --no-python-version-warning --disable-pip-version-check

pyinstaller main.py --clean -c --add-data generator:generator --add-data kl:kl -n kl --noconfirm -F --log-level ERROR

sudo cp dist/kl /usr/bin/kl
sudo chmod +x /usr/bin/kl

rm -rf ./**/__pycache__ __pycache__ dist build kl.spec