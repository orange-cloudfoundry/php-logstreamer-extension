# Php-logstreamer-extension

A [php-buildpack](https://github.com/cloudfoundry/php-buildpack) extension for cloud foundry to handle logs better than with php-fpm output.

:warning: On php 7.3 and higher you can simply set a fpm config as defined [here](#fpm-config-php-73) and this extension will be unecessary :warning:


## Why ? 

There is 3 reasons to use another method to forward log to stdout when using php-buildpack:
1. By default, php-fpm doesn't forward output from its child to stdout and in the php-buildpack you need to tweak the `php-fpm.conf` to uncomment the line `catch_workers_output = yes`.
2. Php-fpm add a prefix (with child id) on each message which is annoying for reading and parsing.
3. Php-fpm truncate a long log message (see: https://github.com/docker-library/php/issues/207 )

For points 3 a fix is coming but not yet even merged, see: https://github.com/php/php-src/pull/1076

**UPDATE**: You can remove now the prefix and the log limit on PHP 7.3 and higher see [here](#fpm-config-php-73) to configure your php without this extension.

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

## Fpm config PHP >=7.3


:warning: **When using this configuration you must not install this buildpack extension** :warning:

Php fom configuration has new options for logs which achieve the same goal and let you write stdout as normal, these options are: `decorate_workers_output` and `log_limit` (see https://www.php.net/manual/en/install.fpm.configuration.php for more information).

Let's see how to configure:
1. create a directories structure in the app root: `.bp-config/php/fpm.d` (.e.g: `mkdir -p .bp-config/php/fpm.d`)
2. Place a `logs.conf` file in the `.bp-config/php/fpm.d` directory with this content:
```conf
[www]
catch_workers_output = yes
decorate_workers_output = no

[global]
log_limit = 100000
```
Details:
  - **log_limit**: Bigger log limit for avoid truncating
  - **catch_workers_output**: Retrieve logs from stdout in workers
  - **decorate_workers_output**: Remove prefix
3. You can now write in stdout without worrying:
```php
<?php 
file_put_contents("php://stdout", "THIS IS an app log\n"); // you should see, after hitting your page, in cf logs this line without prefix.
```
