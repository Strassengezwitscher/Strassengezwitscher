var settings = require('./settings')();

casper.test.begin('Testing Map (User Frontend)', 1, function(test) {
    casper.start(settings.frontendUrl);

    casper.waitUntilVisible('sg-map', function then(){
        test.assertVisible('sg-map', 'Map is visible');
        // TODO: Add meaningful tests here.
    }, function timeout() {
        test.fail('Could not find element with tag "sg-map"');
    });

    casper.run(function(){
        test.done();
    })
});
