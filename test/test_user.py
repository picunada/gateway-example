from app.models.user import UserInDb, Roles, UserOut
from .test_base import db, client, user


class TestUser:
    def test_user_creation(self, client, user):
        response = client.post(
            "/api/v1/user", headers={"content-type": "application/json"}, json=user
        )

        assert response.status_code == 201

    def test_user_creation_not_valid_email(self, client):
        user = dict(
            email="testcom", username="test", password="password", password2="password"
        )
        response = client.post(
            "/api/v1/user", headers={"content-type": "application/json"}, json=user
        )

        assert response.status_code == 422

    def test_user_creation_passwords_not_match(self, client):
        user = dict(
            email="test@example.com",
            username="test",
            password="password2",
            password2="password",
        )
        response = client.post(
            "/api/v1/user", headers={"content-type": "application/json"}, json=user
        )

        assert response.status_code == 422
        assert "loc" in response.json()["detail"][0].keys()
        assert (
            "Value error, Passwords do not match" == response.json()["detail"][0]["msg"]
        )

    def test_user_get(self, client, user):
        blacklist = db.client.get_database("mt-services")["blacklist"]
        blacklist.delete_many({})
        users = db.client.get_database("mt-services")["users"]
        users.update_one({"email": "test@example.com"}, {"$set": {"role": "admin"}})

        auth = client.post(
            "/api/v1/auth/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=dict(
                username=user["email"], password=user["password"], scope=["read"]
            ),
        )

        assert auth.status_code == 200
        assert auth.json()["access_token"] is not None

        get = client.get(
            "/api/v1/user",
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
        )

        assert get.status_code == 200
        assert len(get.json()["results"]) != 0

    def test_user_get_one(self, client, user):
        users = db.client.get_database("mt-services")["users"]
        user_data = users.find_one({"email": "test@example.com"})
        user_data = UserOut.model_validate(user_data)

        auth = client.post(
            "/api/v1/auth/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=dict(
                username=user["email"],
                password=user["password"],
                scope=["read", "write"],
            ),
        )

        assert auth.status_code == 200
        assert auth.json()["access_token"] is not None

        get_one = client.get(
            f"/api/v1/user/{user_data.id}",
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
        )

        data = user_data.model_dump_json(by_alias=True).strip().lower()
        response = str(get_one.json()).replace("'", '"').replace(" ", "").lower()

        assert get_one.status_code == 200
        assert response == data

        get_one_invalid_id = client.get(
            f"/api/v1/user/1234",
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
        )

        assert get_one_invalid_id.status_code == 404
        assert get_one_invalid_id.json()['detail'] == "Invalid ID should be 12-byt hex string"

        not_found = client.get(
            "/api/v1/user/737f2466c578e69ac37c0fd5",
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
        )

        assert not_found.status_code == 404
        assert not_found.json() == {"detail": "User not found"}

    def test_user_update(self, client, user):
        users = db.client.get_database("mt-services")["users"]
        user_data = users.find_one({"email": "test@example.com"})
        user_data = UserInDb.model_validate(user_data)

        auth = client.post(
            "/api/v1/auth/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=dict(
                username=user["email"],
                password=user["password"],
                scope=["read", "write"],
            ),
        )

        assert auth.status_code == 200
        assert auth.json()["access_token"] is not None

        update = client.put(
            f"/api/v1/user/{user_data.id}",
            headers={
                "content-type": "application/json",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
            json=dict(
                email="test@example.com",
                username="test",
                first_name="test",
                last_name="test",
            ),
        )

        response = update.json()

        assert update.status_code == 200
        assert response["first_name"] == "test"
        assert response["last_name"] == "test"

        not_found = client.put(
            "/api/v1/user/44727769ed122ffe12a8335d",
            headers={
                "content-type": "application/json",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
            json=dict(
                email="test@example.com",
                username="test",
                first_name="test",
                last_name="test",
            ),
        )

        assert not_found.status_code == 404
        assert not_found.json()['detail'] == "User not found"

        invalid = client.put(
            "/api/v1/user/1234",
            headers={
                "content-type": "application/json",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
            json=dict(
                email="test@example.com",
                username="test",
                first_name="test",
                last_name="test",
            ),
        )

        assert invalid.status_code == 404
        assert invalid.json()['detail'] == "Invalid ID should be 12-byte hex string"

    def test_user_delete(self, client, user):
        users = db.client.get_database("mt-services")["users"]
        users.insert_one(
            UserInDb(
                email="test2@example.com",
                username="test2",
                role=Roles.default,
                hashed_password="1a2dc3a39cb4170093d8c0fc",
            ).model_dump()
        )
        user_data = users.find_one({"email": "test2@example.com"})
        user_data = UserInDb.model_validate(user_data)

        auth = client.post(
            "/api/v1/auth/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=dict(
                username=user["email"],
                password=user["password"],
                scope=["read", "write"],
            ),
        )

        assert auth.status_code == 200
        assert auth.json()["access_token"] is not None

        delete = client.delete(
            f"/api/v1/user/{user_data.id}",
            headers={"Authorization": f"Bearer {auth.json()['access_token']}"},
        )

        response = delete.json()

        assert delete.status_code == 204
        assert response["detail"] == "OK"

        not_found = client.delete(
            "/api/v1/user/e346d91bda5cff5f01ded053",
            headers={"Authorization": f"Bearer {auth.json()['access_token']}"},
        )

        response = not_found.json()

        assert not_found.status_code == 404
        assert response["detail"] == "User not found"

        invalid = client.delete(
            "/api/v1/user/1234",
            headers={"Authorization": f"Bearer {auth.json()['access_token']}"},
        )

        response = invalid.json()

        assert invalid.status_code == 404
        assert response["detail"] == "Invalid ID should be 12-byte hex string"
