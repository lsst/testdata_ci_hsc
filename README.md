ci_hsc
======

ci_hsc is test data used to exercise the LSST Stack.

git-lfs
-------

ci_hsc stores large files using [git-lfs](https://git-lfs.github.com/). To use ci_hsc you must install git-lfs and configure it. LSST runs its own git-lfs server and storage service.

There is **no password required** for cloning or pulling from LSST's git-lfs server, but it is recommended that you use a [credential helper](https://help.github.com/articles/caching-your-github-password-in-git/) to avoid being prompted for a username and password repeatedly.

If you are a member of the lsst GitHub organization, then you may push using git-lfs. To push, you should login using your GitHub username and password (or [token for 2FA users](#token)) to the git-lfs server (git-lfs.lsst.codes).

If you are using [GitHub's two-factor authentication (2FA)](https://help.github.com/articles/about-two-factor-authentication/), use a personal access token instead of your GitHub password.
You can create a token specifically for `git-lfs.lsst.codes` by going to [https://github.com/settings/tokens](https://github.com/settings/tokens). Tokens for our gitLFS service only require read:org scope. If you have not been using https already for Github, and have 2FA turned on, you will want another public_repo scope token for Github access (as opposed to access to our gitLFS service - a transaction with each happens during a push). You might want to test using https access with your Github repos first with a non-LFS repo to avoid confusion. 


Setting up git-lfs for the first time
-------------------------------------

There is a small amount of one-time setup to use git-lfs for any project on your computer.

### Mac OS X

```bash
brew install git-lfs
git config --global credential.helper osxkeychain
git config --global lfs.batch false
git lfs init
```

The ``osxkeychain`` helper will store your password/token securely in OS X's keychain; you'll never have to worry about it again.

### Linux

[Download and install](https://github.com/github/git-lfs/releases/tag/v1.0.0) the current git-lfs.

```bash
git config --global credential.helper cache # A credential helper is highly recommended.
git config --global lfs.batch false
git lfs init
```

The ``cache`` credential helper will remember your password for 15 minutes by default; long enough to clone a repository.

### First Clone

Once git-lfs is installed and configured, clone an lfs-enabled repository such as this one with the HTTPS protocol:

```bash
git clone https://github.com/lsst/ci_hsc.git
```

`git clone` will ask you to authenticate to our git-lfs server:

```bash
Username for 'https://git-lfs.lsst.codes': <GitHub Username OR Blank>
Password for 'https://<git>@git-lfs.lsst.codes': <GitHub password, token OR Blank>
```

* If you are only interested in cloning or pulling, the 'Username' and 'Password' can be blank.
* If you are a member of the LSST GitHub organization, then you can use your GitHub username and password.
* If you *also* have [GitHub's two-factor authentication](https://help.github.com/articles/about-two-factor-authentication/) enabled, use a personal access token instead of a password. You can setup a personal token at [https://github.com/settings/tokens](https://github.com/settings/tokens).

Finally, the git clone will ask you to authenticate to `s3.lsst.codes`:

```bash
Username for 'https://s3.lsst.codes': <Empty>
Password for 'https://s3.lsst.codes': <Empty>
```

There is no username or password for LSST's S3 service.

Using this git-lfs enabled repo
-------------------------------

*Just use this repo as you normally would any other repo.*
All of the regular git commands just work.

If you use the ``cache``-based credential helper, you will likely need to go through the authentication steps we did previously when you ``git push``.
See our note below on credential helpers.

Tracking new files types
------------------------

If you want to know what types of files are being stored in git-lfs, view the ``.gitattributes`` file in the repo.

If there is a new type of file you'd like to have stored in git-lfs, just run

```bash
git lfs track "*.ext"
```

where ``ext`` is the file's extension.

Make sure you ``git add`` and ``git commit`` changes to the ``.gitattributes`` file.


<a href="cred-helpers"></a>Credential Helpers
---------------------------------------------

GitHub has excellent documentation on configuring [credential helpers](https://help.github.com/articles/caching-your-github-password-in-git/).

If you do not use a credential helper, git-lfs will repeatedly ask for your username and password/[token](#token). This can be very frustrating. To avoid globally installing a credential helper, use git's cache credential helper. By default, it will work for 15 minutes before expiring.

```
git config --global credential.helper cache
```

If your home directory is on a network filesystem, you may need to specify a local filesystem for the cache's socket: "`git config --global credential.helper 'cache --socket /path/to/local/dir/.git-credential-socket'`"


LICENSE
-------

See the LICENSE file.
