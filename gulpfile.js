var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');

gulp.task('common', function() {
  gulp.src(["./apps/website/static/javascripts/lib/scrolling-nav-1.0.1/js/bootstrap.min.js",
            "./apps/website/static/javascripts/lib/scrolling-nav-1.0.1/js/jquery.easing.min.js",
            "./apps/website/static/javascripts/lib/scrolling-nav-1.0.1/js/scrolling-nav.js"])
    .pipe(concat('common.js'))
    .pipe(uglify())
    .pipe(gulp.dest('./apps/website/static/javascripts/dist/lib'))
});

gulp.task('lib', function() {
  gulp.src(["./apps/website/static/javascripts/lib/jquery/dist/jquery.js",
            "./apps/website/static/javascripts/lib/backbone-amd/backbone.js",
            "./apps/website/static/javascripts/lib/underscore-amd/underscore.js"])
    .pipe(uglify())
    .pipe(gulp.dest('./apps/website/static/javascripts/dist/lib'))
});

gulp.task('util', function() {
  gulp.src('./apps/website/static/javascripts/src/util/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('./apps/website/static/javascripts/dist/src/util'))
});

gulp.task('views', function() {
  gulp.src('./apps/website/static/javascripts/src/views/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('./apps/website/static/javascripts/dist/src/views'))
});

gulp.task('models', function() {
  gulp.src('./apps/website/static/javascripts/src/models/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('./apps/website/static/javascripts/dist/src/models'))
});

gulp.task('collections', function() {
  gulp.src('./apps/website/static/javascripts/src/collections/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('./apps/website/static/javascripts/dist/src/collections'))
});

gulp.task('watch', function() {
  gulp.watch('./apps/website/static/javascripts/src/collections/*.js', ['collections']);
  gulp.watch('./apps/website/static/javascripts/src/models/*.js', ['models']);
  gulp.watch('./apps/website/static/javascripts/src/views/*.js', ['views']);
  gulp.watch('./apps/website/static/javascripts/src/util/*.js', ['util']);
});

gulp.task('default', ['util', 'views', 'models', 'collections', 'common', 'lib', 'watch']);

