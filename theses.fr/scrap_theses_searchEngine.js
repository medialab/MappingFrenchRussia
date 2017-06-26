const request = require('request');
const Url  = require('url');
const querystring = require('querystring');
const fs = require('fs')
const async = require('async')
const _ = require('lodash')
const {parse} = require('csv')


const EXTRACT = "ids";//"searchEngine"



function downloadAllDocuments(url, query, documents, cb){

	
	console.log(`new request to ${Url.format({host:url,query:query})}`)
	request({method:'GET',url:url,qs:query}, (err,response,data) => {
		if (response && response.statusCode == 200){
			requestData = JSON.parse(data)
	    	documents = documents.concat(requestData.response.docs)
	    	console.log(`response with start=${requestData.response.start} returned ${requestData.response.docs.length} docs`);
	    	if (requestData.response.start + requestData.response.docs.length  < requestData.response.numFound){
	    		query.start = requestData.response.start + requestData.response.docs.length
	    		downloadAllDocuments(url, query, documents, cb);
	    	}
	    	else
	    		//done
	    		cb(documents);
      	} else {
	        console.log(err, response)
	        console.log(data)
      	}
		
	});
}

async.waterfall([
	(next)=>{
		// List thesis containing some keywords
		// let url = 'http://www.theses.fr/?q=russe;&format=json'
		// http://www.theses.fr/?q=soviet;&format=json
		// http://www.theses.fr/?q=urss;&format=json

		if (EXTRACT === "searchEngine"){
			const keywords = ['russe', 'russie','soviet', 'urss']
			next(null, keywords.map(
			 	keyword => `http://www.theses.fr/?q=&zone1=titreRAs&val1=${keyword}&op1=OR&zone2=motCleRAs&val2=${keyword}&op2=OR&zone3=abstracts&val3=${keyword}&format=json`
		 	));
		}
		// List thesis from IDs list
		// load ids list
		else
			if (EXTRACT === "ids"){
				fs.readFile('all_theses_ids.csv', 'utf8', 
					(err,data) => next(null,data.split('\n').map(id => `http://www.theses.fr/?q=${id}&format=json`)));
			}
	},
	(urls,next) => {
		async.mapLimit(urls, 10,(url,next) =>{
			url = Url.parse(url, true)
			let query = url.query
			url = url.protocol+'//'+url.host
			//url.query = querystring.parse(url.query)
			query.start = 0

			downloadAllDocuments(url, query, [], data =>{
				next(null,data)	
			})
		}, (err, data) => {
			// merge and deduplicate docs
			data = _.uniqBy(_(data).flatten().value(), d => d.id)
			fs.writeFile('theses_metadata.json',JSON.stringify(data),'utf8');	
			next(null);
		})
	}
])

		
