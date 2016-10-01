module.exports = function(config) {
    var gulpConfig = require('./gulp.config.js')();

    var configuration = {
        frameworks: ['jasmine'],
        browsers: ['PhantomJS'],
        reporters: ['mocha', 'coverage'],

        preprocessors: {},

        // Generate json used for remap-istanbul
        coverageReporter: {
            includeAllSources: true,
            dir: gulpConfig.path.report,
            reporters: [
                { type: 'json', subdir: 'report-json' }
            ]
        },

        files: [
            // transpiled application & spec code paths loaded via module imports
            { pattern: gulpConfig.path.build + 'frontend/**/*.js', included: false, watched: true },
            { pattern: gulpConfig.path.build + 'frontend/test-helpers/global/**/*.js', included: true },

            // System.js for module loading
            'node_modules/systemjs/dist/system.src.js',
            'node_modules/systemjs/dist/system-polyfills.js',

            // Polyfills
            'node_modules/core-js/client/shim.js',

            // Reflect and Zone.js
            'node_modules/reflect-metadata/Reflect.js',
            'node_modules/zone.js/dist/zone.js',
            'node_modules/zone.js/dist/long-stack-trace-zone.js',
            'node_modules/zone.js/dist/proxy.js',
            'node_modules/zone.js/dist/sync-test.js',
            'node_modules/zone.js/dist/jasmine-patch.js',
            'node_modules/zone.js/dist/async-test.js',
            'node_modules/zone.js/dist/fake-async-test.js',

            // RxJs.
            { pattern: gulpConfig.path.build + 'rxjs/**/*.js', included: false, watched: false },
            { pattern: gulpConfig.path.build + 'rxjs/**/*.js.map', included: false, watched: false },

            // Angular 2 itself and the testing library
            {pattern: gulpConfig.path.build + '@angular/**/!(*.spec)+(.js)', included: false, watched: false},
            {pattern: gulpConfig.path.build + '@angular/**/*.js.map', included: false, watched: false},

            { pattern: gulpConfig.path.root + 'systemjs.config.js', included: true },
            'karma-test-shim.js',

            // paths for debugging with source maps in dev tools
            {pattern: gulpConfig.typescript.files, included: false, watched: false},
            {pattern: gulpConfig.path.build + '**/*.js.map', included: false, watched: false}
        ],

        // proxied base paths
        proxies: {
            '/static/': '/base/crowdgezwitscher/static/build/',
            '/crowdgezwitscher/': '/base/crowdgezwitscher/',
        },

        port: 9876,
        colors: true,
        logLevel: config.LOG_WARN,
        autoWatch: true,
        client: {
            captureConsole: false
        }
    };

    configuration.preprocessors[gulpConfig.path.build + 'frontend/**/!(*.spec|main)+(.js)'] = ['coverage'];
    configuration.preprocessors[gulpConfig.path.build + '**/*.js.map'] = ['sourcemap'];

    config.set(configuration);
}
