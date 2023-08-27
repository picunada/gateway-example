from .test_base import db, client, user


class TestAuth:
    def test_user_auth(self, client, user):
        client.post(
            "/api/v1/user", headers={"content-type": "application/json"}, json=user
        )

        auth = client.post(
            "/api/v1/auth/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=dict(
                username=user["email"], password=user["password"], scope=["read"]
            ),
        )

        assert auth.status_code == 200
        assert auth.json()["access_token"] is not None

        not_valid_password = client.post(
            "/api/v1/auth/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=dict(
                username=user["email"], password="123456", scope=["read"]
            ),
        )

        assert not_valid_password.status_code == 401
        assert not_valid_password.json()["detail"] == "Invalid password" \

        logout = client.post(
            "/api/v1/auth/logout",
            headers={"content-type": "application/json"},
            json=auth.json()
        )

        assert logout.status_code == 200
        assert logout.json()["detail"] == "Logout"

        blacklisted_after_logout = client.get(
            "/api/v1/user",
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
        )

        assert blacklisted_after_logout.status_code == 403
        assert blacklisted_after_logout.json()["detail"] == "Blacklisted"

    def test_resource_accessed_with_token(self, client, user):
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

        accessed = client.get(
            "/api/v1/user",
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
        )

        print(accessed.json())
        assert accessed.status_code == 200


    def test_resource_not_accessed_without_scope(self, client, user):
        users = db.client.get_database("mt-services")["users"]
        users.update_one({"email": "test@example.com"}, {"$set": {"role": "admin"}})

        auth = client.post(
            "/api/v1/auth/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=dict(
                username=user["email"],
                password=user["password"],
            ),
        )

        assert auth.status_code == 200
        assert auth.json()["access_token"] is not None

        accessed = client.get(
            "/api/v1/user",
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {auth.json()['access_token']}",
            },
        )

        assert accessed.status_code == 401

    def test_resource_not_accessed_without_token(self, client, user):
        users = db.client.get_database("mt-services")["users"]
        users.update_one({"email": "test@example.com"}, {"$set": {"role": "default"}})

        not_accessed = client.get(
            "/api/v1/user",
            headers={
                "content-type": "application/x-www-form-urlencoded",
            },
        )

        assert not_accessed.status_code == 401

    def test_refresh_tokens(self, client, user):
        auth = client.post(
            "/api/v1/auth/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=dict(
                username=user["email"],
                password=user["password"],
            ),
        )

        assert auth.status_code == 200
        assert auth.json()["access_token"] is not None
        print(auth.json())

        refresh = client.post(
            "/api/v1/auth/refresh",
            headers={
                "content-type": "application/json",
            },
            json=auth.json(),
        )

        assert refresh.status_code == 200

    def test_tokens_blacklist(self, client, user):
        blacklist = db.client.get_database("mt-services")["blacklist"]
        blacklist.delete_many({"token_type": "bearer"})

        auth = client.post(
            "/api/v1/auth/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=dict(
                username=user["email"],
                password=user["password"],
            ),
        )

        assert auth.status_code == 200
        assert auth.json()["access_token"] is not None
        print(auth.json())

        refresh = client.post(
            "/api/v1/auth/refresh",
            headers={
                "content-type": "application/json",
            },
            json=auth.json(),
        )

        print(refresh.json())

        assert refresh.status_code == 200

        second_refresh = client.post(
            "/api/v1/auth/refresh",
            headers={
                "content-type": "application/json",
            },
            json=auth.json(),
        )

        assert second_refresh.status_code == 403
        assert second_refresh.json() == {"detail": "Blacklisted"}

        not_accessed_with_blacklisted_token = client.get(
            "/api/v1/user",
            headers={
                "Authorization": f"Bearer {auth.json()['access_token']}"
            }
        )

        assert not_accessed_with_blacklisted_token.status_code == 403
        assert not_accessed_with_blacklisted_token.json()["detail"] == "Blacklisted"
