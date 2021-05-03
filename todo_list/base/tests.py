from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.test import Client
from django.contrib.auth.models import User, AnonymousUser
from .views import CustomLoginView, RegisterPage, TaskList
from .models import Task


# Create your tests here.
class RegisterPageTestCase(TestCase):
    def setUp(self) -> None:
        self.username = "Testing"
        self.password1 = "Pass!!!123"
        self.password2 = "Pass!!!123"
        self.client = Client()

    def test_register_url(self):
        response = self.client.get('/register', fallow=True)
        self.assertRedirects(response, '/register/', status_code=301, target_status_code=200)

    def test_register_form(self):
        response = self.client.post('/register', data={
            "username": self.username,
            "password1": self.password1,
            "password2": self.password2
        })
        self.assertEqual(response.status_code, 301)


class TaskCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test_user@gmail.com', password='Pass!!!123')

    def test_create_task(self):
        request = self.factory.get('/create-task')

        request.user = AnonymousUser()
        response = self.client.get('/create-task', follow=True)
        self.assertRedirects(response, '/login/?next=/create-task/', status_code=301, target_status_code=200)

        request.user = self.user
        response = self.client.post('/create-task', data={
            "title": "Title",
            "description": "Description ...",
            "complete": False
        }, follow=True)
        self.assertEqual(response.status_code, 200)


class TaskUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser', email='test_user@gmail.com', password='Pass!!!123')
        self.factory = RequestFactory()

    def test_task_update(self):
        response = self.client.get('/task-update/1/', follow=True)
        self.assertRedirects(response, '/login/?next=/task-update/1/', status_code=302, target_status_code=200)

        self.client.login(username='testuser', password='Pass!!!123')
        task = Task.objects.create(user=self.user, title="Title", description="Description ...", complete=False)
        response = self.client.post(reverse('task-update', kwargs={'pk': task.id}),
                                    {'title': task.title, 'complete': True})
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.complete, True)


class TaskDetailTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser', email='test_user@gmail.com', password='Pass!!!123')

    def test_task_list(self):
        response = self.client.get('/task/1', follow=True)
        self.assertRedirects(response, '/login/?next=/task/1/', status_code=301, target_status_code=200)

        self.client.login(username='testuser', password='Pass!!!123')
        task = Task.objects.create(user=self.user, title="Title", description="Description ...", complete=False)
        response = self.client.get(f'/task/{task.id}', follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/task/404', follow=True)
        self.assertEqual(response.status_code, 404)


class TaskListTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser', email='test_user@gmail.com', password='Pass!!!123')
        self.factory = RequestFactory()

    def test_task_list(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/login/?next=/', status_code=302, target_status_code=200)

        self.client.login(username='testuser', password='Pass!!!123')
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_context_variables(self):
        request = self.factory.get('/')
        request.user = self.user
        view = TaskList()
        view.setup(request)
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        self.assertIn('tasks', context)
        self.assertIn('count', context)
        self.assertIn('search_input', context)
        self.assertNotIn('testnotpresent', context)


class DeleteViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser', email='test_user@gmail.com', password='Pass!!!123')

    def test_delete_task(self):
        response = self.client.get('/task-delete/1/', follow=True)
        self.assertRedirects(response, '/login/?next=/task-delete/1/', status_code=302, target_status_code=200)

        self.client.login(username='testuser', password='Pass!!!123')
        task = Task.objects.create(user=self.user, title="Title", description="Description ...", complete=False)
        response = self.client.delete(reverse('task-delete', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 302)
