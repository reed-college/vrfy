import random
import datetime
import requests
from django.test import TestCase, LiveServerTestCase
from django.utils import timezone
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from django.contrib.auth.models import User
from django.core.files import File as Dfile
import shutil

import sys
sys.path.append("../")
import vrfy.settings

from . import views
from .models import ProblemSet, Problem, ProblemSolutionFile

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"
COURSELAB_DIR = "/home/alex/verify_project/courselabs/"

class ProblemSetTests(TestCase):
  """
  A Model for TestCases that use Problem sets 
  It makes a new problem set for testing and then deletes it when the tests are over
  """
  @classmethod
  def setUpClass(cls):
    cls.ps = ProblemSet(title='test_ps_' + str(random.randint(1,10000)), pub_date=timezone.now(), due_date=timezone.now() + datetime.timedelta(days=30))
    cls.ps.save()
    cls.pk = cls.ps.pk
    super(ProblemSetTests, cls).setUpClass()
  
  @classmethod
  def tearDownClass(cls):
    #if the ps still exists, delete it
    if cls.ps.id != None :
      cls.ps.delete()
    super(ProblemSetTests, cls).tearDownClass()
  
class NonExistantProblemsetTests(ProblemSetTests):
  """
  Tests that the course pages give a 404 when you try to access a page that doesnt exist
  """
  @classmethod
  def setUpClass(cls):
    super(NonExistantProblemsetTests, cls).setUpClass()
    cls.ps.delete()

  def test_attempt_gives_404_for_nonexistant_problem_set(self):
    response = self.client.get(reverse('course:attempt_problem_set', args=(self.pk,)))
    self.assertEqual(response.status_code, 404)

  def test_detail_gives_404_for_nonexistant_problem_set(self):
    response = self.client.get(reverse('course:problem_set_detail', args=(self.pk,)))
    self.assertEqual(response.status_code, 404)

  def test_submit_gives_404_for_nonexistant_problem_set(self):
    response = self.client.post(reverse('course:problem_set_submit', args=(self.pk,)))
    self.assertEqual(response.status_code, 404)

  def test_results_gives_404_for_nonexistant_problem_set(self):
    response = self.client.get(reverse('course:results_detail', args=(self.pk,)))
    self.assertEqual(response.status_code, 404)
  
class GetExistingProblemsetTests(ProblemSetTests):
  """
  Test that pages return working for existing problem sets 
  """
  
  def test_attempt_gives_200_for_existing_problem_set(self):
    response = self.client.get(reverse('course:attempt_problem_set', args=(self.pk,)))
    self.assertEqual(response.status_code, 200)

  def test_detail_gives_200_for_existing_problem_set(self):
    response = self.client.get(reverse('course:problem_set_detail', args=(self.pk,)))
    self.assertEqual(response.status_code, 200)

  #302 because the page should redirect you after you submit
  def test_submit_gives_302_for_existing_problem_set(self):
    response = self.client.post(reverse('course:problem_set_submit', args=(self.pk,)))
    self.assertEqual(response.status_code, 302)

  def test_results_gives_200_for_existing_problem_set(self):
    response = self.client.get(reverse('course:results_detail', args=(self.pk,)))
    self.assertEqual(response.status_code, 200)

  #checks for the name of the problem set on the index page
  def test_ps_index_lists_existing_problem_sets(self):
    response = self.client.get(reverse('course:problem_set_index'))
    self.assertIn(self.ps.title, str(response.content))

class CantSeeFutureAssignmentsTests(ProblemSetTests):
  """
  Tests if you can see problem sets with their pubdate in the future
  """
  @classmethod
  def setUpClass(cls):
    super(CantSeeFutureAssignmentsTests, cls).setUpClass()
    #makes the ps's pub date in the future
    cls.ps.pub_date = timezone.now() + datetime.timedelta(days=5)
    cls.ps.save()
    
  def test_attempt_gives_404_for_future_problem_set(self):
    response = self.client.get(reverse('course:attempt_problem_set', args=(self.ps.pk,)))
    self.assertEqual(response.status_code, 404)

  def test_detail_gives_404_for_future_problem_set(self):
    response = self.client.get(reverse('course:problem_set_detail', args=(self.ps.pk,)))
    self.assertEqual(response.status_code, 404)

  def test_submit_gives_404_for_future_problem_set(self):
    response = self.client.post(reverse('course:problem_set_submit', args=(self.ps.pk,)))
    self.assertEqual(response.status_code, 404)

  def test_results_gives_404_for_future_problem_set(self):
    response = self.client.get(reverse('course:results_detail', args=(self.ps.pk,)))
    self.assertEqual(response.status_code, 404)

  #Checks that the future ps is not on the index page
  def test_ps_index_doesnt_list_future_problem_sets(self):
    response = self.client.get(reverse('course:problem_set_index'))
    self.assertNotIn(self.ps.title, str(response.content))

class AdminTests(LiveServerTestCase):
  
  def setUp(self):
    self.driver = webdriver.Firefox()
    User.objects.create_superuser(ADMIN_USERNAME, 'fake@example.com', ADMIN_PASSWORD)

  #helper function that logs in to the admin side
  def _login(self):
    self.driver.find_element_by_id("id_username").send_keys(ADMIN_USERNAME)
    pw = self.driver.find_element_by_id("id_password")
    pw.send_keys(ADMIN_PASSWORD)
    pw.send_keys(Keys.RETURN)
  
  #helper function to make a new problem
  def _new_problem(self, name):
    prob = Problem.objects.create(title=name, course="420", description="Super fun problem", statement="yay")
    return prob
  
  #adds a new solution file
  def _new_solfile(self, prob, filepath):
    with open(filepath, 'r') as f:
      sol = ProblemSolutionFile.objects.create(problem=prob)
      df = Dfile(f)
      sol.file_upload.save(filepath, df)
    return sol
    
  #helper function that fills out a form for a new problem set
  def _new_ps(self, name):
    self.driver.find_element_by_id("id_title").send_keys(name)
    self.driver.find_element_by_id("id_description").send_keys("This is a description")
    problems = Select(self.driver.find_element_by_id('id_problems'))
    problems.select_by_index(0)
    
    self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/form/div/fieldset[3]/div[1]/div/p/span[1]/a[1]").click()
    self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/form/div/fieldset[3]/div[1]/div/p/span[2]/a[1]").click()
    self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/form/div/fieldset[3]/div[2]/div/p/span[1]/a[1]").click()
    self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/form/div/fieldset[3]/div[2]/div/p/span[2]/a[1]").click()

    self.driver.find_element_by_name("_save").click()

    return name
    
  def _del_ps(self, name):
    #remove it from the db
    self.driver.get(self.live_server_url + "/admin/course/problemset/")
    self.driver.find_element_by_link_text(name).click()
    self.driver.find_element_by_class_name("deletelink").click()
    self.driver.find_element_by_name("post").submit()
    #remove it from Tango
    shutil.rmtree(COURSELAB_DIR + vrfy.settings.TANGO_KEY + "-" + name)

  def test_new_problem_set_opens_courselab(self):
    prob = self._new_problem("fun problem")
    self.driver.get(self.live_server_url + "/admin/course/problemset/add")
    self._login()
    
    name = "test_ps_" + str(random.randint(1,10000))
    self._new_ps(name)
    
    url = vrfy.settings.TANGO_ADDRESS + "open/" + vrfy.settings.TANGO_KEY + "/" + slugify(name) + "/"
    response = requests.get(url)
    
    #clean up the db and the tango courselab folder
    self._del_ps(name)
    prob.delete()
    
    #if that request creates the courselab, then it wasn't created by the admin app
    self.assertNotEqual(response.json()["statusMsg"], "Created directory")

  def test_new_problem_set_uploads_file(self):
    prob = self._new_problem("fun problem")
    sol = self._new_solfile(prob, "my_solution_file.txt")
    self.driver.get(self.live_server_url + "/admin/course/problemset/add")
    self._login()
    
    name = "test_ps_" + str(random.randint(1,10000))
    self._new_ps(name)
    
    url = vrfy.settings.TANGO_ADDRESS + "open/" + vrfy.settings.TANGO_KEY + "/" + slugify(name) + "/"
    response = requests.get(url)
    
    self._del_ps(name)
    sol.delete()
    prob.delete()
    
    #Check that the uploaded file is in the courselabs
    self.assertIn("my_solution_file", str(response.json()["files"]))

  def tearDown(self):
    self.driver.close()

