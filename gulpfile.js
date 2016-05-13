'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var typescript = require('gulp-typescript');
var tsconfig = require('./tsconfig.json')

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

gulp.task('copy_static_npm_files', function() {
    return gulp.src(static_npm_file_paths, {base: 'node_modules/'})
        .pipe(gulp.dest(static_lib_path));
});

gulp.task('compile_sass', function() {
    return gulp.src(sass_path)
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(static_complied_path));
});

gulp.task('watch_sass', ['compile_sass'], function() {
    return gulp.watch(sass_path, ['compile_sass']);
});

gulp.task('compile_typescript', function() {
    return gulp.src(ts_path)
        .pipe(typescript(tsconfig.compilerOptions))
        .pipe(gulp.dest(static_complied_path));
});

gulp.task('watch_typescript', ['compile_typescript'], function() {
    return gulp.watch(ts_path, ['compile_typescript']);
});

gulp.task('watch', ['watch_sass', 'watch_typescript']);

gulp.task('default', function() {
  // place code for your default task here
});
