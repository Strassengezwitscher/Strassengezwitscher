var settings = require('./settings')();

casper.test.begin('Testing Crowdgezwitscher App (User Frontend)', 1, function(test) {
    casper.start(settings.frontendUrl);

    casper.then(function() {
        test.assertTitle('Crowdgezwitscher', 'Crowdgezwitscher has correct title');
    });

    casper.run(function(){
        test.done();
    })
});

casper.test.begin('Testing correct display for toolbar on small ', 5, function(test) {
    casper.start(settings.frontendUrl);
    casper.viewport(600, 1024);
    casper.waitUntilVisible('cg-app', function then(){
        test.assertVisible('.hide-on-med-and-up', 'Only on small screen');
        test.assertNotVisible('.md-button', 'Buttons for larger screens are not visible');
        test.assertVisible('#small-screen-menu', 'Menu for small screen');
        this.click('#small-screen-menu');
        test.assertVisible('#contact-button-small', 'Contact link visible');
        test.assertVisible('#imprint-button-small', 'Imprint link visible');

    }, function timeout() {
        test.fail('Could not find element with tag "cg-app"');
    });
    casper.run(function(){
        test.done();
    })
});

casper.test.begin('Testing correct display for toolbar on different sizes ', 3, function(test) {
    casper.start(settings.frontendUrl);
    casper.viewport(1200, 1024);
    casper.waitUntilVisible('cg-app', function then(){
        test.assertVisible('.hide-on-small-only', 'Only on larger screen');
        test.assertVisible('#contact-button-large', 'Contact button visible');
        test.assertVisible('#imprint-button-large', 'Imprint button visible');
    }, function timeout() {
        test.fail('Could not find element with tag "cg-app"');
    });
    casper.run(function(){
        test.done();
    })
});

casper.test.begin('Testing routing of toolbar', 3, function(test) {
    casper.start(settings.frontendUrl);

    casper.waitUntilVisible('cg-app', function then(){
        this.click('#imprint-button-large');
        test.assertUrlMatch(/.*\/imprint/,'now on page imprint');
        this.click('#contact-button-large');
        test.assertUrlMatch(/.*\/contact/,'now on page contact');
        this.click('#map-link');
        test.assertUrlMatch(/.*\/map/,'now on page map');
    });

    casper.run(function(){
        test.done();
    })
});