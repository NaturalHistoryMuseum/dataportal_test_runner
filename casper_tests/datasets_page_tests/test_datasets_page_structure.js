require('../json_report');

/**
 * _test_facet applies tests to check that:
 * - A given facet block exists;
 * - There are a least a certain number of entries in the block
 */
function _test_facet(facet, min, test){
  var match = 'ul.nav-facet li.nav-item a[href^="/dataset?' + facet + '="]';
  // Todo: This is not ideal, we test the existence of an actual facet rather
  // than the block.
  test.assertExists(match, facet + ' facet block exists');
  test.assertTrue(
    casper.getElementsInfo(match).length >= min,
    'There are at least ' + min + ' ' + facet + ' in the facet block'
  );
}

casper.test.begin("Check that the datasets page contains expected elements", function suite(test){
  casper.start(casper.cli.options['url'] + '/dataset', function(){
    test.assertHttpStatus(200, 'Datasets page exists');
    test.assertExists('table.package-list', 'Dataset list is present');
    test.assertTrue(
      casper.getElementsInfo('table.package-list tr').length >= 4,
      'There are at least 4 datasets displayed'
    );
    _test_facet('author', 2, test);
    _test_facet('tags', 2, test);
    _test_facet('res_format', 2, test);
    _test_facet('creator_user_id', 2, test);
  });
  casper.run(function(){
    test.done();
  });
});