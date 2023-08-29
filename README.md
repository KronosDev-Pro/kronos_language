# Kronos Language

Kronos Language (kl) est un langage avec son transpiler embarquer


## BUILD EXE
```bash
pyinstaller main.py --clean -c --version-file 0.1.0 --add-data generator:generator --add-data kl:kl -n kl --noconfirm -F --log-level ERROR
```

## SETUP EXE
```bash
sudo cp dist/kl /usr/bin/kl
sudo chmod +x /usr/bin/kl
```