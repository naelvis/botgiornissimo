# Botgiornissimo
Welcome to the repository for Botgiornissimo! This is my first Telegram bot and my very first Python project.

Botgiornissimo is per se a glorified alarm clock with a few extra perks - we use it to plan the weekly SSBU evening. There's a small script in the modules folder for each of its functionalities; the files are:
* **tokens.py**, which only serves to import various tokens and ID the bot uses (no, I didn't upload the tokens on the repository);
* **start.py**, which contains the start and stop functions for the bot;
* **remote.py**, which contains the handler for starting the bot remotely;
* **smashissimo.py**, which contains the alarm clock and a poll handler for the SSBU evening;
* **augurissimi.py**, which contains the functions executed on special events;
* **ocrissimo.py**, which integrates an R script to detect usernames and points in the results screen of SSBU.

References:
* The official [example list](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Examples);
* crrdvd's [amazon-bot](https://github.com/crrdvd/amazon-bot) repository;
* Documentation on the [magick](https://cran.r-project.org/web/packages/magick/vignettes/intro.html) package for R. The analogous package for Python seems not to be documented/taken care of anymore.

