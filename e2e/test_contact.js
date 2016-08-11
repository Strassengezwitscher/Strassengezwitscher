var settings = require('./settings')();

casper.test.begin('Testing Contact (User Frontend fields available)', 12, function(test) {
    casper.start(settings.contactUrl);

    casper.waitUntilVisible('cg-contact', function then(){
        test.assertVisible('cg-contact', 'Contact form is visible');
        test.assertExists('#contact-form', 'The contact form is available');
        test.assertNotVisible('#contact-error-message', 'Error message not visible');
        test.assertExists('input#contact-name','Input field for name');
        test.assertExists('input#contact-email[type=email]','Input field for email');
        test.assertExists('input#contact-subject','Input field for subject');
        test.assertExists('textarea#contact-message','Textarea for message');
        test.assertExists('input#contact-journalist[type=checkbox]','Input Checkbox for journalist');
        test.assertExists('input#contact-confidential[type=checkbox]','Input Checkbox for confidential');
        test.assertExists('input#contact-file[type=file]','File Input for files');
        test.assertExists('button#contact-submit-button[type=submit]:disabled','Disabled submit button exists')
        test.assertExists('#contact-recaptcha','Google recaptcha div exists')

    }, function timeout() {
        test.fail('Could not find element with tag "cg-contact"');
    });

    casper.run(function(){
        test.done();
    })
});


casper.test.begin('Testing Contact (Name max length)', 3, function(test) {
    casper.start(settings.contactUrl);

    casper.waitUntilVisible('cg-contact', function then(){
        this.sendKeys('#contact-name', 'Peter');
        test.assertSelectorHasText('#contact-name', 'Peter');
        this.sendKeys('#contact-name', 'PeterPeterPeterPeterPeterPeterPeterPeterPeterPeterZuViel');
        test.assertSelectorDoesntHaveText('#contact-name', 'PeterPeterPeterPeterPeterPeterPeterPeterPeterPeterZuViel');
        test.assertSelectorHasText('#contact-name', 'PeterPeterPeterPeterPeterPeterPeterPeterPeterPeter');
    }, function timeout() {
        test.fail('Could not find element with tag "cg-contact"');
    });
    casper.run(function(){
        test.done();
    })
});


casper.test.begin('Testing Contact (Submission disabled)', 4, function(test) {
    casper.start(settings.contactUrl);

    casper.waitUntilVisible('cg-contact', function then(){
        // test case for disabled button with missing subject
        this.sendKeys('#contact-message','Tolle Nachricht');
        test.assertExists('button#contact-submit-button:disabled', 'disabled button, missing subject');
        // test case for disabled button with missing message
        this.sendKeys('#contact-message','', {reset : true});
        this.sendKeys('#contact-subject','Betreff');
        test.assertExists('button#contact-submit-button:disabled', 'disabled button, missing message');
        // test case for enabled button with subject and message, rest empty
        this.sendKeys('#contact-subject','Betreff');
        this.sendKeys('#contact-message','Tolle Nachricht');
        test.assertExists('button#contact-submit-button:disabled', 'disabled button, missing verified captcha')
        // test case for disabled button with wrong email
        this.sendKeys('#contact-email','this@doesNotWork');
        test.assertExists('button#contact-submit-button:disabled', 'disabled button, wrong email');
    }, function timeout() {
        test.fail('Could not find element with tag "cg-contact"');
    });


    casper.run(function(){
        test.done();
    })
});
