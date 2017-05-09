const request = require('request');
const cheerio = require('cheerio');
const {writeFile} = require('fs');

let theses = require ('./theses_metadata.json');

function downloadParseThese(xmlURL, cb) {

	console.log(`fetching ${xmlURL}`)
  request(xmlURL, function (err, res, body) {
    if (!err && res.statusCode === 200) {
      console.log(`got ${xmlURL}`)
      var $ = cheerio.load(body, {xmlMode: true});

      var result = {
        abstract: {fr: '', en: ''}
      };

      result.title = $('dc\\:title').text();

      [].slice.call($('dcterms\\:abstract')).forEach(function (n) {
      	if (n.children.length > 0)
        	result.abstract[n.attribs['xml:lang'].trim() !== '' ? n.attribs['xml:lang'] : 'fr'] = n.children[0].data;
      });

      result.subject = [].slice.call($('dc\\:subject')).map(function (s) {
        return $(s).text().trim()
      }).filter(e => e)

      if (cb) return cb(null, result);
    }
    if (cb) return cb(err);
  });
}

function hydrateThesis(thesis, i, cb){
	console.log(`process these ${i}`)
	downloadParseThese(`http://www.theses.fr/${thesis[i].num}.xml`, (err,data) =>{
		if (err){
			console.log("bou!!!!")
			return
		}
		thesis[i].abstract_fr = data.abstract.fr
		thesis[i].abstract_en = data.abstract.en
		thesis[i].subjects = data.subject
		if (i < thesis.length - 1)
			setTimeout( () => hydrateThesis(thesis, i+1, cb), 500)
		else
			cb(thesis)
	})

}

hydrateThesis(theses,0, data => {
	writeFile('theses_metadata_abstract_keywords.json',JSON.stringify(data),'utf8');
})
