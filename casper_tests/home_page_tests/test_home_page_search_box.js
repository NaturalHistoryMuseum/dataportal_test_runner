require('../json_report');

casper.test.begin("Check the home page search box works", function suite(test){
  casper.start(casper.cli.options['url']).then(function(){
    casper.fill('form.collection-search-form', {q: 'Mollusca'});
  }).thenClick('form.collection-search-form button', function(){
      test.assertHttpStatus(200, 'Could navigate to search page');
      test.assertMatch(
        casper.getCurrentUrl(),
        /\/dataset\/.+\/resource\/.+\?.*q=Mollusca/,
        'Destination URL contains search term'
      );
  });
  casper.run(function(){
    test.done();
  });
});