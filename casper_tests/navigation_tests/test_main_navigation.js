require('../json_report');

casper.test.begin("Check the main navigation works", function suite(test){
  var clear_url = casper.cli.options['url'].replace(/\/$/, '');
  casper.start(clear_url).thenClick('nav.navigation a[href="/dataset"]', function(){
    test.assertHttpStatus(200, 'Could navigate to dataset page');
    test.assertEquals(casper.getCurrentUrl(), clear_url + '/dataset')
  }).thenClick('nav.navigation a[href="/about"]', function(){
    test.assertHttpStatus(200, 'Could navigate to about page');
    test.assertEquals(casper.getCurrentUrl(), clear_url + '/about')
  }).thenClick('nav.navigation a[href="/"]', function(){
    test.assertHttpStatus(200, 'Could navigate back to home page');
    test.assertEquals(casper.getCurrentUrl(), clear_url + '/')
  });
  casper.run(function(){
    test.done();
  });
});