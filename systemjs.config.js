(function(global) {
  // ENV
  global.ENV = global.ENV || 'development';

  // map tells the System loader where to look for things
  var map = {
    'app':                        'app', // 'dist',
    'rxjs':                       'static/rxjs',
    '@angular':                   'static/@angular',
    '@angular2-material':         'static/@angular2-material',
    'symbol-observable':          'static/symbol-observable',
    'captcha':                    'static/frontend/app/captcha',
    'contact':                    'static/frontend/app/contact',
    'events':                     'static/frontend/app/events',
    'facebook':                   'static/frontend/app/facebook',
    'map':                        'static/frontend/app/map',
  };

  // packages tells the System loader how to load when no filename and/or no extension
  var packages = {
    'app':                        { main: 'frontend/main.js', defaultExtension: 'js' },
    'rxjs':                       { defaultExtension: 'js' },
    'symbol-observable':          { main: 'index.js', defaultExtension: 'js' },
    'ng2-bootstrap':              { defaultExtension: 'js' },
    'captcha':                    { main: 'index.js', defaultExtension: 'js' },
    'contact':                    { main: 'index.js', defaultExtension: 'js' },
    'events':                     { main: 'index.js', defaultExtension: 'js' },
    'facebook':                   { main: 'index.js', defaultExtension: 'js' },
    'map':                        { main: 'index.js', defaultExtension: 'js' },
  };

  var ngPackageNames = [
    'common',
    'compiler',
    'core',
    'forms',
    'http',
    'platform-browser',
    'platform-browser-dynamic',
    'router',
    'router-deprecated',
    'upgrade',
  ];

  // Individual files (~300 requests):
  function packIndex(pkgName) {
    packages['@angular/'+pkgName] = { main: 'index.js', defaultExtension: 'js' };
  }
  // Bundled (~40 requests):
  function packUmd(pkgName) {
    packages['@angular/'+pkgName] = { main: '/bundles/' + pkgName + '.umd.js', defaultExtension: 'js' };
  }
  // Most environments should use UMD; some (Karma) need the individual index files
  var setPackageConfig = System.packageWithIndex || global.ENV == 'testing' ? packIndex : packUmd;
  // Add package entries for angular packages
  ngPackageNames.forEach(setPackageConfig);

  var config = {
    map: map,
    packages: packages
  };

  System.config(config);
  System.defaultJSExtensions = true;

})(this);
