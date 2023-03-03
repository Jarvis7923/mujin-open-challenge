
cd /workspaces/mujin-open-challenge/mujin_server && pip install .
cp /workspaces/mujin-open-challenge/.devcontainer/.bashrc /root/.bashrc
cd /workspaces/mujin-open-challenge
source /root/.bashrc

flask run