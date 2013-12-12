CrawerNPU
=========
Main Contributor: Yu Bowen

=========
A web crawler for Northwestern Polytechnic University(China).
I found there is a spell mistake on the title of the repository, but I have no idea
on how to correct it.

2013/12/11 This term we have learned concepts about databases. Now I have developed
a more stable, more applicable web-crawler. Last version I have used files to store
the data fetched, which makes a spaghetti code and stopped this project for several
months. What's more, after closed, the states will be stored into the database which
means you can continue the work after closed it rather than repeat again. **However,
this feature is only available in windows for the moment.

Todo:
[x] 1. Multi-tasking support to be concerned.
[ ] 2. [2013/12/12] It is slow, use Performance Analysis to try to improve its performance.
Bugs For this crawer:
2013/6/25 Contents are downloaded directly into local disk without encoding conversion,
mixing up kinds of encodings.
[Solution]	Do not store all the html file into local disk, but only data in txt form, and stored in UTF-8 form.

2013/6/26 I just want to store text rather html into my local disk. Originally I store
all what I get from server into local disk, and that makes the search progress very
slow. So I modified HTMLParser to only save data except scripts or stylesheets.

2013/12/12 BUG, URL's length being 100 is not ever enough. I'll try 500.
	