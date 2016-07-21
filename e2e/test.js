casper.test.begin('Testing Google', 1, function(test){
    casper.start('http://localhost:8000/');

    casper.then(function(){
        test.assertTitle('Google', 'Google has correct title');
    });

    casper.wait(100, function(){
        test.assertTitle('Strassengezwitscher', 'SG has correct title2');
    });

    casper.run(function(){
        test.done();
    })
});

casper.test.begin("Hello, Test!", 1, function(test) {
  test.assert(true);
  test.done();
});
