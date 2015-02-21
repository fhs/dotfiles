#!/bin/bash

source /etc/profile

# unset RHEL defaults
unset LS_COLORS
unalias -a

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

ulimit -S -c 0
umask 0022
unset HISTFILE
alias vi=vim

export EDITOR=vim
export VISUAL=$EDITOR
export PAGER=less
export LESS="-iR $LESS"
export LESSHISTFILE=/dev/null

case "$HOSTTYPE" in
	i[456]86) objtype=386 ;;
	x86_64) objtype=amd64 ;;
	*) objtype=unknown ;;
esac
[ -d $HOME/bin ] && PATH=$HOME/bin:$PATH
[ -d $HOME/bin/sh ] && PATH=$HOME/bin/sh:$PATH
[ -d $HOME/bin/$objtype ] && PATH=$HOME/bin/$objtype:$PATH
export PATH

# Set up terminal window title
case "$TERM-$LOGNAME" in
linux-*)
	unset PROMPT_COMMAND
	;;
*-root)
	export PROMPT_COMMAND='printf "\033]0;%s@%s:%s\007" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/~}"'
	;;
*)
	export PROMPT_COMMAND='printf "\033]0;%s:%s\007" "${HOSTNAME%%.*}" "${PWD/#$HOME/~}"'
	;;
esac

if [ "$LOGNAME" = "root" ]; then
	export PS1="\h# "
else
	export PS1="\h=; "
fi

# "local cd" -- grep for directory to cd into
lcd () {
	if [ $# -lt 1 ]; then
		\cd
		return
	fi
	case "$1" in
		/*)
			\cd $1
			return
		;;
	esac
	
	dir="$(ls -d */ | grep -i $1 | sed 1q)"
	if [ -z "$dir" ]; then
		echo $1: no match
		return 1
	fi
	echo cd "$dir"
	\cd "$dir"
}


# Host specific configs
if [ -x ~/lib/bashrc.host/${HOSTNAME}.bash ]; then
	source ~/lib/bashrc.host/${HOSTNAME}.bash
fi

# Program specific configs
for f in ~/lib/bashrc.d/*; do
	if [ -x "$f" ]; then
		source $f
	fi
done
