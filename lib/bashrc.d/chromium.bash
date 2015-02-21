
# save some disk I/O on my SSD
# https://wiki.archlinux.org/index.php/Chromium_tweaks#Cache_in_tmpfs
if [ -e /etc/chromium/default ]; then
	source /etc/chromium/default
	export CHROMIUM_USER_FLAGS="${CHROMIUM_FLAGS} --disk-cache-dir=/tmp/${LOGNAME}-chromium-cache"
	unset CHROMIUM_FLAGS
fi
