module.exports = function(config) {
    var gulpConfig = require('./gulp.config.js')();

    /**
    * List of npm packages that imported via `import` syntax
    */
    var dependencies = [
        '@angular',
        'rxjs',
    ];

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
            // XXX include env.js !!!
            //createFilePattern(gulpConfig.path.build + 'frontend/test-helpers/global/**/*.js', { included: true }),
            {pattern: gulpConfig.path.build + 'frontend/**/*.js', included: false, watched: true},
            gulpConfig.path.build + 'frontend/test-helpers/global/**/*.js',

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
            {pattern: gulpConfig.path.build + '@angular/**/*.js', included: false, watched: false},
            {pattern: gulpConfig.path.build + '@angular/**/*.js.map', included: false, watched: false},

            // {pattern: 'systemjs.config.js', included: false, watched: false},
            createFilePattern(gulpConfig.path.root + 'systemjs.config.js', { included: true }),
            'karma-test-shim.js',
            // createFilePattern(gulpConfig.path.root + 'karma-test-shim.js', { included: true }),

            // transpiled application & spec code paths loaded via module imports
            // {pattern: appBase + '**/*.js', included: false, watched: true},
            // {pattern: gulpConfig.path.build + 'frontend/**/!(*.spec|main)+(.js)', included: false, watched: true},
            // {pattern: gulpConfig.path.build + 'frontend/**/*.js', included: false, watched: true},
            // {pattern: gulpConfig.path.build + 'frontend/test-helpers/global/**/*.js', included: true },


            // asset (HTML & CSS) paths loaded via Angular's component compiler
            // (these paths need to be rewritten, see proxies section)
            // {pattern: appBase + '**/*.html', included: false, watched: true},
            // {pattern: appBase + '**/*.css', included: false, watched: true},

            // paths for debugging with source maps in dev tools
            // {pattern: appBase + '**/*.ts', included: false, watched: false},
            // {pattern: appBase + '**/*.js.map', included: false, watched: false}
            {pattern: gulpConfig.typescript.files, included: false, watched: false},
            {pattern: gulpConfig.path.build + '**/*.js.map', included: false, watched: false}
        ],

        // proxied base paths
        proxies: {
            '/static/': '/base/crowdgezwitscher/static/build/',
            '/crowdgezwitscher/': '/base/crowdgezwitscher/',
            //'/@angular/': '/base/crowdgezwitscher/static/build/@angular/',
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

    var files = [
        createFilePattern(gulpConfig.path.build + '**/*.js', { included: false, watched: false }),
        createFilePattern(gulpConfig.path.build + '**/*.js.map', { included: false, watched: false }),
        // createFilePattern(gulpConfig.path.build + 'frontend/test-helpers/global/**/*.js', { included: true }),
        // createFilePattern('node_modules/core-js/client/shim.min.js.map', { included: false, watched: false }),

        // createFilePattern(gulpConfig.path.root + 'systemjs.config.js', { included: true }),
        // createFilePattern(gulpConfig.path.root + 'karma-test-shim.js', { included: true }),
        // createFilePattern(gulpConfig.typescript.files, { included: false, watched: false }),
    ];

    // configuration.files = configuration.files.concat(files);

    dependencies.forEach(function(key) {
        configuration.files.push({
            pattern: 'node_modules/' + key + '/**/*.js',
            included: false,
            watched: false
        });
    });

    config.set(configuration);

    // Helpers
    function createFilePattern(path, config) {
        config.pattern = path;
        return config;
    }
}
