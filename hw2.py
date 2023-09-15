#!/usr/bin/env python

def parse_passwd(path):
	users = {}
	with open(path, 'r') as f:
		for line in f:
			if not line.startswith("#"):
				parts = line.strip().split(':')
				username = parts[0]
				uid = parts[2]
				gid = parts[3]
				users[username] = {'uid': uid, 'gid': gid, 'groups': []}
	return users

def parse_group(path, users):
	with open(path, 'r') as f:
		for line in f:
			if not line.startswith("#"):
				parts = line.strip().split(':')
				group_name = parts[0]
				gid = parts[2]
				members = parts[3].split(',')
				for user in users:
					if users[user]['gid'] == gid:
						users[user]['groups'].insert(0, group_name)
					elif user in members:
						users[user]['groups'].append(group_name)

def main():
	users = parse_passwd('/etc/passwd')
	parse_group('/etc/group', users)
	for user, data in users.items():
		print(f"{user} id: {data['uid']} groups: {', '.join(data['groups'])}")

if __name__ == "__main__":
	main()

