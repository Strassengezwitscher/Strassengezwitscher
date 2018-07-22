module.exports = function () {
    var root = './';
    var path = {
        root: root,
        build: root + 'crowdgezwitscher/static/build/',
        dist: root + 'crowdgezwitscher/static/dist/',
        shared: root + 'crowdgezwitscher/static/shared/',
        npm: root + 'node_modules/',
        frontend: 'frontend/',
        report: root + '.report/',
        partial: {
            frontend: 'frontend',
        },
        frontend_config: 'frontend/config/',
        aot: root + 'aot/',
        aot_compiled: root + 'aot-compiled/',
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
        exclude_files: '!' + root + 'frontend/main-ngc.ts',
        bundle: {
            config: root + 'rollup.config.js',
            entry: root + 'aot-compiled/aot/frontend/main-ngc.js',
            dest: path.dist + 'bundle.js',
        },
    };

    var frontend = {
        all: path.frontend + '**/*',
        imgFiles: path.frontend + 'img/*',
        htmlFiles: path.frontend + '**/*.html',
    };

    var e2e = {
        files: 'e2e/test_*',
    }

    var npm = {
        static: [
            path.npm + 'core-js/client/shim.min.js',
            path.npm + 'rxjs/**/*',
            path.npm + '@angular/**/*.+(js|js.map)',
            path.npm + 'systemjs/dist/system.src.js',
            path.npm + 'symbol-observable/**/*',
            path.npm + 'traceur/bin/traceur.js',
            path.npm + 'cookieconsent/build/cookieconsent.min.js',
            path.npm + 'cookieconsent/build/cookieconsent.min.css'
        ],
        shared_files: [
            path.npm + 'bootstrap/dist/css/bootstrap.min.css',
            path.npm + 'bootstrap/dist/css/bootstrap.min.css.map',
            path.npm + 'bootstrap/dist/js/bootstrap.min.js',
            path.npm + 'bootstrap/dist/fonts/*',
            path.npm + 'jquery/dist/jquery.min.js',
            path.npm + 'django-formset/dist/django-formset.js',
            path.npm + 'selectize/dist/js/standalone/selectize.min.js',
            path.npm + 'selectize/dist/css/selectize.bootstrap3.css',
            path.npm + 'eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js',
            path.npm + 'eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.min.css',
            path.npm + 'moment/min/moment-with-locales.min.js',
        ],
        angular_dependencies: {
            files: [
                path.npm + 'zone.js/dist/zone.js',
                path.npm + 'reflect-metadata/Reflect.js',
                path.npm + 'hammerjs/hammer.js',
                path.npm + 'web-animations-js/web-animations.min.js',
            ],
            name: 'dependencies.js',
        },
    };
    npm['files'] = npm.static.concat(npm.angular_dependencies.files);

    var systemjs = {
        files: 'systemjs.config.js',
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
