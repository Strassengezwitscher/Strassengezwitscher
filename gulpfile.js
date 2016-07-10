'use strict';

var config = require('./gulp.config.js')();
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

gulp.task('copy:npmfiles', function() {
    return gulp.src(config.npm.files, {base: config.path.npm})
        .pipe(gulp.dest(config.path.build));
});

gulp.task('copy:systemjsconfig', function() {
    return gulp.src(config.systemjs.files)
        .pipe(gulp.dest(config.path.build));
});

gulp.task('copy:staticfiles', ['copy:npmfiles', 'copy:systemjsconfig']);

gulp.task('compile:sass', function() {
    return gulp.src(config.sass.files)
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(concat(config.sass.bundle.dev_name))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.path.build));
});

gulp.task('compile:typescript', function() {
    var tsResult = gulp.src(config.typescript.files)
        .pipe(sourcemaps.init())
        .pipe(typescript(tsProject));
    return merge([
        tsResult.dts.pipe(gulp.dest(config.path.build)),
        tsResult.js
            .pipe(embedTemplates())
            .pipe(sourcemaps.write())
            .pipe(gulp.dest(config.path.build))
    ]);
});

gulp.task('bundle:typescript', ['copy:staticfiles', 'compile:typescript'], function() {
    var builder = new SystemBuilder(config.path.build, config.systemjs.config);
    builder.loader.defaultJSExtensions = true;
    return builder.buildStatic('main', config.typescript.bundle.path, config.typescript.bundle.config);
});

gulp.task('bundle:dependencies', function() {
    return gulp.src(config.npm.angular_dependencies.files)
        .pipe(concat(config.npm.angular_dependencies.name))
        .pipe(uglify())
        .pipe(gulp.dest(config.path.dist));
});

gulp.task('bundle:sass', ['compile:sass'], function() {
    return gulp.src(config.sass.bundle.files)
        .pipe(concat(config.sass.bundle.name))
        .pipe(cssnano())
        .pipe(gulp.dest(config.path.dist));
});

gulp.task('dist', ['bundle:dependencies', 'bundle:typescript', 'bundle:sass']);

gulp.task('watch:sass', ['compile:sass'], function() {
    return gulp.watch(config.sass.path, ['compile:sass']);
});

gulp.task('watch:typescript', ['compile:typescript'], function() {
    return gulp.watch(config.typescript.files, ['compile:typescript']);
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
        return gulp.src(config.typescript.files)
            .pipe(tslint({configuration: 'tslint.json'}))
            .pipe(tslint.report('prose', {
                emitError: false,
                summarizeFailureOutput: true
            }));
    });

    gulp.task('lint:sass', function() {
        return gulp.src(config.sass.files)
            .pipe(sassLint())
            .pipe(sassLint.format());
    });

    gulp.task('lint', ['lint:python', 'lint:typescript', 'lint:sass']);

    gulp.task('clean', function() {
        return gulp.src([config.path.build, config.path.dist], {read: false})
            .pipe(clean());
    });
}
