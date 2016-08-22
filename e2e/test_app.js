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
