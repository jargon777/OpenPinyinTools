# OpenPinyinTools

This program is a personal program I am developing to put pinyin in subtitles.
At the moment this is a very basic program. SRT files in /parse are automatically read. At the moment only traditional/full charachters are searched for in the reference dictionary. Output is automatically written to /write. Output is a little buggy as if there are multiple readings of a particular phrase/hanzi the first is automatically chosen. (e.g. 了 is always rendered as le if it doesn't occur as part of another word).

Currently, when pinyin is added, it is added such that it appears below existing Chinese charachters (so you'll see both). Subtitles should also only have Chinese text in them (no English).

If you are interested in the script but it is too basic for you (or if you want simplified support), let me know and maybe I can build an exe for it.
muresan.matthew@gmail.com

Consider checking https://github.com/jargon777/OpenPinyinTools/tree/dev for the latest version.
