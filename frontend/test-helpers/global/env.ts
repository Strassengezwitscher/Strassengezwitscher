// This lets systemjs.conf.js knows how to load the module during testing
((global) => {
    console.log('asdgafgdfgsd');
    global.ENV = "testing";
})(this);
