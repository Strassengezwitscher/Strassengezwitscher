'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');

var sass_path = './strassengezwitscher/**/css/*.scss'
var static_npm_file_paths = [
    'node_modules/bootstrap/dist/css/bootstrap.min.css',
    'node_modules/bootstrap/dist/css/bootstrap.min.css.map',
    'node_modules/angular/angular.min.js',
    'node_modules/angular/angular.min.js.map'
];

gulp.task('copy_static_npm_files', function() {
    return gulp.src(static_npm_file_paths, {base: 'node_modules/'})
        .pipe(gulp.dest('strassengezwitscher/static/lib/'));
});

gulp.task('compile_sass', function() {
    return gulp.src(sass_path)
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('strassengezwitscher/static/compiled/'));
});

gulp.task('watch_sass', ['compile_sass'], function() {
    return gulp.watch(sass_path, ['compile_sass']);
});

gulp.task('watch', ['watch_sass']);

gulp.task('default', function() {
  // place code for your default task here
});
