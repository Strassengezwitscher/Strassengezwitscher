var settings = require('./settings')();

casper.test.begin('Testing Contact (User Fronted)', 2, function(test) {
    casper.start(settings.contactUrl);

    casper.waitUntilVisible('sg-contact', function then(){
        test.assertVisible('sg-contact', 'Contact form is visible');
        test.assertTextExists('Insert contact form here.', 'Does show wip text');
    }, function timeout() {
        test.fail('Could not find element with tag "sg-contact"');
    });

    casper.run(function(){
        test.done();
    })
});
