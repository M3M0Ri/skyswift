from django.test import TestCase
from user.models import MyUserModel, Profile


class TestUserModel(TestCase):

    def setUp(self):
        self.user = MyUserModel.objects.create_user(
            email='test@gmail.com',
            username='testuser',
            password='testpassword'
        )

    def test_creates_user(self):
        # user = MyUserModel.objects.create_user(
        #     email='test@gmail.com',
        #     username='testuser',
        #     password='testpassword'
        # )
        self.assertIsInstance(self.user, MyUserModel)
        self.assertEquals(self.user.email, "test@gmail.com")
        self.assertEquals(self.user.username, "testuser")
        self.assertEquals(self.user.password, "testpassword")
        self.assertEqual(self.user.role, 'normal')
        self.assertEqual(self.user.gender, 'male')

    def test_profile_creation(self):
        profile = Profile.objects.create(
            user=self.user,
            full_name='test User',
            bio='test bio',
            phone='1234567890',
            gender='male',
            about_me='test about me',
            country='test country',
            state='test state',
            city='test city',
            address='test address',
            working_at='test working',
            instagram='test instagram',
            verified=True
        )

        self.assertEqual(profile.full_name, 'test User')
        self.assertEqual(profile.bio, 'test bio')
        self.assertEqual(profile.phone, '1234567890')
        self.assertEqual(profile.gender, 'male')
        self.assertEqual(profile.about_me, 'test about me')
        self.assertEqual(profile.country, 'test country')
        self.assertEqual(profile.state, 'test state')
        self.assertEqual(profile.city, 'test city')
        self.assertEqual(profile.address, 'test address')
        self.assertEqual(profile.working_at, 'test working')
        self.assertEqual(profile.instagram, 'test instagram')
        self.assertTrue(profile.verified)


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = MyUserModel.objects.create_user(
            email='test@gmail.com',
            username='testuser',
            password='testpassword'
        )

    def test_one_to_one_field_relationship(self):
        user = MyUserModel.objects.create_user(email="test@gmail.com", username="testuser")
        profile = user.profile
        self.assertEqual(profile.user, user)

    def test_profile_slug_generation(self):
        profile = Profile.objects.create(user=self.user, full_name='test user')
        self.assertIsNotNone(profile.slug)
        self.assertTrue(profile.slug.startswith('test-user'))