<p align="center">
<a href="https://www.paypal.com/donate/?hosted_button_id=7CPLHJ3PT47KQ">
 <img  alt="Donate with PayPal button" border="0" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" />
</a>
</p>

# Installer Xtream-UI
Installer Xtream-UI currently supports linux 18, 20, 22, 24
This is an installation mirror for xtream ui software on Ubuntu. Includes MariaDB 11.5 and NGINX 1.26.0 and PHP 7.4.33.

### Installation: ###
Update your ubuntu first, then install panel:
``` 
rm -rf install.py && wget https://github.com/xoceunder/Xtream-UI-install/raw/main/install.py && sudo python3 install.py 
```

## 🛠️ Managing the Panel
To start the Xtream Codes panel, use:
```sh
sudo /etc/init.d/xtreamcodes start
```
| Command | Description |
|---------|------------|
| `start` | Start the panel |
| `stop` | Stop the panel |
| `restart` | Restart the panel |
| `reload` | Reload Nginx configuration |