const {stringify} = require('csv');
const moment = require('moment');
const {writeFile} = require('fs');
const ddc = require('./ddc.json');

let theses = require ('./theses_metadata_abstract_keywords_25_09.json');

theses = theses.map(t => {
	if (!t.ecole_doctorale_id)
		t.ecole_doctorale_id = ''
	if (!t.ecole_doctorale_name)
		t.ecole_doctorale_name = ''
	t.dateMaj = moment(t.dateMaj).format('YYYY-MM-DD');
	t.dateInsert = moment(t.dateInsert).format('YYYY-MM-DD');
	t.sujDatePremiereInscription = moment(t.sujDatePremiereInscription).format('YYYY-MM-DD');
	if (t.abstract)
		delete t.abstract
	if (t.oaiSetSpec){
		t.oaiSetSpec = t.oaiSetSpec.map(oai => {
			let label = ddc.find(d => d.oaiSetSpec === oai)
			if (label && label != 'null') 
				return label["label"];
			else
				return oai
		})
	}
	return t;
});

stringify(theses,
	{
		header:true,
		formatters:{
			object: o => Array.isArray(o) ? o.join(',') : 'warning objects !'
		}
	},
	(err,csv) => 
		writeFile('theses_metadata_25_09.csv', csv, 'utf8',
			err => {
				if (err)
					console.log(`Error while writing file ${err}`)
				else
					console.log('file wrote')
			})
);
