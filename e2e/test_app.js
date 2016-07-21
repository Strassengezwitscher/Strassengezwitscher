var settings = require('./settings')();

casper.test.begin('Testing Strassengezwitscher App (User Frontend)', 1, function(test) {
    casper.start(settings.frontendUrl);

    casper.then(function() {
        test.assertTitle('Strassengezwitscher', 'Strassengezwitscher has correct title');
    });

    casper.run(function(){
        test.done();
    })
});
