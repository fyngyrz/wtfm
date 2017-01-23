# wftm BETA Changelog

### Note

This log reflects changes to the wftm documentation system. Other changes
such as to the associated utlitilies and sample files are not tracked here.

### Log
0.0.10
 * Search now does not require wrapping term with **

0.0.9
 * Page search now supports case sensitivity
 * Wildcards are now ? and * instead of annoying SQL _ and %

0.0.8
 * Page Content field now tracks content size as you type.

0.0.7
 * (multi-)password security implementation
 * (multi-)IP security implementation
 * [local ds_rawmode 1] in page locals triggers raw Page Content
 * - in Non-Default Exension skips ANY extension

0.0.6
 * Project editor "Page Editor List" link now opens new tab

0.0.5
 * if a page had no pagelocals, next/prev links would not be set, fixed

0.0.4
 * could create or update a blank project under some circumstances, fixed

0.0.3
 * Serious bug fixed wherre multiple projects were writing over each other when there were identically-named pages

0.0.2
 * Added search operator: % and _ wildcards, case insensitive
 * Removed anti-robot indexing from html401.dsys
 * wrapped nobreak around the Table Of Contents string in the tocmod1.dsys module

0.0.1
 * Support for [slit] and [vlit]
 * Added changelog.md to project
 * Improved npbar.dsys (now class instead of label... ooops)
 * mousetrap.js: added, README.md info, example in documentation
 * Updated aa_macro version
 * Updated users-guide.md
 * Updated doc_system.cfg
 * Moved configuration load nearer to front of doc_system.py
 * Updated documentation at http://ourtimelines.com/wtfm/tocpage.html

0.0.0
 * Initial release

