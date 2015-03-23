
if [ -n "$PLAN9" -a -d "$PLAN9" ]; then
	export PATH=$PATH:$PLAN9/bin
	export font=$PLAN9/font/fixed/unicode.9x18.font
	export tabstop=4
	export mousescrollsize=30%
	export BROWSER=chromium	# web(1)
	export NPROC=$(grep '^processor' /proc/cpuinfo | wc -l)	# mk(1)
	
	export NAMESPACE="/tmp/ns.${LOGNAME}.:0"	# for goplan9
	if [ ! -e $NAMESPACE ]; then
		mkdir $NAMESPACE
	fi
	
	if [ "$TERM" = "dumb" -a -n "$termprog" ]; then	# acme or 9term
		set +o emacs
		export PAGER=nobs
		export EDITOR=E
		export VISUAL=$EDITOR

		unset PROMPT_COMMAND
		alias cd=_cd
		_cd () {
			\cd "$@" && awd
		}
		awd
	fi
	
	if ! 9p ls plumb &>/dev/null; then
		export EDITOR=ed
		export VISUAL=$EDITOR
	fi

	# postscript fonts from Plan 9
	if [ "$GS_FONTPATH" = "" ]; then
		export GS_FONTPATH=$HOME/lib/psfonts
	else
		export GS_FONTPATH=$GS_FONTPATH:$HOME/lib/psfonts
	fi

	# lc in the system is mono compiler
	alias lc="$PLAN9/bin/lc"
fi
