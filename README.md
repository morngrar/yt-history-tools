# Youtube watch history tools

This is a collection of scripts to analyse one's youtube watch history through exported data. Sadly, it is no longer possible to poll this through google's API, so these scripts have to work by parsing data exported from [Google Takeout](https://takeout.google.com/).

To ensure that you export from the correct account, go to youtube and right-click your portrait. Choose "manage account". Go to "Data & Privacy" and scroll down to the bottom and click on "Download your data" in the right-side box called "Download or delete your data".

## To get only the watch history

First click "Deselect all", then scroll all the way to the bottom, and select "YouTube and YouTube Music". Then, click on "All YouTube data included" that is now highlighted, and "Deselect all" again. Now select "history" and click "ok". Then click "Next step". Pick relevant options and click "Create export".

## Usage

When you've downloaded your export, extract the file and locate "watch-history.html" and copy it into the same directory as the scripts.

Run `parser.py` to transform the html data into a CSV file that is lighter to work with. **This may take several minutes depending on the size of the file.**

Once the parsing is complete, run the `plotter.py` script to plot your data. Play around with the parameters in the top of the script for different settings.
