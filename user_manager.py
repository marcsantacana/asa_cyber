import csv

# Funció per carregar usuaris des de CSV
def load_users(file_path):
    users = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users

# Exemple d'ús
users = load_users('users.csv')
for user in users:
    print(user['email'])
