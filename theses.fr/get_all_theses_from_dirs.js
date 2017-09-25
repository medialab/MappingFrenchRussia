const _ = require('lodash');
const {mapLimit} = require('async');
const {parse} = require('csv');
const request = require('request');
const cheerio = require('cheerio');
const {readFile, writeFile} = require('fs');

readFile('./theses_metadata.csv', 'utf-8', function(err, data){
  if (err){
    return console.log("ERROR reading csv", err);
  }
  parse(data, {columns: true}, extract_dirs);
});

function extract_dirs(err, data){
  if (err){
    return console.log("ERROR parsing csv", err);
  }
  mapLimit(
    uniqDirs = _.uniq(_(data.map(d => d.directeurThesePPN_correct.split(',').map(e => e.trim()))).flatten().value().filter(d => d)),
    10,
    function(dir, cb) {
      if (dir.length === 8)
        dir = '0' + dir
      request('http://www.theses.fr/' + dir + '.xml', function(err, res, body){
        if (err)
          return cb(err);
        const $ = cheerio.load(body, {xmlMode: true});
        const theses_ids = $("bibo\\:Thesis").filter(function(i, t){
            return $(t).find("marcrel\\:ths foaf\\:Person")
              .toArray()
              .some( e => $(e).attr("rdf:about") === 'http://www.theses.fr/' + dir + '/id');
          }).map((i, e) => $(e).attr("rdf:about").replace(new RegExp(/http:\/\/www\.theses\.fr\/(.*?)\/id/), '$1'))
          .toArray()
        if (theses_ids.length === 0)
          console.log( dir )
        cb(null, theses_ids);
      });
    },
    function(err, data){
      if (err){
        console.log("WARNING", err)
      }
      console.log(data.length,_.countBy(data.map(d => d.length)))
      writeFile('all_theses_ids.csv', _.uniq(_(data).flatten().value()).join('\n'), 'utf8');
    }
  );
  
}
