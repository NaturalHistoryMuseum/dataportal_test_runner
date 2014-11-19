require('../json_report');

casper.test.begin("Check we can navigate from homepage to filtered specimen view", function suite(test){
  casper.start(casper.cli.options['url']);
  casper.thenClick('a[href*="collectionCode%3AZOO"]').then(function(){
    test.assertHttpStatus(200, 'Could navigate to zoology view');
  });
  casper.thenOpen(casper.cli.options['url']);
  casper.thenClick('a[href*="collectionCode%3AZOO"]').then(function(){
    test.assertHttpStatus(200, 'Could navigate to zoology view');
  });
  casper.thenOpen(casper.cli.options['url']);
  casper.thenClick('a[href*="collectionCode%3ABOT"]').then(function(){
    test.assertHttpStatus(200, 'Could navigate to botany view');
  });
  casper.thenOpen(casper.cli.options['url']);
  casper.thenClick('a[href*="collectionCode%3AMIN"]').then(function(){
    test.assertHttpStatus(200, 'Could navigate to mineralogy view');
  });
  casper.thenOpen(casper.cli.options['url']);
  casper.thenClick('a[href*="collectionCode%3APAL"]').then(function(){
    test.assertHttpStatus(200, 'Could navigate to paleo view');
  });
  casper.thenOpen(casper.cli.options['url']);
  casper.thenClick('a[href*="collectionCode%3ABMNH%28E%29"]').then(function(){
    test.assertHttpStatus(200, 'Could navigate to entemology view');
  });
  casper.run(function(){
    test.done();
  });
});