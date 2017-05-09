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
    uniqDirs = _.uniq(_(data.map(d => d.directeurThesePpn.split(','))).flatten().value().filter(d => d)),
    10,
    function(dir, cb) {
      request('http://www.theses.fr/' + dir + '.xml', function(err, res, body){
        if (err)
          return cb(err);
        const $ = cheerio.load(body, {xmlMode: true});
        cb(null, $("bibo\\:Thesis").filter(function(i, t){
            return $(t).find("marcrel\\:ths foaf\\:Person")
              .toArray()
              .some( e => $(e).attr("rdf:about") === 'http://www.theses.fr/' + dir + '/id');
          }).map((i, e) => $(e).attr("rdf:about").replace(/^.*\.fr\/(^\/)+\/id/, '$1'))
          .toArray()
        );
      });
    },
    function(err, data){
      if (err){
        console.log("WARNING", err)
      }
      writeFile('all_theses_ids.csv', _.uniq(_(data).flatten().value()).join('\n'), 'utf8');
    }
  );
  
}
