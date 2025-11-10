<p align="center">
<a href="https://www.paypal.com/donate/?hosted_button_id=7CPLHJ3PT47KQ">
 <img  alt="Donate with PayPal button" border="0" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" />
</a>
</p>

## 📌 About XtreamCodes Server
Installer Xtream-UI currently supports linux 18, 20, 22, 24
This is an installation mirror for xtream ui software on Ubuntu.

## ⚙️ Installation
Update your ubuntu first, then install panel:
``` 
sudo apt update && sudo apt full-upgrade -y && rm -rf install.py && wget https://github.com/xoceunder/Xtream-UI-install/raw/main/install.py && sudo python3 install.py 
```
## 📡 Streaming URLs
| Platform | URL Format |
|----------|------------|
| **XtreamCodes** | `http://<host>:25500` |
| **MAG/Stalker Portal** | `http://<host>:25461/stalker_portal/c/` |
| **M3U Playlist** | `http://<host>:25461/get.php?username=test&password=test&type=m3u_plus&output=ts` |

📌 **Refer to the API documentation for details on GET request parameters.**

## 🛠️ Managing the Panel
To start the Xtream Codes panel, use:
```sh
sudo systemctl start xtreamcodes
```
| Command | Description |
|---------|------------|
| `status` | Status the panel |
| `start` | Start the panel |
| `stop` | Stop the panel |
| `restart` | Restart the panel |
| `reload` | Reload Nginx configuration |