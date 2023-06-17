const mix = require("laravel-mix");

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

mix
  .js("app/templates/assets/js/src/index.js", "app/static/js")
  .postCss("app/templates/assets/js/src/index.css", "app/static/css", [
    require("tailwindcss"),
  ]);
