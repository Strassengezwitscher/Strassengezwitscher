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

casper.test.begin('Testing correct display for toolbar on small ', 4, function(test) {
    casper.start(settings.frontendUrl);
    casper.viewport(600, 1024);
    casper.waitUntilVisible('cg-app', function then(){
        this.click('#toolbar-menu-button-small');
        this.clickLabel('Impressum');
        test.assertUrlMatch(/.*\/imprint/,'now on page imprint');
        this.click('#toolbar-menu-button-small');
        this.clickLabel('Kontakt');
        test.assertUrlMatch(/.*\/contact/,'now on page contact');
        this.clickLabel('CrowdgezwitscherMap');
        test.assertUrlMatch(/.*\/map/,'now on page map');
        this.click('#toolbar-menu-button-small');
        this.clickLabel('Über uns');
        test.assertUrlMatch(/.*\/about/,'now on page about');
    }, function timeout() {
        test.fail('Could not find element with tag "cg-app"');
    });
    casper.run(function(){
        test.done();
    })
});

casper.test.begin('Testing correct display for toolbar on different sizes ', 4, function(test) {
    casper.start(settings.frontendUrl);
    casper.viewport(1200, 1024);
    casper.waitUntilVisible('cg-app', function then(){
        this.clickLabel('Impressum');
        test.assertUrlMatch(/.*\/imprint/,'now on page imprint');
        this.clickLabel('Kontakt');
        test.assertUrlMatch(/.*\/contact/,'now on page contact');
        this.clickLabel('Über uns');
        test.assertUrlMatch(/.*\/about/,'now on page about');
        this.clickLabel('CrowdgezwitscherMap');
        test.assertUrlMatch(/.*\/map/,'now on page map');
    }, function timeout() {
        test.fail('Could not find element with tag "cg-app"');
    });
    casper.run(function(){
        test.done();
    })
});
