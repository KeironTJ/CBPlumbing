from app import db, create_app
from app.models import User, UserRoles, Role

app=create_app()

app_context = app.app_context()
app_context.push()

# Test to create roles
def create_role(name):
    role = Role(name=name)
    db.session.add(role)
    return role

def create_user(username, email, password): 
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    return user


def delete_existing_data():
    db.session.query(User).delete()
    db.session.query(Role).delete()
    db.session.query(UserRoles).delete
    db.session.commit()
    print("Data Deleted")
    
delete_existing_data()

# Create admin and user roles
admin_role = create_role('admin')
user_role = create_role('user')

# Create admin user
admin_user = create_user('admin', 'test1@test.com', 'abc123')
test_user = create_user('test', 'test2@test.com', 'abc123')
db.session.commit()

# Assign role to admin 
admin_user_role = UserRoles(user_id=admin_user.id, role_id=admin_role.id)
test_user_role = UserRoles(user_id=test_user.id, role_id=user_role.id)
db.session.add(admin_user_role)
db.session.add(test_user_role)

# Commit all changes 
db.session.commit()
print("Data Created")
