require('../json_report');

/**
 * _parse_number
 *
 * Parse a string representation of a number which may contain thousand
 * separator commas and units.
 *
 * If the number is not parseable, return False.
 */
function _parse_number(number) {
  number = number.replace(/,|\s/g, '');
  var match = number.match(/^([0-9.]+)(K|M)?$/i)
  if (match) {
    var result = parseFloat(match[1]);
    if (typeof(match[2]) !== 'undefined') {
      var unit = match[2].toLowerCase();
      if (unit == 'm') {
        result = result * 1000000;
      } else if (unit == 'k') {
        result = result * 1000;
      }
    }
    return result;
  } else {
    return false;
  }
}

casper.test.begin("Check that the home page counters contain sensible values", function suite(test){
  casper.start(casper.cli.options['url'], function(){
    var num = _parse_number(this.getHTML('div.stats li a[href="/about/statistics/records"] span'));
    test.assert((typeof(num) == 'number'), "Records is a number");
    test.assert(num > 1000000, "There is more than 1 million records");
    test.assert(num < 100000000, "There is less than 100 million records");
  });
  casper.then(function(){
    var num = _parse_number(this.getHTML('div.stats li a[href="/dataset"] span'));
    test.assert((typeof(num) == 'number'), "Datasets is a number");
    test.assert(num > 4, "There is more than 4 datasets");
    test.assert(num < 100000, "There is less than 100 thousand datasets");
  });
  casper.then(function(){
    var num = _parse_number(this.getHTML('div.stats li a[href="/about/statistics/contributors"] span'));
    test.assert((typeof(num) == 'number'), "Contributors is a number");
    test.assert(num >= 1, "There is at least one contributor");
    test.assert(num < 100000, "There is less than 100 thousand contributors");
  });
  casper.then(function(){
    var num = _parse_number(this.getHTML('div.collection-stats li a[href*="collectionCode%3AZOO"] span'));
    test.assert((typeof(num) == 'number'), "Zoology records is a number");
    test.assert(num > 500000, "There is at least 500,000 zoology records");
    test.assert(num < 100000000, "There is less than 100 million zoology records");
  });
  casper.then(function(){
    var num = _parse_number(this.getHTML('div.collection-stats li a[href*="collectionCode%3ABOT"] span'));
    test.assert((typeof(num) == 'number'), "Botany records is a number");
    test.assert(num > 200000, "There is at least 200,000 botany records");
    test.assert(num < 100000000, "There is less than 100 million botany records");
  });
  casper.then(function(){
    var num = _parse_number(this.getHTML('div.collection-stats li a[href*="collectionCode%3APAL"] span'));
    test.assert((typeof(num) == 'number'), "Paleo records is a number");
    test.assert(num > 200000, "There is at least 200,000 paleo records");
    test.assert(num < 100000000, "There is less than 100 million paleo records");
  });
  casper.then(function(){
    var num = _parse_number(this.getHTML('div.collection-stats li a[href*="collectionCode%3AMIN"] span'));
    test.assert((typeof(num) == 'number'), "Mineralogy records is a number");
    test.assert(num > 200000, "There is at least 200,000 mineralog records");
    test.assert(num < 100000000, "There is less than 100 million mineralog records");
  });
  casper.then(function(){
    var num = _parse_number(this.getHTML('div.collection-stats li a[href*="collectionCode%3ABMNH%28E%29"] span'));
    test.assert((typeof(num) == 'number'), "Entomology records is a number");
    test.assert(num > 200000, "There is at least 200,000 entomology records");
    test.assert(num < 100000000, "There is less than 100 million entomology records");
  });
  casper.run(function(){
    test.done();
  });
});