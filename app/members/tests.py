from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.test import APITestCase

from members.models import MyList
from tours.models import Place

User = get_user_model()


class MyListTest(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        self.place = baker.make(Place)

    def test_list(self):
        l1 = MyList.objects.create(user=self.user, place=self.place)
        place1 = baker.make(Place)
        l2 = MyList.objects.create(user=self.user, place=place1)
        # 비 인증 유저는 빈 쿼리셋
        response = self.client.get('/members/myList/')

        self.client.force_authenticate(self.user)
        # 인증이 된 유저는 해당 유저에 대한 myList queryset
        response = self.client.get('/members/myList/')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        self.client.force_authenticate(self.user)
        data = {
            'user': self.user.id,
            'place': self.place.id
        }
        response = self.client.post('/members/myList/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['place'], data['place'])
        self.assertTrue(response.data['id'])

    def test_delete(self):
        l1 = MyList.objects.create(user=self.user, place=self.place)
        self.client.force_authenticate(self.user)
        response = self.client.delete(f'/members/myList/{l1.id}/')
        self.assertEqual(response.status_code, 204)
