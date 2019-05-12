## Updating graphion server
1. ```git pull```
2. ```sudo systemctl restart graphion```
3. ```netstat -an | grep "LISTEN "```
4. Copy the ports listed from the previous parts (there should be ```n``` ports when gunicorn has been started with ```--workers n```)
5. ```sudo nano /etc/ufw/applications.d/bokeh``` and update the listed ports
6. ```sudo ufw app update Bokeh``` (and possible re-add it to the firewall)
7. ```sudo nano /etc/nginx/sites-enabled/bokeh``` and update the listed ports
8. ```sudo systemctl restart nginx```
9. graphion should now be accessible through graphion.uddi.ng