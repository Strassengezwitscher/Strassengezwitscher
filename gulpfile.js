'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var merge = require('merge2');
var typescript = require('gulp-typescript');
var tsconfig = require('./tsconfig.json');
var tsProject = typescript.createProject(tsconfig.compilerOptions);

var sass_path = './strassengezwitscher/**/css/*.scss';
var ts_path = './frontend/**/*.ts';
var static_npm_file_paths = [
    'node_modules/bootstrap/dist/css/bootstrap.min.css',
    'node_modules/bootstrap/dist/css/bootstrap.min.css.map',
    'node_modules/rxjs/**/*',
    'node_modules/angular2-in-memory-web-api/**/*',
    'node_modules/@angular/**/*',
    'node_modules/es6-shim/es6-shim.min.js',
    'node_modules/zone.js/dist/zone.js',
    'node_modules/reflect-metadata/Reflect.js',
    'node_modules/systemjs/dist/system.src.js'
];
var static_lib_path = 'strassengezwitscher/static/lib/';
var static_complied_path = 'strassengezwitscher/static/compiled/';

gulp.task('copy:staticnpmfiles', function() {
    return gulp.src(static_npm_file_paths, {base: 'node_modules/'})
        .pipe(gulp.dest(static_lib_path));
});

gulp.task('compile:sass', function() {
    return gulp.src(sass_path)
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(static_complied_path));
});

gulp.task('compile:typescript', function() {
    var tsResult = gulp.src(ts_path).pipe(typescript(tsProject));
    return merge([
        tsResult.dts.pipe(gulp.dest(static_complied_path)),
        tsResult.js.pipe(gulp.dest(static_complied_path))
    ]);
});

gulp.task('watch:sass', ['compile:sass'], function() {
    return gulp.watch(sass_path, ['compile:sass']);
});

gulp.task('watch:typescript', ['compile:typescript'], function() {
    return gulp.watch(ts_path, ['compile:typescript']);
});

gulp.task('watch', ['watch:sass', 'watch:typescript']);

gulp.task('default', function() {
  // place code for your default task here
});
