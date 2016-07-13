module.exports = function () {
    var root = './';
    var path = {
        root: root,
        build: root + 'strassengezwitscher/static/build/',
        dist: root + 'strassengezwitscher/static/dist/',
        npm: root + 'node_modules/',
        report: root + '.report/',
    };
    var sass = {
        files: root + 'frontend/**/*.scss',
        bundle: {
            name: 'bundle.css',
            dev_name: 'bundle.dev.css',
            files: [
                path.build + 'bootstrap/**/*.css',
                path.build + 'bundle.dev.css',
            ],
        },
    };
    var typescript = {
        files: root + 'frontend/**/*.ts',
        bundle: {
            path: path.dist + 'bundle.js',
            config: {
                minify: true,
            },
        },
    };

    var npm = {
        static: [
            path.npm + 'bootstrap/dist/css/bootstrap.min.css',
            path.npm + 'bootstrap/dist/css/bootstrap.min.css.map',
            path.npm + 'rxjs/**/*',
            path.npm + '@angular/**/*',
            path.npm + 'systemjs/dist/system.src.js',
            path.npm + 'symbol-observable/**/*',
        ],
        angular_dependencies: {
            files: [
                path.npm + 'es6-shim/es6-shim.min.js',
                path.npm + 'zone.js/dist/zone.js',
                path.npm + 'reflect-metadata/Reflect.js',
            ],
            name: 'dependencies.js',
        },
    };
    npm['files'] = npm.static.concat(npm.angular_dependencies.files);

    var systemjs_config = {
        map: {
            '@angular/common.js': '@angular/common',
            '@angular/compiler.js': '@angular/compiler',
            '@angular/core.js': '@angular/core',
            '@angular/forms.js': '@angular/forms',
            '@angular/http.js': '@angular/http',
            '@angular/platform-browser.js': '@angular/platform-browser',
            '@angular/platform-browser-dynamic.js': '@angular/platform-browser-dynamic',
            '@angular/router.js': '@angular/router',
            '@angular/router-deprecated.js': '@angular/router-deprecated',
            '@angular/upgrade.js': '@angular/upgrade',
        },
        packages: {
          'rxjs': { defaultExtension: 'js' },
          'symbol-observable': { main: 'index.js', defaultExtension: 'js' },
          '@angular/common': { main: 'index.js', defaultExtension: 'js' },
          '@angular/compiler': { main: 'index.js', defaultExtension: 'js' },
          '@angular/core': { main: 'index.js', defaultExtension: 'js' },
          '@angular/forms': { main: 'index.js', defaultExtension: 'js' },
          '@angular/http': { main: 'index.js', defaultExtension: 'js' },
          '@angular/platform-browser': { main: 'index.js', defaultExtension: 'js' },
          '@angular/platform-browser-dynamic': { main: 'index.js', defaultExtension: 'js' },
          '@angular/router': { main: 'index.js', defaultExtension: 'js' },
          '@angular/upgrade': { main: 'index.js', defaultExtension: 'js' },
      },
    };
    var systemjs = {
        files: [root + 'systemjs.config.js'],
        config: systemjs_config,
    }

    var config = {
        path: path,
        sass: sass,
        typescript: typescript,
        npm: npm,
        systemjs: systemjs,
    };

    return config;
};
