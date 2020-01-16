import pipes

LOGS_STREAMER_FILE = "logstream"

def logsStreamerPath(ctx):
	return '%s/%s' % (pipes.quote(ctx['TMPDIR']), LOGS_STREAMER_FILE)

def configure(ctx):
	pass

def preprocess_commands(ctx):
	cmds = []
	cmds.append(('mkfifo', logsStreamerPath(ctx)))
	return cmds

def service_commands(ctx):
    return {
        "logpipe": ('tail', '-f', logsStreamerPath(ctx))
    }

def service_environment(ctx):
	return {
		'LOGS_STREAM': logsStreamerPath(ctx),
	}

def compile(install):
	return 0