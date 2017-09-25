const request = require('request');
const cheerio = require('cheerio');
const {writeFile} = require('fs');
const {mapLimit} = require('async');

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

          var id = '';
          if (orga.attr('rdf:about')) {
            id = orga.attr('rdf:about').match(/http:\/\/www\.idref\.fr\/(.*?)\/id\/?/);
            id = id ? id[1] : '';
          }
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
      	if ($(this).children.length > 0 && $(this).children[0] ){
          var lang = $(this).attr('xml:lang')
          if (lang.trim() === 'en')
            result.abstract_en = $(this).children[0].data;
          else
          	result.abstract_fr = $(this).children[0].data;
        }
      });

      result.contributor_ids = []
      result.contributor_names = []
  
      $('dcterms\\:contributor').each(function (i,n) {
        var orga = $(this).children('foaf\\:Organization').first()
        var id = '';
        if (orga.attr('rdf:about')) {
          id = orga.attr('rdf:about').match(/http:\/\/www\.idref\.fr\/(.*?)\/id\/?/);
          id = id ? id[1] : '';
        }
        if (orga.children.length > 0){
           var name = orga.children().first().text();
           result.contributor_names.push(name)
           result.contributor_ids.push(id)
        }

      });

      result.subjects = []
      $('dc\\:subject').each(function (i,s) {
        result.subjects.push($(s).text().trim())
      })
      result.subjects = result.subjects.filter(e => e)

      if (cb) return cb(null, result);
    }
    if (cb) return cb(err);
  });
}

mapLimit(
  theses,
  10,
  function(these, cb) {
    console.log(`process these ${these.num}`)
    downloadParseThese(`http://www.theses.fr/${these.num}.xml`, (err,data) =>{
      if (err){
        console.log("bou!!!!")
        return
      }
      setTimeout(_ => cb(null,Object.assign({},these, data)), 500)
      
    });
  },
  function(err, data){
    if (err){
      console.log("WARNING", err)
    }
    writeFile('theses_metadata_abstract_keywords.json',JSON.stringify(data),'utf8');
  }
);

