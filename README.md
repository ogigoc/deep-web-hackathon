# Deep Web Hackathon Project

**The code in this repository has been created for a hackathon, and so it
contains unfinished work and is generally unpolished.**

This repository contains *Excadrill*, a deep web data extraction and analytics
platform. Its purpose is to crawl Tor hidden services pertaining to predefined
keywords, extract meaningful data from them, and present it in a useful form,
from which conclusions can be drawn. It is divided into two parts: *discovery*
and *analytics*.

## Discovery

The discovery module crawls .onion domains, using results from several deep web
search engines as a starting point. The data is parsed in an attempt to separate
high-quality data from noise on pages, using an algorithm specifically optimized
for the structure of typical Tor hidden services. Crawling is prioritized by
several parameters and heuristics, and the results are stored in a PostgreSQL
database for further interaction.

## Analytics

The analytics module analyzes the stored data, and extracts several useful
features, such as dates and times, geographical locations, sentiments, etc. The
results are summarized, also stored in the database, and visualized on an HTML5
dashboard developed using React and Semantic UI.

Due to the limited time available for the completion of the project (48 hours),
several example analysis tools and visualizations have been developed as a
proof of concept.

The dashboard also provides current status of the disovery process running on the
server, with the ability to run new crawling jobs from given keywords and monitor
the progress of existing ones.

The widgets provided are:

* **Geographical sentiment**: Displays overall sentiment (on a positive-negative
  spectrum) about geographical locations mentioned in the data on a map.
* **Topical opinion analysis**: Given a specific topic, traverses the data
  and summarizes the sentiments expressed towards it.
* **Keyword trends**: Given a time period, displays the most popular terms
  encountered in text from that period, alongside a graphical plot of their
  trends through time.

![Dashboard Screenshot](/screenshots/dashboard.png?raw=true "Dashboard Screenshot")
