const _ = require('lodash');
const {writeFile} = require('fs');

let theses = require ('./theses_metadata.json');
theses = _(theses).flatten().value()
theses = _.uniqBy(theses, d => d.id)


writeFile('theses_metadata.json',JSON.stringify(theses),'utf8');