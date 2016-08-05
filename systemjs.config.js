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
  };

  // packages tells the System loader how to load when no filename and/or no extension
  var packages = {
    'app':                        { main: 'frontend/main.js', defaultExtension: 'js' },
    'rxjs':                       { defaultExtension: 'js' },
    'symbol-observable':          { main: 'index.js', defaultExtension: 'js' },
    'ng2-bootstrap':               { defaultExtension: 'js' },
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


  // put the names of any of your Material components here
  const materialPkgs = [
    'core',
    'button',
    'card',
    'icon',
    'input',
    'slide-toggle',
    'toolbar',
  ];

  materialPkgs.forEach(function(pkgName) {
    packages['@angular2-material/' + pkgName] = { main: pkgName + '.js' };
  });

  var config = {
    map: map,
    packages: packages
  };

  System.config(config);
  System.defaultJSExtensions = true;

})(this);
