
# some essential tools
apt-get install -y --no-install-recommends build-essential cmake doxygen \
  g++ git octave python-dev python-setuptools wget mlocate


# qt5
apt-get install -y --no-install-recommends qtcreator qtcreator-data qtcreator-doc qtbase5-examples qtbase5-doc-html qtbase5-dev qtbase5-private-dev

# from reference
# apt-get install -y --no-install-recommends qt5-default minizip

# video codec
apt-get install -y --no-install-recommends ann-tools libann-dev            \
libassimp-dev libavcodec-dev libavformat-dev libeigen3-dev           \
libflann-dev libfreetype6-dev liblapack-dev libglew-dev libgsm1-dev             \
libmpfi-dev  libmpfr-dev liboctave-dev libode-dev libogg-dev libpcre3-dev       \
libqhull-dev libswscale-dev libtinyxml-dev libvorbis-dev libx264-dev            \
libxml2-dev libxvidcore-dev libbz2-dev


echo "deb http://deb.debian.org/debian `lsb_release -cs` non-free" >> /etc/apt/sources.list
apt update
apt-get install -y libfaac-dev


apt-get install -y --no-install-recommends libboost-all-dev libboost-python-dev


# install rapid json
cd /workspaces/mujin-open-challenge/dep
git submodule add https://github.com/Tencent/rapidjson.git
cd rapidjson && git checkout 7dddd054628e42ab973bdbd1f9ab94535beb4d03
mkdir build && cd build
cmake .. && make -j `nproc` && sudo make install
# if memcpy/memmove no trival copy contructor errors popped up, see
# readme file for a fix. 

apt-get install -y --no-install-recommends python2 curl
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
python2 get-pip.py
pip install ipython h5py numpy scipy wheel pyopengl

apt install -y python3-pip
pip3 install ipython h5py numpy scipy wheel pyopengl

# install pybind11
cd /workspaces/mujin-open-challenge/dep
git submodule add https://github.com/pybind/pybind11.git 
cd pybind11
mkdir build && cd build 
git remote add woody https://github.com/woodychow/pybind11.git 
git remote add cielavenir https://github.com/cielavenir/pybind11.git 
git fetch woody && git fetch cielavenir && git checkout v2.9.2
cmake .. -DPYBIND11_TEST=OFF -DPythonLibsNew_FIND_VERSION=2 
sudo make install

# !!! not tested with cherry pick yet
git cherry-pick 94824d68a037d99253b92a5b260bb04907c42355
git cherry-pick 98c9f77e5481af4cbc7eb092e1866151461e3508
