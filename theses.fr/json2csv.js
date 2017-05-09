const {stringify} = require('csv');
const moment = require('moment');
const {writeFile} = require('fs');
const ddc = require('./ddc.json');

let theses = require ('./theses_metadata_abstract_keywords.json');

theses = theses.map(t => {
	t.dateMaj = moment(t.dateMaj).format('YYYY-MM-DD');
	t.dateInsert = moment(t.dateInsert).format('YYYY-MM-DD');
	t.sujDatePremiereInscription = moment(t.sujDatePremiereInscription).format('YYYY-MM-DD');
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
		writeFile('theses_metadata.csv', csv, 'utf8',
			err => {
				if (err)
					console.log(`Error while writing file ${err}`)
				else
					console.log('file wrote')
			})
);
