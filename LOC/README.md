
# documentation  LOC API 

https://libraryofcongress.github.io/data-exploration/requests.html

# 1- search for books avout Russia

Option asynchrone : http://sametmax.com/go-to-in-asyncio-considered-harmful/
Multiproc : https://docs.python.org/3/library/multiprocessing.html?highlight=worker#using-a-pool-of-workers
Sequential : obvious

https://www.loc.gov/books/?fo=json&q=russia+OR+soviet+OR+URSS+OR+russian&all=true&fa=language:english&dates=1980/2017&c=150&sp=1

results are stored in json (filename sp)

ids stred as a list on disk
paginate Throttle

# 2- get book metadata

1- Open the id list from them any id files on disk
1 bis - filter out ids that are present in filenames in the output dir
2- launch the workers on the 30k
3- by worker
	query
	callback : 
		store the xml into a file with id as filename
Take id, add /marcxml and stack the URL

https://lccn.loc.gov/2016015019/marcxml

# 3- parsing

1- list xml file in output
For each launch a worker
 - read
 - parse
 - store output in a CSV
 
