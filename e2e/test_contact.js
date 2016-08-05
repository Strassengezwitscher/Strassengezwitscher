var settings = require('./settings')();

casper.test.begin('Testing Contact (User Frontend fields available)', 11, function(test) {
    casper.start(settings.contactUrl);

    casper.waitUntilVisible('sg-contact', function then(){
        test.assertVisible('sg-contact', 'Contact form is visible');
        test.assertExists('#contact-form', 'The contact form is available');
        test.assertNotVisible('#contact-error-message', 'Error message not visible');
        test.assertExists('input#contact-name-input','Input field for name');
        test.assertExists('input#contact-email-input[type=email]','Input field for email');
        test.assertExists('input#contact-subject-input','Input field for subject');
        test.assertExists('textarea#contact-message-input','Textarea for message');
        test.assertExists('input#contact-journalist-input[type=checkbox]','Input Checkbox for journalist');
        test.assertExists('input#contact-confidential-input[type=checkbox]','Input Checkbox for confidential');
        test.assertExists('input#contact-file[type=file]','File Input for files');
        test.assertExists('button#contact-submit-button[type=submit]:disabled','Disabled submit button exists')

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
        this.sendKeys('#contact-name-input', 'Peter');
        test.assertSelectorHasText('#contact-name-input', 'Peter');
        this.sendKeys('#contact-name-input', 'PeterPeterPeterPeterPeterPeterPeterPeterPeterPeterZuViel');
        test.assertSelectorDoesntHaveText('#contact-name-input', 'PeterPeterPeterPeterPeterPeterPeterPeterPeterPeterZuViel');
        test.assertSelectorHasText('#contact-name-input', 'PeterPeterPeterPeterPeterPeterPeterPeterPeterPeter');
    }, function timeout() {
        test.fail('Could not find element with tag "sg-contact"');
    });
    casper.run(function(){
        test.done();
    })
});


casper.test.begin('Testing Contact (Submission enabled/disabled)', 5, function(test) {
    casper.start(settings.contactUrl);

    casper.waitUntilVisible('sg-contact', function then(){
        // test case for disabled button with missing subject
        this.sendKeys('#contact-message-input','Tolle Nachricht');
        test.assertExists('button#contact-submit-button:disabled', 'disabled button, missing subject');
        // test case for disabled button with missing message
        this.sendKeys('#contact-message-input','', {reset : true});
        this.sendKeys('#contact-subject-input','Betreff');
        test.assertExists('button#contact-submit-button:disabled', 'disabled button, missing message');
        // test case for enabled button with subject and message, rest empty
        this.sendKeys('#contact-subject-input','Betreff');
        this.sendKeys('#contact-message-input','Tolle Nachricht');
        test.assertExists('button#contact-submit-button:enabled', 'enabled button')
        // test case for disabled button with wrong email
        this.sendKeys('#contact-email-input','this@doesNotWork');
        test.assertExists('button#contact-submit-button:disabled', 'disabled button, wrong email');
        // test case for enabled button with subject and message and correct email
        this.sendKeys('#contact-subject-input','Betreff');
        this.sendKeys('#contact-message-input','Tolle Nachricht');
        this.sendKeys('#contact-email-input','this@doesWork.com', {reset : true});
        test.assertExists('button#contact-submit-button:enabled', 'enabled button')
    }, function timeout() {
        test.fail('Could not find element with tag "sg-contact"');
    });


    casper.run(function(){
        test.done();
    })
});
