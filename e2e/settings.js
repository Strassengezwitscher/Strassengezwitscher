module.exports = function(options) {
    var options = options || {}
    options.viewportWidth = options.hasOwnProperty('viewportWidth') ? options.viewportWidth : 1280;
    options.viewportHeight = options.hasOwnProperty('viewportHeight') ? options.viewportHeight : 1024;
    options.timeout = options.hasOwnProperty('timeout') ? options.timeout : 10000;
    options.enableBrowserLog = options.hasOwnProperty('enableBrowserLog') ? options.enableBrowserLog : false;

    var hostUrl = 'http://localhost:8000/map/';

    function init() {
        setViewportSize(options.viewportWidth, options.viewportHeight);
        setWaitTimeout(options.timeout);
        setBrowserLog(options.enableBrowserLog);
    };

    function setViewportSize(width, height) {
         var viewportWidth = width;
         var viewportHeight = height;

         casper.echo('Current viewport size is ' + viewportWidth + 'x' + viewportHeight + '.', 'INFO');

         casper.options.viewportSize = {
             width: viewportWidth,
             height: viewportHeight
         };
    };

    function setWaitTimeout(waitTimeout) {
         casper.echo('Default waitFor timeout is ' + waitTimeout + 'ms.', 'INFO');
         casper.options.waitTimeout = waitTimeout;
         casper.options.pageSettings.resourceTimeout = waitTimeout;
    }

    function setBrowserLog(enable) {
        if (enable) {
            casper.on('remote.message', function(message) {
                casper.echo('BROWSER: ' + message);
            });
        }
    }

    init();

    var settings = {
        frontendUrl: hostUrl,
        contactUrl: hostUrl + 'contact/',
    };

    return settings;
};
