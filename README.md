CrawerNPU
=========

A web crawler for Northwestern Polytechnic University(China).  爬取校园网的信息。
I found there is a spell mistake on the title of the repository, but I have no idea
on how to correct it.

Todo:
1. Multi-tasking support to be concerned. [OK]

****************************Logs*****************************
2013/6/26	Multitasking SUPPORT! This will accelerate this program a lot because a
lot of time is used to wait the server's response.

****************************Bugs*****************************
[Solved]2013/6/25 Contents are downloaded directly into local disk without encoding conversion,
mixing up kinds of encodings.
[Solution]	Do not store all the html file into local disk, but only data in txt form, and stored in UTF-8 form.

[Solved]2013/6/26 The size of files increase rapidly.
[Solution]	Every time initializing MyHTMLParser, reset the output buffer and everything's fine. This is very
strange, since A MyHTMLParser is composed of a output buffer and I don't need to reset it. The code is right
in traditional OOP Language. But Not Python.

[Solved]2013/6/26 I just want to store text rather html into my local disk. Originally I store
all what I get from server into local disk, and that makes the search progress very
slow. So I modified HTMLParser to only save data except scripts or stylesheets.

