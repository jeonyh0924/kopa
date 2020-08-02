from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from tours.models import Place, PlaceReview, ReviewComment

User = get_user_model()

"""
- 로그인 유저라면 후기, 댓글 유저와 매핑,
- 비 로그인 유저라면 (Anonymous User) 간편 로그인을 통하여 작
"""


class CommentTest(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        self.place = baker.make('tours.Place')
        self.place_review = PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            title='title',
            content='content',
        )

    def test_create(self):
        data = {
            'review': self.place_review.pk,
            'user': self.user.pk,
            'title': 'title',
            'content': 'content',
            'password': '1111'
        }
        response = self.client.post('/review/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['review'], data['review'])
        self.assertEqual(response.data['user'], data['user'])
        self.assertEqual(response.data['password'], data['password'])

        ### 로그인 유저
        self.client.force_authenticate(self.user)
        data = {
            'review': self.place_review.pk,
            'user': self.user.pk,
            'title': 'title',
            'content': 'content'
        }

        response = self.client.post('/review/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['review'], data['review'])
        self.assertEqual(response.data['user'], data['user'])
        # 로그인 유저는 댓글 비밀번호 유저 아이디로 저장
        self.assertEqual(response.data['password'], self.user.username[:20])

    def test_update(self):
        data = {
            'review': self.place_review.pk,
            'user': self.user.pk,
            'title': 'title',
            'content': 'content'
        }
        self.client.force_authenticate(self.user)
        response = self.client.post('/review/', data=data)

        update_data = {'password': '222', 'credit': response.data['password']}
        response = self.client.patch('/review/1/',
                                     data=update_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['password'], update_data['password'])

    def test_delete(self):
        ReviewComment.objects.create(
            review=self.place_review,
            user=self.user,
            title='title',
            content='content',
            password=self.user.username[:20]
        )
        data = {
            'credit':self.user.username[:20]
        }
        response = self.client.delete('/review/1/', data=data)
        self.assertEqual(response.status_code, 204)
