__author__ = 'henar'

import generate_users
import os
if __name__ == '__main__':
    os.environ["OS_PROJECT_DOMAIN_NAME"] = "default"
    os.environ["OS_USERNAME"] = "idm"
    os.environ["OS_PASSWORD"] = "idm"
    os.environ["OS_TENANT_NAME"] = "idm"
    os.environ["OS_AUTH_URL"] = "http://130.206.114.220:5000/v3"
    os.environ["KEYSTONE_HOST"] = "130.206.114.220"

    create = generate_users.GenerateUser("community_user", "community_user", "community_user", "community")
    create.create_user()
    create = generate_users.GenerateUser("trial_user", "trial_user", "trial_user", "trial")
    create.create_user()
    create = generate_users.GenerateUser("basic_user", "basic_user", "basic_user", "basic")
    create.create_user()
    create = generate_users.GenerateUser("test", "test", "test", "community")
    create.create_user()
