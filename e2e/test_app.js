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

casper.test.begin('Testing correct display for toolbar on small screens', 7, function(test) {
    casper.start(settings.frontendUrl);
    casper.viewport(600, 1024);
    casper.waitUntilVisible('cg-app', function then(){
        this.clickLabel('Blog');
        test.assertUrlMatch(/.*\/blog/,'now on page: blog');

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

        this.click('#toolbar-menu-button-small');
        this.clickLabel('Spenden');
        casper.waitForPopup(/.*paypal.me\/strassengezwitscher/, function(){
            test.assertEquals(this.popups.length, 1);
        }, function timeout() {
            test.fail('No new page for donation opened');
        });
        casper.withPopup(/.*paypal.me\/strassengezwitscher/, function() {
            test.assertUrlMatch(/.*paypal.me\/strassengezwitscher/,'now on page: donation');
        });
    }, function timeout() {
        test.fail('Could not find element with tag "cg-app"');
    });
    casper.run(function(){
        test.done();
    })
});


casper.test.begin('Testing correct display for toolbar on medium screens', 7, function(test) {
    casper.start(settings.frontendUrl);
    casper.viewport(900, 1024);
    casper.waitUntilVisible('cg-app', function then(){
        this.clickLabel('Blog');
        test.assertUrlMatch(/.*\/blog/,'now on page: blog');

        this.clickLabel('Impressum');
        test.assertUrlMatch(/.*\/imprint/,'now on page: imprint');

        this.clickLabel('Kontakt');
        test.assertUrlMatch(/.*\/contact/,'now on page: contact');

        this.clickLabel('CrowdgezwitscherMap');
        test.assertUrlMatch(/.*\/map/,'now on page map');

        this.click('#toolbar-menu-button-medium');
        this.clickLabel('Über uns');
        test.assertUrlMatch(/.*\/about/,'now on page about');

        this.click('#toolbar-menu-button-medium');
        this.clickLabel('Spenden');
        casper.waitForPopup(/.*paypal.me\/strassengezwitscher/, function(){
            test.assertEquals(this.popups.length, 1);
        }, function timeout() {
            test.fail('No new page for donation opened');
        });
        casper.withPopup(/.*paypal.me\/strassengezwitscher/, function() {
            test.assertUrlMatch(/.*paypal.me\/strassengezwitscher/,'now on page: donation');
        });
    }, function timeout() {
        test.fail('Could not find element with tag "cg-app"');
    });
    casper.run(function(){
        test.done();
    })
});

casper.test.begin('Testing correct display for toolbar on larger screens ', 7, function(test) {
    casper.start(settings.frontendUrl);
    casper.viewport(1200, 1024);
    casper.waitUntilVisible('cg-app', function then(){
        this.clickLabel('Blog');
        test.assertUrlMatch(/.*\/blog/,'now on page: blog');

        this.clickLabel('Impressum');
        test.assertUrlMatch(/.*\/imprint/,'now on page: imprint');

        this.clickLabel('Kontakt');
        test.assertUrlMatch(/.*\/contact/,'now on page: contact');

        this.clickLabel('Über uns');
        test.assertUrlMatch(/.*\/about/,'now on page: about');

        this.clickLabel('CrowdgezwitscherMap');
        test.assertUrlMatch(/.*\/map/,'now on page: map');

        this.clickLabel('Spenden');
        casper.waitForPopup(/.*paypal.me\/strassengezwitscher/, function(){
            test.assertEquals(this.popups.length, 1);
        }, function timeout() {
            test.fail('No new page for donation opened');
        });
        casper.withPopup(/.*paypal.me\/strassengezwitscher/, function() {
            test.assertUrlMatch(/.*paypal.me\/strassengezwitscher/,'now on page: donation');
        });

    }, function timeout() {
        test.fail('Could not find element with tag "cg-app"');
    });
    casper.run(function(){
        test.done();
    })
});
