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
    basePath: './',

    frameworks: ['jasmine'],
    browsers: ['PhantomJS'],
    reporters: ['progress', 'coverage'],

    preprocessors: {},

    // Generate json used for remap-istanbul
    coverageReporter: {
      dir: 'report/',
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
    // proxies: {
    //   // required for component assests fetched by Angular's compiler
    //   "/src/": "/base/src/",
    //   "/app/": "/base/src/app/",
    //   "/node_modules/": "/base/node_modules/"
    // },

    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true
  };

  configuration.preprocessors[__dirname + '/frontend/' + '**/!(*.spec)+(.js)'] = ['coverage'];
  // configuration.preprocessors[gulpConfig.tmpApp + '**/*.js'] = ['sourcemap'];
  // configuration.preprocessors[gulpConfig.tmpTest + '**/*.js'] = ['sourcemap'];

  var files = [
    //gulpConfig.tmpTest + 'test-helpers/global/**/*.js',
    createFilePattern(__dirname + '/systemjs.config.js', { included: false }),
    createFilePattern(__dirname + '/karma-test-shim.js', { included: false }),
    createFilePattern(gulpConfig.typescript.files, { included: false, watched: false })
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
