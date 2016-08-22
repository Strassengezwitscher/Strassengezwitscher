'use strict';

var config = require('./gulp.config.js')();
var argv = require('yargs').argv;
var gulp = require('gulp');
var rename = require('gulp-rename');
var fs = require('fs');
var exec = require('child_process').exec;
var sass = require('gulp-sass');
var merge = require('merge2');
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var cssnano = require('gulp-cssnano');
var SystemBuilder = require('systemjs-builder');
var typescript = require('gulp-typescript');
var tsconfig = require('./tsconfig.json');
var tsProject = typescript.createProject(tsconfig.compilerOptions);

if (!argv.production) {
    var clean = require('gulp-clean');
    var tslint = require('gulp-tslint');
    var sassLint = require('gulp-sass-lint');
    var Server = require('karma').Server;
    var remapIstanbul = require('remap-istanbul/lib/gulpRemapIstanbul');
}

gulp.task('copy:npmfiles', function() {
    return gulp.src(config.npm.files, {base: config.path.npm})
        .pipe(gulp.dest(config.path.build));
});

gulp.task('copy:sensitive_config', function() {
    fs.stat(config.path.frontend_config + 'sensitive_conf.ts', function(err, stat) {
        if(err != null) {
            return gulp.src(config.path.frontend_config + 'sensitive_conf_dummy.ts')
                .pipe(rename('sensitive_conf.ts'))
                .pipe(gulp.dest(config.path.frontend_config));
        }
    });
});

gulp.task('copy:config', ['copy:sensitive_config'] , function() {
    var config_path = config.path.frontend_config + ((argv.production) ? 'prod_conf.ts': 'dev_conf.ts');
    return gulp.src(config_path)
        .pipe(rename('config.ts'))
        .pipe(gulp.dest(config.path.frontend_config));
});

gulp.task('copy:systemjsconfig', function() {
    return gulp.src(config.systemjs.files)
        .pipe(gulp.dest(config.path.build));
});

gulp.task('copy:frontendImgFiles', function() {
    return gulp.src(config.frontend.imgFiles, {base: config.path.frontend})
        .pipe(gulp.dest(config.path.build));
});

gulp.task('copy:html', function() {
    return gulp.src(config.frontend.htmlFiles, {base: config.path.root})
        .pipe(gulp.dest(config.path.build));
});

gulp.task('copy:staticfiles', ['copy:npmfiles', 'copy:systemjsconfig', 'copy:frontendImgFiles']);

gulp.task('compile:sass', function() {
    return gulp.src(config.sass.files)
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(concat(config.sass.bundle.dev_name))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.path.build));
});

gulp.task('compile:typescript', ['copy:config'], function() {
    var tsResult = gulp.src(config.typescript.files)
        .pipe(sourcemaps.init())
        .pipe(typescript(tsProject));
    return merge([
        tsResult.dts.pipe(gulp.dest(config.path.build)),
        tsResult.js
            .pipe(sourcemaps.write('./', {sourceRoot: config.path.partial.frontend}))
            .pipe(gulp.dest(config.path.build + config.path.partial.frontend))
    ]);
});

gulp.task('bundle:typescript', function() {
    var builder = new SystemBuilder("./compiled2", config.systemjs.config);
    builder.loader.defaultJSExtensions = true;
    return builder.buildStatic('main-ngc', config.typescript.bundle.path, config.typescript.bundle.config);
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

gulp.task('optimize:frontendImgFiles', function() {
    return gulp.src(config.frontend.imgFiles, {base: config.path.frontend})
        .pipe(gulp.dest(config.path.dist));
});

gulp.task('dist', ['bundle:dependencies', 'bundle:typescript', 'bundle:sass', 'optimize:frontendImgFiles']);

gulp.task('watch:sass', ['compile:sass'], function() {
    return gulp.watch(config.sass.files, ['compile:sass']);
});

gulp.task('watch:typescript', ['compile:typescript'], function() {
    return gulp.watch(config.typescript.files, ['compile:typescript']);
});

gulp.task('watch:frontendImgFiles', ['copy:frontendImgFiles'], function() {
    return gulp.watch(config.frontend.imgFiles, {cwd: config.root}, ['copy:frontendImgFiles']);
});

gulp.task('watch:html', ['copy:html'], function() {
    return gulp.watch(config.frontend.htmlFiles, {cwd: config.root}, ['copy:html']);
});

gulp.task('watch', ['watch:sass', 'watch:typescript', 'watch:frontendImgFiles', 'watch:html']);

gulp.task('build', ['copy:staticfiles', 'copy:html', 'compile:typescript', 'compile:sass']);

gulp.task('default', function() {
  // place code for your default task here
});

// var rollup = require('rollup').rollup;
// var commonjs = require('rollup-plugin-commonjs');
// var nodeResolve = require('rollup-plugin-node-resolve');

// gulp.task('rollup', function () {
//   return rollup({
//     entry: 'compiled2/main-ngc.js',
//     plugins: [
//       nodeResolve({ jsnext: true }),
//       commonjs()
//     ]
//   }).then(function (bundle) {
//     return bundle.write({
//       format: 'iife',
//       dest: 'compiled3/main.js'
//     });
//   });
// });

if (!argv.production) {
    gulp.task('lint:python', function(done) {
        var command = 'prospector crowdgezwitscher --profile ../.landscape.yml';
        var lint = exec(command, function (err, stdout, stderr) {
            console.log(stdout);
            console.log(stderr);
        });
        lint.on('close', function(exitcode) {
            done(exitcode ? new Error('Python linting failed') : 0);
        });
    });

    gulp.task('lint:typescript', function() {
        return gulp.src(config.typescript.files)
            .pipe(tslint({
                configuration: 'tslint.json',
                formatter: 'prose'
            }))
            .pipe(tslint.report({
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

    gulp.task('clean:build', function() {
        return gulp.src(config.path.build, {read: false})
            .pipe(clean());
    });

    gulp.task('clean:dist', function() {
        return gulp.src(config.path.dist, {read: false})
            .pipe(clean());
    });

    gulp.task('clean:report', function() {
        return gulp.src(config.path.report, {read: false})
            .pipe(clean());
    });

    gulp.task('clean', ['clean:build', 'clean:dist', 'clean:report']);

    gulp.task('test:typescript', ['build'], function(done) {
        new Server({
            configFile: config.report.karma.configFile,
            singleRun: true,
        }, function(exitcode) {
            done(exitcode ? new Error('Typescript tests failed') : 0);
        }).start();
    });

    gulp.task('test:e2e', function(done) {
        var command = 'PHANTOMJS_EXECUTABLE=./node_modules/phantomjs-prebuilt/bin/phantomjs ./node_modules/casperjs/bin/casperjs test ' + config.e2e.files;
        var casper = exec(command, function (err, stdout, stderr) {
            console.log(stdout);
            console.log(stderr);
        });
        casper.on('close', function(exitcode) {
            done(exitcode ? new Error('E2E tests failed') : 0);
        });
    });

    gulp.task('test:python', function(done) {
        var command = 'python crowdgezwitscher/manage.py test crowdgezwitscher';
        var test = exec(command, function (err, stdout, stderr) {
            console.log(stdout);
            console.log(stderr);
        });
        test.on('close', function(exitcode) {
            done(exitcode ? new Error('Python tests failed') : 0);
        });
    });

    gulp.task('coverage:typescript', function(done) {
        new Server({
            configFile: config.report.karma.configFile,
            singleRun: true,
        }, remapCoverage).start();

        function remapCoverage(exitcode) {
            console.log('path', config.report.path);
            gulp.src(config.report.path)
                .pipe(remapIstanbul({
                    reports: config.report.remap.reports,
                }))
                .on('finish', function() {
                    done(exitcode ? new Error('Typescript coverage report failed') : 0);
                });
        }
    });

    gulp.task('coverage:python', function(done) {
        var command = 'coverage run crowdgezwitscher/manage.py test crowdgezwitscher';
        var coverage = exec(command, function (err, stdout, stderr) {
            console.log(stdout);
            console.log(stderr);
        });
        coverage.on('close', function(exitcode) {
            done(exitcode ? new Error('Python coverage report failed') : 0);
        });
    });
}
