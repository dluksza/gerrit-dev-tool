# Gerrit Dev Tool (grdt)

## About

[Gerrit](https://www.gerritcodereview.com/) Dev Tool is a standalone tool to simplify Gerrit development. It does not depend on any Gerrit, Bazel or JDK version. Instead, it uses Python to evaluate and understand Bazel `BUILD` and  Gerrit configuration files.

The main purpose of it is to automate and simplify the tedious parts of Gerrit plugin development. Instead of manually managing Gerrit and plugin versions, `external_plugin_deps.bzl`, `plugins.bzl`, plugin repositories and configurations use a command line interface to get it done in one or two commands instead.

## Installation

### Pre-requirements

`grdt` can not ensure (yet) that your system is properly configured for Gerrit development. It still requires:
 * git
 * Bazel
 * JDK
 * Python3 (Python 3.11 dependent)

being installed in your system. See [Gerrit dev documentation](https://gerrit-review.googlesource.com/Documentation/dev-bazel.html#installation) for reference.

Additionally, as `grdt` is not (yet) distributed as PYPI package you'll need to clone this repository first, then do
```console
$ pip install .
```
for normal installation or
```console
$ pip install --editable .
```
if you want your code changes being immediately reflected in the cli.

From this point, you can run `grdt` command anywhere in your system.

# Initial setup

Before you can leverage any of `grdt` magick you need to create its workspace by calling:
```console
$ grdt setup
```
which will:
 * create workspace directory structure,
 * clone Gerrit (including submodules),
 * install the `commit-msg` hook,
 * synchronise Bazel dependencies,
 * build Gerrit,
 * create the test site.

Depending on your internet connection and hardware, this step can take some time.

When it finishes, you can navigate to `gerrit-workspace/` directory (with the `--name` argument an alternative name can be provided). From this point, you can use all of the `grdt` powers in that directory!

# Usage

## `grdt config`

Configure Gerrit test site from anywhere in the workspace!

By default `grdt config` will open `gerrit_testsite/etc/gerrit.config` for editing. When used with an additional `name` argument it will open that file from `gerrit_testsite/etc/` directory eg. `grdt config secure.config` will open `gerrit_testsite/etc/secure.config`

## `grdt run/start/stop`

Start Gerrit from anywhere in the workspace.

The `run` subcommand will start Gerrit in the foreground, whereas `start` will do the same in the background, then use `stop` to stop that background instance.

This is equivalent to manually running `gerrit_testsite/bin/gerrit.sh run/start/stop` manually.

## Plugin administration

### `grdt plugins install`

_Simply_ install Gerrit plugin.

This is probably the most powerful command of `grdt` as it will do many things at once.

Running `grdt plugins install virtualhost` will:
 * clone the plugin (and install `commit-msg` hook) if it isn't cloned yet
 * install any other plugins that `virutalhost` depends on (if any)
 * checkout compatible plugin version
 * create a symbolic link in `gerrit/plugins/`
 * update `gerrit/plugins/external_plugin_deps.bzl`
 * update `gerrit/tools/bzl/plugins.bzl`
 * run `gerrit/tools/eclipse/project.py`
 * build the plugin
 * update Gerrit test site configuration
 * deploy plugin JAR to `plugins/` directory (or `lib/` when dealing with lib modules)

### `grdt plugins uninstall`

_Simply_ uninstall Gerrit plugin.

This will undo all of the changes that `install` sub-command did, meaning:
 * remove symbolic link from `gerrit/plugins/`
 * remove any external dependencies for that plugin from `gerrit/plugins/external_plugin_deps.bzl`
 * remove that plugin from `gerrit/tools/bzl/plugins.bzl`
 * update Eclipse project
 * remove configuration entries added to `gerrit.config` 
 * remove the plugin JAR file from the Gerrit site

Note:
This will not uninstall the other plugins that this plugin may depend on.

### `grdt plugins deploy`

Build and deploy plugin.

This does just a third of the `install` sub-command, as it will just run a plugin build, and copy the resulting JAR into the test site.

### `grdt plugins clean`

Uninstall all of the plugins.

Cleans up Gerrit workspace and test site. Removes all symbolic links from `gerrit/plugins/`, all plugin JARs from the test site, all `gerit.config` entries are removed and `external_plugin_deps.bzl`, `plugins.bzl` are reverted. Leaving you with a clean Gerrit workspace and test site.

## Switching between Gerrit versions

`grdt checkout` lets you switch the whole workspace between different Gerrit versions.

Running `grdt checkout stable-3.8` will:
* checkout Gerrit's `origin/stable-3.8` branch
* switch `gerrit_testsite/` to `sites/stable-3.8` if it exists, if not:
	* will build Gerrit
	* initialise fresh test site in `sites/stable-3.8`
	* switch `gerrit_testsite/` to `sites/stable-3.8`
* for each installed plugin it will:
	* checkout compatible version
	* update `external_plugin_deps.bzl` and `plugins.bzl`
	* update `gerrti.config`
	* deploy plugin to the test site

## Test site administration

### `grdt sites snapshot`

Creates a snapshot of the current test site.

It will simply copy the current Gerrit test site with a given name. This is useful when a complicated Gerrit setup is required for bug replication or feature testing. The copy can be then used as a starting point for another round of testing.

### `grdt sites switch`

Updates the `gerrit_testsite/` symbolic link.

This will just update the symbolic link to point to a given test site name. This is useful when testing migration between Gerrit versions, when after `grdt checkout $next_version` you can run `grdt sites switch $previous_version` and run the migration.

# Plugin auto-configuration

The aim of `grdt` is to provide the required parts of `gerrit.config` for plugins. Things like `gerrit.installModule` or `http.filterClass` _should_ be automatically added by `grdt`. But this relies on the resources distributed together with the `grdt` code, if you find anything missing, please do [contribute](#contributing) it!

For custom configurations like `sites` for `virtualhost` or `download` section for `download-commands` plugin (or your closed-sourced plugin) there's a way of extending `grdt` with so-called _recipes_.

Currently `grdt` will read `recipes/$plugin_name/$version/etc/gerrit.config` when `$plugin_name` is installed (or uninstalled) and will merge it with existing `gerrit_testsite/etc/gerrit.config`.

The `$version` folder name should be either version number (`${major}.${minor}`) or `master`. See _[version negotiation](#version-negotiation)_ for more information.

For example, to automatically add `server` section when `virutalhost` plugin is installed create a `gerrit.config` file in `recipes/virtualhost/master/etc/` with content:
```
[server "second.localhost"]
	projects = second/*
```

# Version negotiation

By convention, Gerrit is using `stable-x.y` branch names for the released versions. `grdt` is leveraging that convention heavily. It will always use `origin/stable-x.y` when `grdt checkout` is used.

It also expects plugins to follow that convention.

Some of the plugins can be compatible with multiple Gerrit versions. This means that although the exact branch is not found we can still successfully use the previous version or `master` branch.

This is where the _version negotiation_ comes into play. `grdt` will try to figure out a compatible branch using a simple heuristic:
 * use that branch when there's an exact match
 * use the closest previous version when there's no match eg. when the plugin has `stable-3.2` and `stable-3.4` and Gerrit is in version `3.3`, `grdt` will pick `stable-3.2` as compatible
 * use `master` when the last compatible version will be picked, eg. when the plugin has `stable-3.1` and `stable-3.2` and Gerrit is in version `3.5`, `grdt` will pick `master` as compatible
 * otherwise use `master`

The same heuristics apply to the [user-defined configuration](#plugin-auto-configuration) file in the `recipes/` directory.

# Limitations

The Gerrit and its plugins are complex beasts, the automated approach may not always work! Here are the known limitations, but more may be discovered over time or some of them may be overcome.

 * For now, only Bazel "in-tree" plugins are supported.

 * Only plugins that produce a single JAR file can be automatically installed. `grdt` will always pick the JAR file from the Bazel output directory that has a matching name with the plugin.

 * All comments in `gerrit.config` will be removed when any sub-command that is touching that file is run.

 * When any of the `gerrit.config` options that were added by `grdt plugins install` will be manually changed, it will not be removed by `grdt plugins uninstall`. The uninstall process will only remove options that have **exactly** the same, section, subsection and value.

 * Only Gerrit open-source plugins can be automatically cloned. You can always manually clone your plugin into `plugins/` or `modules/` directory and use it with `grdt`.

 * Using `grdt checkout` will leave your repository in the _[detached HEAD](https://git-scm.com/docs/git-checkout#_detached_head) state_. Gerrit Dev Tool is always checking out the remote branches (eg. `origin/stable-3.9`) which will result in _detached HEAD_, for more information. 

# Contributing
Contributions can be pushed for review on [GerritHub.io](https://review.gerrithub.io/q/repo:dluksza/gerrit-dev-tool).

Login with your GitHub account into GerritHub.io. Once logged in you can clone the repository and `commit-msg` hook using (**do not forget to replace `$login` in the URL**):
```console
$ git clone "https://$login@review.gerrithub.io/a/dluksza/gerrit-dev-tool" && (cd "gerrit-dev-tool" && f=`git rev-parse --git-dir`/hooks/commit-msg ; mkdir -p $(dirname $f) ; curl -Lo $f https://review.gerrithub.io/tools/hooks/commit-msg ; chmod +x $f)
```
Instead of cloning, you can also add `review` remote:
```console
$ git remote add review https://$login@review.gerrithub.io/a/dluksza/gerrit-dev-tool
```
do not forget to replace `$login` with your account name and install `commit-msg` hook.

Then push to the desired branch.
```console
$ git push review HEAD:refs/for/master

```
