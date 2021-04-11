# YouTube exact subscription count scraper

Get your exact subscription count into a file using Selenium and headless Chrome.

```bash
docker build . -t yt-subs-scraper

docker run GUSERNAME="user_with_access_to_channel@gmail.com" -e GPASSWORD="password" -e CHANNELID="UCiL94444444444" -e PHONENUMBER="+358 4512312345" yt-subs-scraper

```