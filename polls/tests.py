from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
 
class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
	# creem superusuari
        user = User.objects.create_user("test", "test@test.com", "test123")
        user.is_superuser = False
        user.is_staff = True
        user.save()
 
    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()
 
    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
 
        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
 
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('test')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('test123')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
 
        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )
        self.selenium.get(f'{self.live_server_url}/admin/password_change')
        old_password = self.selenium.find_element(By.ID, "id_old_password")
        old_password.send_keys("test123")
        new_password_input1 = self.selenium.find_element(By.ID, "id_new_password1")
        new_password_input2 = self.selenium.find_element(By.ID, "id_new_password2")
        new_password_input1.send_keys("123")
        new_password_input2.send_keys("123")
        self.selenium.find_element(By.XPATH, '//input[@type="submit" and @value="Change my password"]').click()
        errors = self.selenium.find_elements(By.CLASS_NAME, "errorlist")

        error_texts = [e.text for e in errors]
        for t in error_texts:
           print(t)
# Create your tests here
