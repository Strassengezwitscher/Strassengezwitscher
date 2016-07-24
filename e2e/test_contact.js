var settings = require('./settings')();

casper.test.begin('Testing Contact (User Frontend fields available)', 11, function(test) {
    casper.start(settings.contactUrl);

    casper.waitUntilVisible('sg-contact', function then(){
        test.assertVisible('sg-contact', 'Contact form is visible');
        test.assertExists('#contact-form', 'The contact form is available');
        test.assertNotVisible('#contact-error-message', 'Error message not visible');
        test.assertExists('input#contact-name','Input field for name');
        test.assertExists('input#contact-email[type=email]','Input field for email');
        test.assertExists('input#contact-subject','Input field for subject');
        test.assertExists('textarea#contact-message','Textarea for message');
        test.assertExists('input#contact-journalist[type=checkbox]','Input Checkbox for journalist');
        test.assertExists('input#contact-confidential[type=checkbox]','Input Checkbox for confidential');
        test.assertExists('input#contact-file[type=file]','File Input for files');
        test.assertExists('button#contact-submit-button[type=submit]','Submit button exists')

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
