(function(global) {
  // ENV
  global.ENV = global.ENV || 'development';
  console.log(global.ENV);

  // map tells the System loader where to look for things
  var map = {
    'app': global.ENV == 'testing' ? 'crowdgezwitscher/static/build/frontend/app' : 'static/frontend/app',
    // 'app': 'crowdgezwitscher/static/build/frontend/app',
    'rxjs': 'static/rxjs',
    '@angular': 'static/@angular',
    '@angular2-material': 'static/@angular2-material',
    'symbol-observable': 'static/symbol-observable',
    'traceur': 'static/traceur/bin/traceur',
  };
  console.log('dasfasdfasd', map['app']);

  // packages tells the System loader how to load when no filename and/or no extension
  var packages = {
    'app': { main: 'frontend/main.js', defaultExtension: 'js' },
    'rxjs': { defaultExtension: 'js' },
    'symbol-observable': { main: 'index.js', defaultExtension: 'js' },
  };

  var appBarrels = [
    'app/captcha',
    'app/contact',
    'app/events',
    'app/facebook',
    'app/map'
  ];

  appBarrels.forEach(function(barrelName) {
    packages[barrelName] = { main: 'index.js' }
  });

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
    packages['@angular/'+pkgName+'/testing'] = { main: 'index.js', defaultExtension: 'js' };
  }
  // Bundled (~40 requests):
  function packUmd(pkgName) {
    packages['@angular/'+pkgName] = { main: '/bundles/' + pkgName + '.umd.js', defaultExtension: 'js' };
    // packages['@angular/'+pkgName+'/testing'] = { main: 'index.js', defaultExtension: 'js' };
    packages['@angular/'+pkgName+'/testing'] = { main: '../bundles/' + pkgName + '-testing.umd.js', defaultExtension: 'js' };
  }
  // Most environments should use UMD; some (Karma) need the individual index files
  // var setPackageConfig = System.packageWithIndex || global.ENV == 'testing' ? packIndex : packUmd;
  var setPackageConfig = packUmd;
  // Add package entries for angular packages
  ngPackageNames.forEach(setPackageConfig);


  var materialPackages = [
    'button',
    'card',
    'core',
    'checkbox',
    'icon',
    'input',
    'slide-toggle',
    'toolbar',
    'tooltip',
  ];

  materialPackages.forEach(function(pkgName) {
    packages['@angular2-material/' + pkgName] = {
      format: 'cjs',
      main: pkgName + '.umd.js'
    };
  });


  var config = {
    map: map,
    packages: packages
  };

  System.config(config);
  System.defaultJSExtensions = true;

})(this);
