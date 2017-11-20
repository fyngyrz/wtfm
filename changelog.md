# wftm BETA Changelog

### Note

This log reflects changes to the wftm documentation system. Other changes
such as to the associated utilities and sample files are not tracked here.

### Log
0.0.21
 * single quote color in forms, previewer

0.0.20
 * Removed visible demo text in forms, replaced with button
 * added clear button
 * Updated stand-alone previewer likewise

0.0.19
 * Changed HTML angle bracket colors in previewer and forms

0.0.18
 * HTML / aa-macro previewer improved
 * added stand-along previewer HTML page

0.0.17
 * HTML / aa-macro previewer improved

0.0.16
 * HTML / aa-macro previewer added

0.0.15
 * new `aa_formboiler.py`
 * `editdb.py` added for database maintainance - BE CAREFUL: BACKUP old db first!
 * Pages can now be locked out of renumbering.

If you have not previously been using **wtfm**, you can ignore the following.

Version 0.0.15 **REQUIRES** editing any existing database from version 14 or earlier.

I have provided `editdb.py` to help you perform this process.
You must copy `editdb.py` and `aa_qslite.py` to the directory where
your database reside.

First, **BACK UP YOUR CURRENT DATABASE** by copying it to a different name

The following assumes `docsystem.db`
is your db name... alter that if not.

Enter these commands at the shell prompt:

> `cd DIRECTORY_WHERE_DATABASE_RESIDES`
> `./editdb.py`
> `db=docsystem.db`
> `qs=alter table pages add column noreseq default 0`
> `x`
> `q`

Your old database is now compatible with 0.0.15

0.0.14
 * tocmod1.dsys now supports all 6 levels of HTML headings
 * latest aa-macro.py

0.0.13
 * Project Editor now tracks character count in style block

0.0.12
 * Renumber bug where identical page names cause renumber in multiple projects fixed
 * improved HTML in page list generation
 * Latest support libraries

0.0.11
 * Warning messages when page save fails because:
    * specified project does not exist
    * project name is blank
	* page name is blank

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

