module.exports = function(config) {
  var gulpConfig = require('./gulp.config.js')();

  /**
   * List of npm packages that imported via `import` syntax
   */
  var dependencies = [
    '@angular',
    'rxjs'
  ];

  var configuration = {
    // basePath: '',

    frameworks: ['jasmine'],
    browsers: ['PhantomJS'],
    reporters: ['mocha', 'coverage'],

    preprocessors: {},

    // Generate json used for remap-istanbul
    coverageReporter: {
      includeAllSources: true,
      dir: '.report/',
      reporters: [
        { type: 'json', subdir: 'report-json' }
      ]
    },

    files: [
      'node_modules/core-js/client/shim.min.js',
      'node_modules/zone.js/dist/zone.js',
      'node_modules/zone.js/dist/async-test.js',
      'node_modules/zone.js/dist/fake-async-test.js',
      'node_modules/systemjs/dist/system.src.js'
    ],

    // proxied base paths
    proxies: {
      // required for component assests fetched by Angular's compiler
    //   "/src/": "/base/src/",
    //   "/app/": "/base/src/app/",
        // '/node_modules/': '/base/node_modules/',
        '/static/': '/base/strassengezwitscher/static/build/',
        '/strassengezwitscher/': '/base/strassengezwitscher/'
    },

    port: 9876,
    colors: true,
    logLevel: config.LOG_WARN,
    autoWatch: true
  };

  configuration.preprocessors[gulpConfig.path.build + 'frontend/**/!(*.spec|main)+(.js)'] = ['coverage'];
  // configuration.preprocessors[gulpConfig.tmpApp + '**/*.js'] = ['sourcemap'];
  // configuration.preprocessors[gulpConfig.tmpTest + '**/*.js'] = ['sourcemap'];
  configuration.preprocessors[gulpConfig.path.build + '**/*.js'] = ['sourcemap'];

  var files = [
    createFilePattern(gulpConfig.path.build + '**/*.js', { included: false, watched: false }),
    createFilePattern(gulpConfig.path.build + '**/*.js.map', { included: false, watched: false }),
    createFilePattern(gulpConfig.path.build + 'frontend/test-helpers/global/**/*.js', { included: true }),
    createFilePattern('node_modules/core-js/client/shim.min.js.map', { included: false, watched: false }),
    // createFilePattern(gulpConfig.path.build + 'frontend/**/*.js', { included: true, watched: false, served: false }),
    createFilePattern(gulpConfig.path.root + 'systemjs.config.js', { included: true }),
    createFilePattern(gulpConfig.path.root + 'karma-test-shim.js', { included: true }),
    createFilePattern(gulpConfig.typescript.files, { included: false, watched: false }),
  ];

  configuration.files = configuration.files.concat(files);

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
