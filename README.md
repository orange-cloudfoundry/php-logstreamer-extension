# Php-logstreamer-extension

A [php-buildpack](https://github.com/cloudfoundry/php-buildpack) extension for cloud foundry to handle logs better than with php-fpm output.

## Why ?

There is 3 reasons to use another method to forward log to stdout when using php-buildpack:
1. By default, php-fpm doesn't forward output from its child to stdout and in the php-buildpack you need to tweak the `php-fpm.conf` to uncomment the line `catch_workers_output = yes`.
2. Php-fpm add a prefix (with child id) on each message which is annoying for reading and parsing.
3. Php-fpm truncate a long log message (see: https://github.com/docker-library/php/issues/207 )

For points 3 a fix is coming but not yet even merged, see: https://github.com/php/php-src/pull/1076

## Usage

You will need to import this repo to your app folder in the `.extensions` folder, to do so:

- **If your app is a git repo**: `git submodule add https://github.com/orange-cloudfoundry/php-logstreamer-extension.git .extensions/php-logstreamer-extension`
- **If your app is not a git repo**: `git clone https://github.com/orange-cloudfoundry/php-logstreamer-extension.git .extensions/php-logstreamer-extension`

In the next cf push this extension will be loaded.

You will have now have to write your logs on the file path given by the env var `LOGS_STREAM`, example:

```php
<?php 
file_put_contents($_ENV['LOGS_STREAM'], "THIS IS an app log\n"); // you should see, after hitting your page, in cf logs this line without prefix.
```