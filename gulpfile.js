'use strict';

var argv = require('yargs').argv;
var gulp = require('gulp');
var exec = require('child_process').exec;
var sass = require('gulp-sass');
var merge = require('merge2');
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var cssnano = require('gulp-cssnano');
var embedTemplates = require('gulp-angular-embed-templates');
var SystemBuilder = require('systemjs-builder');
var typescript = require('gulp-typescript');
var tsconfig = require('./tsconfig.json');
var tsProject = typescript.createProject(tsconfig.compilerOptions);

if (!argv.production) {
    var clean = require('gulp-clean');
    var tslint = require('gulp-tslint');
    var sassLint = require('gulp-sass-lint');
}

var sass_path = './frontend/**/*.scss';
var ts_path = './frontend/**/*.ts';
var static_npm_file_paths = [
    'node_modules/bootstrap/dist/css/bootstrap.min.css',
    'node_modules/bootstrap/dist/css/bootstrap.min.css.map',
    'node_modules/rxjs/**/*',
    'node_modules/@angular/**/*',
    'node_modules/systemjs/dist/system.src.js',
    'node_modules/symbol-observable/**/*',
];
var angular_dependencies = [
    'node_modules/es6-shim/es6-shim.min.js',
    'node_modules/zone.js/dist/zone.js',
    'node_modules/reflect-metadata/Reflect.js',
];
var build_path = 'strassengezwitscher/static/build/';
var dist_path = 'strassengezwitscher/static/dist/';

gulp.task('copy:npmfiles', function() {
    return gulp.src(static_npm_file_paths.concat(angular_dependencies), {base: 'node_modules/'})
        .pipe(gulp.dest(build_path));
});

gulp.task('copy:systemjsconfig', function() {
    return gulp.src('systemjs.config.js')
        .pipe(gulp.dest(build_path));
});

gulp.task('copy:staticfiles', ['copy:npmfiles', 'copy:systemjsconfig']);

gulp.task('compile:sass', function() {
    return gulp.src(sass_path)
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(concat('bundle.dev.css'))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(build_path));
});

gulp.task('compile:typescript', function() {
    var tsResult = gulp.src(ts_path)
        .pipe(sourcemaps.init())
        .pipe(typescript(tsProject));
    return merge([
        tsResult.dts.pipe(gulp.dest(build_path)),
        tsResult.js
            .pipe(embedTemplates())
            .pipe(sourcemaps.write())
            .pipe(gulp.dest(build_path))
    ]);
});

gulp.task('bundle:typescript', ['copy:staticfiles', 'compile:typescript'], function() {
    var builder = new SystemBuilder(build_path, {
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
          '@angular/router-deprecated': { main: 'index.js', defaultExtension: 'js' },
          '@angular/upgrade': { main: 'index.js', defaultExtension: 'js' },
      }
    });
    builder.loader.defaultJSExtensions = true;
    return builder.buildStatic('main', dist_path + '/bundle.js', {
        minify: true
    });
});

gulp.task('bundle:dependencies', function() {
    return gulp.src([
        'node_modules/es6-shim/es6-shim.min.js',
        'node_modules/zone.js/dist/zone.js',
        'node_modules/reflect-metadata/Reflect.js'
    ]).pipe(concat('dependencies.js'))
    .pipe(uglify())
    .pipe(gulp.dest(dist_path));
});

gulp.task('bundle:sass', ['compile:sass'], function() {
    return gulp.src([
        build_path + '/bootstrap/**/*.css',
        build_path + '/bundle.dev.css'
    ]).pipe(concat('bundle.css'))
        .pipe(cssnano())
        .pipe(gulp.dest(dist_path));
});

gulp.task('dist', ['bundle:dependencies', 'bundle:typescript', 'bundle:sass']);

gulp.task('watch:sass', ['compile:sass'], function() {
    return gulp.watch(sass_path, ['compile:sass']);
});

gulp.task('watch:typescript', ['compile:typescript'], function() {
    return gulp.watch(ts_path, ['compile:typescript']);
});

gulp.task('watch', ['watch:sass', 'watch:typescript']);

gulp.task('build', ['copy:staticfiles', 'compile:typescript', 'compile:sass']);

gulp.task('default', function() {
  // place code for your default task here
});

if (!argv.production) {
    gulp.task('lint:python', function() {
        exec('prospector strassengezwitscher --profile ../.landscape.yml', function (err, stdout, stderr) {
            console.log(stdout);
            console.log(stderr);
        });
    });

    gulp.task('lint:typescript', function() {
        return gulp.src(ts_path)
        .pipe(tslint())
        .pipe(tslint.report("prose", {
            emitError: false,
            summarizeFailureOutput: true
        }));
    });

    gulp.task('lint:sass', function() {
        return gulp.src(sass_path)
        .pipe(sassLint())
        .pipe(sassLint.format());
    });

    gulp.task('lint', ['lint:python', 'lint:typescript', 'lint:sass']);

    gulp.task('clean', function() {
        return gulp.src([build_path, dist_path], {read: false})
            .pipe(clean());
    });
}
