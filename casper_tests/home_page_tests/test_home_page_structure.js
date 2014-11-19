require('../json_report');

casper.test.begin("Check that the home page contains expected elements", function suite(test){
  casper.start(casper.cli.options['url'], function(){
      test.assertHttpStatus(200, 'Home page exists');
      test.assertExists('.site-title', 'The main page title');
      test.assertExists('nav.navigation', 'The main navigation bar');
      test.assertExists('nav.account', 'The user navigation bar');
      test.assertExists('header', 'The introduction message');
      test.assertExists('div.stats', 'The stats section');
      test.assertExists('div.specimen-collection', 'The specimen collection section');
      test.assertExists('footer', 'The page footer');
      // TODO: There isn't an easy/maintainable way to test for featured datasets.
  });
  casper.run(function(){
    test.done();
  });
});