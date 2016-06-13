__author__ = 'henar'

import generate_users
if __name__ == '__main__':
    create = generate_users.GenerateUser("community_user", "community_user", "community_user", "community")
    create.create_user()
    create = generate_users.GenerateUser("trial_user", "trial_user", "trial_user", "trial")
    create.create_user()
    create = generate_users.GenerateUser("basic_user", "basic_user", "basic_user", "basic")
    create.create_user()
    create = generate_users.GenerateUser("test", "test", "test", "community")
    create.create_user()
