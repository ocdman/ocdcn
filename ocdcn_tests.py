import os
import ocdr
import unittest
import tempfile

class OcdrTestCase(unittest.TestCase):
	
	def setUp(self):
		self.db_fd, ocdr.app.config['DATABASE'] = tempfile.mkstemp()
		ocdr.app.config['TESTING'] = True
		self.app = ocdr.app.test_client()
		ocdr.init_db()
		
	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(ocdr.app.config['DATABASE'])
		
	def login(self, username, password):
		return self.app.post('/login', data=dict(
			username=username,
			password=password
		), follow_redirects=True)
		
	def logout(self):
		return self.app.get('/logout', follow_redirects=True)
		
	def test_empty_db(self):
		rv = self.app.get('/')
		#assert bytes("No entries here so far", "utf-8") in rv.data
		assert b'No entries here so far' in rv.data
		
	def test_login_logout(self):
		rv = self.login('admin', 'default')
		assert b'You were logged in' in rv.data
		rv = self.logout()
		assert b'You were logged out' in rv.data
		rv = self.login('john', 'default')
		assert b'Invalid username' in rv.data
		rv = self.login('admin', 'john')
		assert b'Invalid password' in rv.data
		
	def test_messages(self):
		self.login('admin', 'default')
		rv = self.app.post('/add', data=dict(
			title='<Keep Alive>',
			text='<strong>Keep</strong> Trainning'
		), follow_redirects=True)
		assert b'No entries here so far' not in rv.data
		assert b'&lt;Keep Alive&gt;' in rv.data
		assert b'<strong>Keep</strong> Trainning' in rv.data
		
		
if __name__ == '__main__':
	unittest.main()