### wtfm

This repo shares my online documentation system, **wtfm**, which utilizes my
[aa_macro](https://github.com/fyngyrz/aa_macro)
project. **wtfm** is fully operational and I am using it for a number
of projects, so it's pretty stable.

The [documentation is here.](http://ourtimelines.com/wtfm/tocpage.html)
Unfortunately I couldn't do the documentation here on Github, because they
offer no support for repo-centric syntax highlighting, and they won't
accept a generally available syntax highlighting definition until hundreds
of repos use it. Forunately, in _this_ case, I'm documenting an actual documentation
system, so providing my own documentation serves as a lovely demo.

## About

**wtfm** resides on a \*NIX web server. It is CGI that allows you to
create and maintain online \(HTML, most likely, although it certainly
isn't limited to HTML\) documentation right on the server,
working in your browser. It is single creator, multiple client software;
by this I mean that document creation is designed to be a private
undertaking by the documentation author as a security matter, ideally
via https, while the resulting documentation itself can and most likely
will be shared; **wtfm**  can run in one location, and generate output
from any project into any directory you wish on a per-project basis
\(assuming you've set up your filesystem permissions accordingly\).

## Features

* Hugely customizable
* Extensive macro capability
* Styles allow global document changes with an absolute minimum of effort
* Full access to *all* of HTML and CSS
* Handles multiple documentation undertakings
* Global \(all projects\), doc-wide \(all pages\) and page-Local preset styles
* External document and style includes
* Glossary generation
* Multi-level TOC generation
* Index generation
* HTML Tables
* HTML Lists
* Variables
* Counters
* Data lists
* Data dictionaries
* Stack operations
* Math
* Base conversion
* Word wrapping
* Text alignment for fixed width fonts
* Conditional Content
* Character mapping
* Data Sorting
* Word expansion
* Various word casing modes
* Various numbering schemes \(Roman, etc.\)
* Footnote generation
* Endnote generation
* Images
* Links
* Side blocks \(left and/or right\)
* Note blocks
* Warning blocks
* Caution blocks
* Forward and Backward references \(multi-pass link resolution\)

...plus more

## Examples

### Examples of custom doc conventions
![Examples of custom doc conventions](http://fyngyrz.com/images/wtfmx1.png)

### Examples of custom blocks
![Examples of custom blocks](http://fyngyrz.com/images/wtfmx2a.png)

### Example of content using some of these features
![Example of document content](http://fyngyrz.com/images/wtfmx3.png)

### Example of content using images
![Example of images](http://fyngyrz.com/images/wtfmx4.png)

## Credit

### Author
Ben, AA7AS / fyngyrz

### Name
Credit for the name **wtfm** goes to `xxxJonBoyxxx` on Slashdot.
He just threw it out like it should have been obvious. It wasn't.
But it is now!

### mousetrap.js

I include, for your convenience, `mousetrap.js` by Craig Campbell. This
is a lovely little bit of cross-browser compatible javascript that
allows, among other things, reliable keyboard navigation of documents. I
use it in the `wftm` documentation, and I highly recommend you do as
well. There's a page in the manual about how to use
it [here.](http://ourtimelines.com/wtfm/mousetrap.html).
