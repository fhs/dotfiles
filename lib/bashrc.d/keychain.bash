
if which keychain >/dev/null 2>&1; then
	keychain -Q -q --agents ssh --noask
	[[ -f $HOME/.keychain/$HOSTNAME-sh ]] && source $HOME/.keychain/$HOSTNAME-sh
fi
