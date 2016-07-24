var settings = require('./settings')();

casper.test.begin('Testing Contact (User Frontend initial)', 3, function(test) {
    casper.start(settings.contactUrl);

    casper.waitUntilVisible('sg-contact', function then(){
        test.assertVisible('sg-contact', 'Contact form is visible');
        test.assertExists('#contact-form', 'The contact form is available');
        test.assertNotVisible('#contact-error-message', 'Error message not visible');
    }, function timeout() {
        test.fail('Could not find element with tag "sg-contact"');
    });

    casper.run(function(){
        test.done();
    })
});


casper.test.begin('Testing Contact (Name max length)', 3, function(test) {
    casper.start(settings.contactUrl);

    casper.waitUntilVisible('sg-contact', function then(){
        this.sendKeys('#contact-name', 'Peter');
        test.assertSelectorHasText('#contact-name', 'Peter');
    }, function timeout() {
        test.fail('Could not find element with tag "sg-contact"');
    });

    casper.waitUntilVisible('sg-contact', function then(){
        this.sendKeys('#contact-name', 'PeterPeterPeterPeterPeterPeterPeterPeterPeterPeterZuViel');
        test.assertSelectorDoesntHaveText('#contact-name', 'PeterPeterPeterPeterPeterPeterPeterPeterPeterPeterZuViel');
        test.assertSelectorHasText('#contact-name', 'PeterPeterPeterPeterPeterPeterPeterPeterPeterPeter');
    }, function timeout() {
        test.fail('Could not find element with tag "sg-contact"');
    });

    casper.run(function(){
        test.done();
    })
});

