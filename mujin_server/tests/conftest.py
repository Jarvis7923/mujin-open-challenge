import pytest
from mujin_server.main import create_app, ROBOT_COLLECTION_PATH, WORKSPACE_PATH, ROBOT_COLLECTION_BACKUP_PATH


@pytest.fixture()
def app():
    app = create_app()
    # app.config.update({
    #     "TESTING": True,
    # })

    # other setup can go here

    yield app
    # clean up / reset resources here

    for fn in ROBOT_COLLECTION_PATH.glob('*.json'):
        fn.rename(ROBOT_COLLECTION_BACKUP_PATH / fn.name)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):

    yield

    for fn in ROBOT_COLLECTION_PATH.glob('*.json'):
        fn.rename(ROBOT_COLLECTION_BACKUP_PATH / fn.name)
