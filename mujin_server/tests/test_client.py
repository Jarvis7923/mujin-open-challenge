#!/usr/bin/env python
import json
from pathlib import Path
from mujin_server.main import ROBOT_COLLECTION_BACKUP_PATH, ROBOT_COLLECTION_PATH


def test_upload_robot_by_file(client):
    response = client.post("/api/robot",
                           data={
                               "file": ((ROBOT_COLLECTION_BACKUP_PATH /
                                         "test.json").open("rb"), 'test.json',
                                        'text/plain')
                           },
                           follow_redirects=True)

    obj = json.load((ROBOT_COLLECTION_BACKUP_PATH / "test.json").open("rb"))
    assert obj == json.load((ROBOT_COLLECTION_PATH / "test.json").open("rb"))
    assert response.status_code == 200


def test_bad_request_if_upload_robot_without_filename(client):
    response = client.post("/api/robot",
                           data={
                               "file":
                               ((ROBOT_COLLECTION_BACKUP_PATH /
                                 "test.json").open("rb"), '', 'text/plain')
                           },
                           follow_redirects=True)
    print(response.json)
    assert response.status_code == 400


def test_get_robot_by_filename(client):
    client.post("/api/robot",
                data={
                    "file":
                    ((ROBOT_COLLECTION_BACKUP_PATH / "test1.json").open("rb"),
                     'test1.json', 'text/plain')
                },
                follow_redirects=True)
    obj = json.load((ROBOT_COLLECTION_PATH / "test1.json").open("rb"))
    response = client.get("/api/robot/test1.json", follow_redirects=True)

    assert response.status_code == 200
    assert response.json["payload"] == obj


def test_bad_reqeust_if_download_file_not_exist(client):
    response = client.get("/api/robot/test1.json/download",
                          follow_redirects=True)

    assert response.status_code == 400


def test_download_robot_by_filename(client):
    client.post("/api/robot",
                data={
                    "file":
                    ((ROBOT_COLLECTION_BACKUP_PATH / "test1.json").open("rb"),
                     'test1.json', 'text/plain')
                },
                follow_redirects=True)

    response = client.get("/api/robot/test1.json/download",
                          follow_redirects=True)

    assert response.status_code == 200


def test_delete_robot_by_filename(client):
    client.post("/api/robot",
                data={
                    "file":
                    ((ROBOT_COLLECTION_BACKUP_PATH / "test1.json").open("rb"),
                     'test1.json', 'text/plain')
                },
                follow_redirects=True)

    response = client.delete("/api/robot/test1.json", follow_redirects=True)

    assert response.status_code == 200
    assert not (ROBOT_COLLECTION_PATH / 'teset1.json').exists()


def test_update_robot_field_by_filename(client):
    client.post("/api/robot",
                data={
                    "file":
                    ((ROBOT_COLLECTION_BACKUP_PATH / "test1.json").open("rb"),
                     'test1.json', 'text/plain')
                },
                follow_redirects=True)

    new_obj = {"hello": 200, "new": 1}

    response = client.put("/api/robot/test1.json",
                          json=new_obj,
                          follow_redirects=True)
    assert response.status_code == 200

    obj = client.get("/api/robot/test1.json",
                     follow_redirects=True).json["payload"]
    assert obj == new_obj


def test_get_robots(client):
    # flask redirects
    response = client.get("/api/robot", follow_redirects=True)
    assert response.status_code == 200
