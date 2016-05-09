var gulp = require('gulp');

var static_npm_file_paths = [
    'node_modules/bootstrap/dist/css/bootstrap.min.css',
    'node_modules/bootstrap/dist/css/bootstrap.min.css.map'
];

gulp.task('copy_static_npm_files', function() {
    gulp.src(static_npm_file_paths, {base: 'node_modules/'})
        .pipe(gulp.dest('strassengezwitscher/static/lib/'));
});

gulp.task('default', function() {
  // place code for your default task here
});
