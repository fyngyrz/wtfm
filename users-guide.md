# Documentation System User's Guide (beta)

**Note:** I'm working specifically on repo-targeted documentation now. The
project is not yet in the repo. I will place the actual project in the
repo once I get far enough along here. Please be patient with me on
this.

## Overview

This project provides a means to generate HTML documentation that
leverages the power of my aa_macro language. This is very much a
power-user's tool. If you're looking to create complex, flexible online
documentation, find markdown too limiting, and writing HTML and CSS
directly too low-level, this may be just the thing for you. But let me
warn you right up front: there's a learning curve in stepping beyond
basic use into where the real power lies.

aa_macro, and therefore this documentation system, lets you define
styles that can turn any task into a simple one. Notice I didn't claim
that writing the styles themselves was guaranteed to be simple. :\) But
once written, yes, the work of actually preparing the documentation
itself will become much, much easier.

There are three forms involved. One provides a means to specify globals
that apply to all projects. Another provides a way to specify the
project itself. The last one provides a way to build the actual
pages in the project.

When you generate a project, the files generated, which is typically a
web page or a CSS page, are processed this way:

 1. All-project globals are built
 2. Project-specific globals are built
 3. For all files in the project:
   1. File-specific styles are built
   2. File is generated

### Globals

You can define four types of globals:

 1. Global variables \( **`[global variableName Content]`** \)
 2. Global styles \( **`[gstyle styleName styleContent]`** \)
 3. Global lists - quite a few  ways exist to produce lists
 4. Global dictionaries \( **`[dict dictName]`** and/or **`[dset (sep=X,)dictName,keyXvalue]`** \)

These apply as described above; once defined, they remain defined until
they are re-defined. Re-definition can also re-define them to do
nothing.

Globals are useful for tasks and items that span the breadth of your
project. If you want to create useful styles that you can use in
multiple projects, that's what the All-project globals are for.

When you have styles you want to use in a specific project, for instance
how a specific project's web pages will be formatted, you use the
project specific globals to define those.

Lists and dictionaries don't have local forms in the sense of where in
the project they are visible. However, if you define a list or a
dictionary on the tenth file/page of a project, it will not be visible
to the previous nine files as they have already been processed.

Typically then, you'll define lists and doctionaries in the global and
project-specific forms if you want them to be seen by every page in your
project, and only on a specific page when they are only relevant to that
page, keeping in mind that they do persist from then on and so will have
to be re-defined if you want to use the same list or dictionary
elsewhere with different contents.

### Locals

Technically, you can define locals in the global and project spefific forms,
they just won't *do* anything. They are only used in the page-specific environment.

There are two forms of locals:

 1. Local variables \( **`[local variablename variableContent]`** \)
 2. Local styles \( **`[style styleName styleContent]`** \)
 
## Variable Invocation

There are three forms of variable invocation. One specifically only
looks at locals, one specifically only looks at globals, and one
looks at locals, and if a local of that name does not exist, then
it looks at globals.

## Style invocation

There are also three forms of style invocation, as well as a convenience
that duplicates one of them:

 1. Use global style: **`[glos styleName( content)]`**
 2. Use local style: **`[locs styleName( content)]`**
 3. Use localstyle , or if does not exist, use global: **`[s styleName( content)]`**  
 or: **`{styleName( content)}`**
