# Let's Wikirace!
<small>
<b>Description</b>    : An simple implementation of shortest path discovery
<b>Author</b>         : Selwyn-Lloyd McPherson (selwyn.mcpherson@gmail.com)   
<b>Python Version</b> : 3.5.0
</small>


## Contents
0. [Background](#background)
1. [Problem History](#problem_history)
2. [General Approach](#general_approach)
3. [Depth vs Breadth](#depth_vs_breadth)
4. [Implementation](#implementation)
5. [Usage](#usage)
6. [On Logging](#on_logging)
7. [Performance](#performance)
8. [Results](#results)
9. [Moving Forward](#moving_forward)
10. [An Aside](#an_aside)

<a id='background'></a>
## Background
Wikiracing is a well documented sport, and is as exciting to spectate as it is to compete. The goal is to begin on one wikipedia page and click one's way to a destination page using only links in the main body of the articles along the way.  I've always found it fascinating because at each page, the wikiracer is obligated to think several steps ahead. It also emphasizes appreciating knowledge in a hierarchical way, that is to say that wikiracers must conceptualize the meaning of a word from multiple perspectives. A 'break' for example, might mean an unexpected stroke of good luck, a pause from work, or the formation of waves.  

Thankfully, computers care not for these nuances.  

<a id='problem_history'></a>
## Problem History
Studying the degree of connectedness between articles on Wikipedia has long been a source of fascination. There's even an entire Wikipedia article related
to this question (https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia).  

Most have heard of the "Six-Degrees" phenomenon, usually associated with actor Kevin Bacon, which states that two people on Earth are six or fewer acquaintance links apart. Mathematicians similarly identify themselves by an analogous metric, the Erdős number. This number defines an academic mathematician's distance from Paul Erdős, an extremely influential figure whose students and mentees number in the hundreds; the tree grows from there such that almost any published mathematician can determine the degree to wish she or he is related to Erdős himself. Six is an oft use number for the maximum reasonably path between one person and another but, amazingly, most studies show that the average distance is much lower, somewhere around 3.  

<a id='general_approach'></a>
## General Approach
Here, we'll use standard graph traversal methods to find the shortest path. It should be mentioned that, in this naïve implementation, we're going to be rather dumb. If we were to encode some knowledge about the problem __a prori__, we  might cut down on  processing time. But since we're given no other supporting information, we are forced to use a brute force method.  

<a id='depth_vs_breadth'></a>
## Depth vs Breadth 
Our query is fairly well bounded in the sense that we should be relatively certain that, from wherever we start, we shouldn't have to go much further than three or four links deep, which is approximately the average distance for a highly connected graph. A depth-first traversal would be possible if we choose to give up after a certain depth, but that is an awkward fit and not ideal for a cyclical topology (Wikipedia, of course, is).

A breadth-first search is more natural for the problem, works intuitively and is just as easy to implement.

<a id='implementation'></a>
## Implementation
Wikipedia has an easily accessible API, which certainly changes our approach. An unsupervised search would well use __BeautifulSoup__ or __libxml__ to pull out the links and construct the tree. But here, we'll use a handy package, appropriately titled 'wikipedia' (https://pypi.python.org/pypi/wikipedia/) to offload some of the overhead. This is particularly useful, as the package automatically resolves plain text to Wikipedia URLs robustly

Start and end coordinates can be input via a .json file or can be taken from the console. User-guided disambiguation is required for both coordinates only in order to validate the input; disambiguation is handled automatically once the routine begins.

I love graphs, especially when the data lends itself to one. Thankfully, there are lots of sophisticated tools for efficient storage and traversal (my favorites are Apache's TinkerPop and Node.js) -- they're too heavy duty to use here, but I highly recommend them both. 

The choice of a __queue__ for holding the current node and its path up until that point is intentional. Not only does it naturally reflect stack operations but, more importantly, __queues__ in Python are synchronized, meaning we can use them as common data stores accessible by multi-threaded processes. Although not implemented here, it would be essential for a production solution.

<a id='usage'></a>
## Usage
Simple! Just `python wikiracer.py` -- the inputs will be handled in a very short interactive session, followed by a trace as the routine continues

<a id='on_logging'></a>
## On Logging
I really do prefer to pipe the entire session to a log for safe keeping, as I think the **print** function is overused. In this demonstration, however, I've ignored the importance of keeping good log histories for the sake of expediency.

<a id='performance'></a>
## Performance
I would categorize this implementation as "slow to very slow." 

There's a good reason. Traditionally, a breadth-first search has a complexity of `O(n^(1+b))` where b is related to the connetedness of the graph, i.e. the number of related to the average number of edges per vertex. Early on I wondered if approaching the solution from both sides (start and end nodes) would only factor in as a constant, 1/2. What I failed to realize is that with an average distance of around 3.5, it actually does make a significant difference if a bimodal approach is used.

How do websites like **wikidistrict.com** return results so quickly? It's actually not that difficult to download the relevant parts of the Wikipedia corpus via open data projects like DBPedia. The project, related to the Semantic Web, is even available as an AWS instance. SPARQL is the language to query to these services and request the RDF data that makes content and meta-data available locally. Of course, this speeds things up a lot! 

<a id='results'></a>
## Results
Results from a few test cases reveals that short paths can be found quickly, even three hops away:

```
Path: ['Phase stretch transform', 'Synthetic aperture radar', 'Goodyear Aircraft Company', 'Akron, Ohio']
Time elapsed: 43.733158826828 sec
Total pages seen: 9322

Path: ['Phase stretch transform', 'Edge detection', 'Noise reduction']
Time elapsed: 5.671983003616333 sec
Total pages seen: 1127

Path: ['Fungus', 'Metabolism', 'Steroid']
Time elapsed: 15.142569065093994 sec
Total pages seen: 5135
```

Because I use sets to hold the list of candidates, at each level, the order of candidates will be randomized each time, so other paths may be found if we wanted to continue.

Some searches take considerably longer:

```
Path: ['Apocalypse Now', 'United States Military Academy', 'Oliver O. Howard', 'Toohoolhoolzote']
Time elapsed: 13923.597331047058 sec
Total pages seen: 807794
```

<a id='moving_forward'></a>
## Moving Forward
In a more sophisticated treatment of this problem, we may try to interpret each Wikipedia article and prioritize available links based on presumed similarity. That, of course, is beyond the scope of this project. I've done plenty of Wikiraces and I always find it interesting how humans structure the task and how they choose their strategy. For the same of science, I asked my roommate, a lawyer, to try to get from "Santiago Casilla," relief pitcher for the Giants, to "Door handle," which for whatever reason is always my go-to example. It's a tough one and I often use it because it's a great study on how different people see the problem in different ways. 

Certainly, Wikipedia exhibits characteristics of a small-world network, which is why so many paths end up going through common hubs. "Philosophy," for example, is super useful. When real-live humans are asked to get from one article to another, they intuitively begin by clicking their way to a broad concept, and then try to hone in on the target. The question is: how can we model the logical processes that humans, cognitively, employ to direct them what to click on next? There's actually a great database of human-generated paths that could be useful to explore (https://snap.stanford.edu/data/wikispeedia.html). 

With __a priori__ knowledge about the graph, we can eliminate the limiting factor (http requests), be kinder to Wikipedia, and be employ algorithms that aren't available when the topology of the graph is unknown to us (particularly, identifying hubs).

We should also, as always, look for multi-threading opportunities, develop a distributed infrastructure, and implement better graph storage and traversal methods.

<a id='an_aside'></a>
## An Aside
Watching the hundreds of thousands of Wikipedia article titles fly by as the algorithm performs its search is actually extremely fascinating if you're a nerd. Here are a couple of my favorites:

- https://en.wikipedia.org/wiki/Spondent_Pariter, a papal directive from the 14th century that outlawed false claims related to alchemy, though apparently if your alchemical *resumé* was in fact "true," you might well be in the clear.
- https://en.wikipedia.org/wiki/Jokes_and_Their_Relation_to_the_Unconscious, a book by Freud that attributes our affinity for humor to a core desire to brush off and ignore more serious psychological afflictions
- https://en.wikipedia.org/wiki/Gross_National_Happiness, the idea that the true value of a society is, above all else, the degree to which its people are free from suffering and have fulfilling lives, as opposed to simply producing goods or services. My college roommate and documentarian actually just finished a film on this concept (https://vimeo.com/153739983)