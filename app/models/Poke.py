from system.core.model import Model
import re

class Poke(Model):
    def __init__(self):
        super(Poke, self).__init__()

    def create_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        name = info['name']
        alias = info['alias']
        email = info['email']
        password = info['password']
        confirm = info['confirm']
        bday = info['bday']
        valid = True
        errors = []
        if name < 1:
            errors.append("Name not filled in!")
            valid = False
        if not name.isalpha():
            errors.append("Name has non alphabet characters")
            valid = False
        if alias < 1:
            errors.append("Alias is nonexistant!")
            valid = False
        if email < 1:
            errors.append('Email is nonexistant!')
            valid = False
        if not EMAIL_REGEX.match(email):
            errors.append("Email is not a valid format!")
            valid = False
        if password < 8:
            errors.append("Password is not long enough!")
            valid = False
        if password != confirm:
            errors.append('Passwords do not match!')
            valid = False
        if valid:
            pcrypt = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (name, alias, email, password, bday, created_at, updated_at) " \
                    "VALUES (:name, :alias, :email, :pcrypt, :bday, NOW(), NOW())"
            data = {
                'name': name,
                'alias': alias,
                'email': email,
                'pcrypt': pcrypt,
                'bday': bday
            }
            self.db.query_db(query, data)
            query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(query)
            return {'valid': True, 'user': users[0]}
        else:
            return {'valid': False, 'errors': errors}

    def login_user(self, info):
        query = "SELECT * FROM users WHERE email = :email"
        data = {'email': info['email']}
        user = self.db.query_db(query, data)
        errors = []
        if len(user) >= 1:
            password = user[0]['password']
            if self.bcrypt.check_password_hash(password, info['password']):
                return{'valid': True, 'user': user[0]}
            else:
                errors.append("Email and password do not match!")
                return {'valid': False, 'errors': errors}
        else: 
                errors.append("Invalid input! Email not in Database!")
                return {'valid': False, 'errors': errors}

    def load_all_pokes(self, id):
        query = "SELECT * FROM users WHERE id <> :id"
        data = {
            'id': id
        }
        all_users = self.db.query_db(query, data)
        for user in all_users:
            query = "SELECT users.id, user2.id as poked_id, users.name, user2.name as name2, user2.alias as alias2, user2.email as email2, COUNT(pokes.poke_id) as person_pokes FROM users " \
                    "left join pokes on pokes.user_id = users.id " \
                    "left join users as user2 on user2.id = pokes.poke_id " \
                    "WHERE pokes.poke_id = :id group by pokes.poke_id;"
            data = {
                'id': user['id']
            }
            pokes = self.db.query_db(query, data)
            if not pokes:
                user['pokes'] = 0
            else:
                user['pokes'] = pokes[0]['person_pokes']
        return all_users

    def poke_someone(self, user_id, poked_id):
        query = "INSERT INTO pokes (created_at, updated_at, user_id, poke_id) " \
                "VALUES (NOW(), NOW(), :user_id, :poked_id)"
        data = {
            'user_id': user_id,
            'poked_id': poked_id
        }
        self.db.query_db(query, data)

    def load_people(self, user_id):
        query = "SELECT *, COUNT(poke_id) as pokes FROM pokes " \
                "left join users on pokes.user_id = users.id " \
                "where poke_id = :id " \
                "group by user_id; "
        data = {
            'id': user_id
        }
        num_people = self.db.query_db(query, data)
        return num_people

    def load_num_people(self, user_id):
      query = "SELECT * FROM pokes " \
              "left join users on pokes.user_id = users.id " \
              "where poke_id = :id " \
              "group by user_id; "
      data = {
          'id': user_id
      }
