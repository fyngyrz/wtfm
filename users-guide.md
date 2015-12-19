# Documentation System User's Guide (beta)

**Note:** I'm working specifically on repo-targeted documentation now. The
project is not yet in the repo. I will place the actual project in the
repo once I get far enough along here. Please be patient with me on
this.

## Overview

This project provides a means to generate HTML documentation that
leverages the power of my aa_macro language. This is very much a
power-user's tool. If you're looking to create complex, flexible online
documentation, and fine markdown too limiting, and writing HTML and CSS
directly too low-level, this may be just the thing for you. But let me
warn you right up front: there's a learning curve in stepping beyond
basic use into where the real power lies.

aa_macro, and therefore this documentation system, lets you define
styles that can turn any task into a simple one. Notice I didn't claim
that writing the styles themselves was guaranteed to be simple. :\) But
once written, yes, the work of actually preparing the documentation
itself will become much, much easier.

There are three forms involved. One provides a means to specify golbals
that apply to all projects. Another provides a way to specify the
project itself. The last one provides a way to build the actual
pages in the project.

When you generate a project, each file generated, which is typically a
web page or a CSS page, is processed this way:

 1. Globals are built
 1. Project-specifics are built
 1. File-specific styles are built
 1. File is generated



