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

      $('marcrel\\:dgg').each(function (i,n) {
          var orga = $(this).children('foaf\\:Organization').first()
          var id = orga.attr('rdf:about').match(/http:\/\/www\.idref\.fr\/(.*?)\/id\/?/);
          id = id ? id[1] : '';
          if (orga.children.length > 0){
             var name = orga.children().first().text();
          }
          if (i === 0){
            // assuming établissement de soutenance
            result.soutenance_id = id;
            result.soutenvance_name = name;
          }
          if (i === 1){
            // assuming école doctorale
            result.ecole_doctorale_id = id;
            result.ecole_doctorale_name = name;  
          }
        });

      $('dcterms\\:abstract').each(function (i,n) {
      	if ($(this).children.length > 0){
          var lang = $(this).attr('xml:lang')
        	result.abstract[lang.trim() !== '' ? lang : 'fr'] = $(this).children[0].data;
        }
      });

      result.contributor_ids = []
      result.contributor_names = []
  
      $('dcterms\\:contributor').each(function (i,n) {
        var orga = $(this).children('foaf\\:Organization').first()
        var id = orga.attr('rdf:about').match(/http:\/\/www\.idref\.fr\/(.*?)\/id\/?/);
        id = id ? id[1] : '';
        if (orga.children.length > 0){
           var name = orga.children().first().text();
           result.contributor_names.push(name)
           result.contributor_ids.push(id)
        }

      });

      result.subject = Array($('dc\\:subject').map(function (i,s) {
        return $(s).text().trim()
      })).filter(e => e)

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
