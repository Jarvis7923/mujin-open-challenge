# mujin-open-challenge
 48-hour open challenge for mujin - robotic backend system engineer


### how to use
remember to add `--network host` to docker run command. 


open terminal and run 
```
flask run
```
this will open port at 5000


some "unit" test for each api, open another terminal and run
```
flask_test
```



### versions
* base image: `debian:bullseye`
* openrave: build from `/production` branch, commit `4da893c03d7e478eca48b719d23546e0e347557d`
* gcc: `gcc (Debian 10.2.1-6) 10.2.1 20210110`

### References


[build openrave on linux official guide](http://openrave.org/docs/latest_stable/coreapihtml/installation_linux.html)

[install gcc on debian 10](https://linuxize.com/post/how-to-install-gcc-compiler-on-debian-10/)

*no so useful for now. dependencies are manually installed*
[useful tools to add apt repositories from shell for debian 10](https://unix.stackexchange.com/questions/45879/how-to-add-repository-from-shell-in-debian) (**official image seems not supporting debian:bullseye at the point**)

*deb-multimedia.org repo seems having issues with gpg keys.* 
*also 3rd party software can damage the system as well.*
[some info about "no public key error with deb-multimedia.org repo"](https://forums.debian.net/viewtopic.php?t=134409)

*libfaac-dev is in the official debian package non-free repo*
[libfaac-dev](https://packages.debian.org/bullseye/libfaac-dev)

*rapidJSON memcpy/memmove error static pointer cast fix for higher version gcc*
[forked rapidJSON repo by smanders](https://github.com/smanders/rapidjson/commit/7a9096749bec93d1cea8cb92bf17346ac0437028)

*not always applicable to downgrade gcc version*
[debian forum](https://forums.debian.net/viewtopic.php?t=150273)

*error: Werror=shadow*. change the local argument's name and it can prevent the confliction. Assuming the production branch is not totally in prod? so I will change some local variable's name to prevent this breaking the build. 

*be careful with the git submodule deletion*
[how to remove a git submodule](https://stackoverflow.com/questions/1260748/how-do-i-remove-a-submodule)