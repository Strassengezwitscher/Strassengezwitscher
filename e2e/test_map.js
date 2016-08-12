var settings = require('./settings')();

casper.test.begin('Testing Map (User Frontend)', 1, function(test) {
    casper.start(settings.frontendUrl);

    casper.waitUntilVisible('cg-map', function then(){
        test.assertVisible('cg-map', 'Map is visible');
        // TODO: Add meaningful tests here.
    }, function timeout() {
        test.fail('Could not find element with tag "cg-map"');
    });

    casper.run(function(){
        test.done();
    })
});
