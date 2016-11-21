# Documentation System User's Guide (beta)

## User Manual - Where is it?

In the spirit of
"[eating my own dog food](https://en.wikipedia.org/wiki/Eating_your_own_dog_food)",
the actual user manual has been written using **wtfm** itself.

The [user manual is located here.](http://ourtimelines.com/wtfm/tocpage.html)

## Project Overview

This project provides a means to generate HTML documentation that
leverages my
[aa_macro language](https://github.com/fyngyrz/aa_macro/blob/master/users-guide.md).
This is very much a power-user's tool. If you're looking to create
complex, flexible online documentation, find markdown too limiting, and
writing HTML and CSS directly too low-level, this may be just the thing
for you. But let me warn you right up front: there's a learning curve in
stepping beyond basic use into where the real power lies.

aa_macro, and therefore this documentation system, let you define styles
that can turn any task into a simple one. Notice I didn't claim that
writing the styles themselves was always simple. :\) But once written,
yes, the work of actually preparing the documentation itself will become
much, much easier.

There are three CGI forms involved. One provides a means to specify
globals that apply to all projects. Another provides a way to specify
the globals that relate to specific projects. The last one provides a
way to build the actual pages in the project.

You can select from lists of projects, and within the context of a
project or a page within a project, from lists of pages/files within
that project.

Projects may be stand-alone in the sense that they only inherit from the
globals, or they may additionally inherit from a parent project. The
latter option provides a means to generate multiple streams of
documentation within the context of the same specific sets of styles.
You can also use a project specifically *as* a parent, that is, without
intending to generate pages directly from that project, in order to
serve as \(one of the\) parent\(s\) for multiple other projects. All
this while still inheriting the target project's globals and the
project-level specifics.

When you generate a project, the files generated, which will typically be a
web page or a CSS page, are processed this way:

 1. All-project globals are built
 2. If there is a parent project, those globals are built
 3. Project-specific globals are built
 4. For all files in the project:
   1. File-specific styles are built
   2. File is generated

## Security

To be at least somewhat secure, you need to do the following things:

* rename the `doc_system.py` file to new `something-really-obscure.py`
* rename the `doc_system.cfg` file to new `a-name-just-as-obscure.cfg`
* change the line in what was `doc_system.py` to the new `.cfg` name
* create a world-writable directory on your server with an obscure name
* Inside the newly renamed `.cfg` file:
    * change the `xsystem` variable to match the new `.py` name
    * change the `dprefix` variable to match the world-writable directory
    * change the `dname` variable to `another-very-obscure-db-name.db`

When all of this is done, you will access your new doc system by going to:

	`http://your-server.your-tld/your-cgi-location/something-really-obscure.py`

...or...

	`https://your-server.your-tld/your-cgi-location/something-really-obscure.py`

### Improving Security

If you'd like to add password protection to the whole system, that'd be
a good idea. I don't need it because I access only from within my LAN,
and there is no external path to the server -- so I punted. You can also
use https, and of course if your server is configured to do so, then you
should..
