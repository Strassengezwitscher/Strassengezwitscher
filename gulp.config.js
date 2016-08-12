module.exports = function () {
    var root = './';
    var path = {
        root: root,
        build: root + 'strassengezwitscher/static/build/',
        dist: root + 'strassengezwitscher/static/dist/',
        npm: root + 'node_modules/',
        frontend: 'frontend/',
        report: root + '.report/',
        partial: {
            frontend: 'frontend',
        },
    };

    var sass = {
        files: root + 'frontend/**/*.scss',
        bundle: {
            name: 'bundle.css',
            dev_name: 'bundle.dev.css',
            files: [
                path.build + 'materialize-css/**/*.css',
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

    var frontend = {
        imgFiles: path.frontend + 'img/*',
        htmlFiles: path.frontend + '*.html',
    };

    var e2e = {
        files: 'e2e/test_*',
    }

    var npm = {
        static: [
            path.npm + 'bootstrap/dist/css/bootstrap.min.css',
            path.npm + 'bootstrap/dist/css/bootstrap.min.css.map',
            path.npm + 'bootstrap/dist/js/bootstrap.min.js',
            path.npm + 'bootstrap/dist/fonts/*',
            path.npm + 'jquery/dist/jquery.min.js',
            path.npm + 'rxjs/**/*',
            path.npm + '@angular/**/*.+(js|js.map)',
            path.npm + '@angular2-material/**/*',
            path.npm + 'systemjs/dist/system.src.js',
            path.npm + 'symbol-observable/**/*',
        ],
        angular_dependencies: {
            files: [
                path.npm + 'core-js/client/shim.min.js',
                path.npm + 'zone.js/dist/zone.js',
                path.npm + 'reflect-metadata/Reflect.js',
                path.npm + 'hammerjs/hammer.js',
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

    var report = {
        path: path.report + 'report-json/coverage-final.json',
        karma: {
            configFile: __dirname + '/karma.config.js',
        },
        remap: {
            reports: {
                'lcovonly': path.report + 'remap/lcov.info',
                'html': path.report + 'remap/html-report',
            },
        },
    }

    var config = {
        path: path,
        sass: sass,
        typescript: typescript,
        e2e: e2e,
        npm: npm,
        systemjs: systemjs,
        frontend: frontend,
        report: report,
    };

    return config;
};
