from django.contrib.auth import get_user_model
from django.db import models
import re

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('태그명', max_length=100, null=True)

    def __str__(self):
        return self.name


class Place(models.Model):
    TAG_PATTERN = re.compile(r'#(\w+)')
    name = models.CharField(max_length=100, verbose_name='관광지 이름', help_text='관광지 이름')
    content = models.TextField(blank=True, verbose_name='관광지 태그')
    address = models.CharField(max_length=150, verbose_name='관광지 주소', help_text='광관지 주소')
    average_score = models.PositiveIntegerField(default=0, help_text='평균점수')
    phone_number = models.CharField(max_length=100, help_text='관광지 전화번호')
    open_time = models.CharField(max_length=100, help_text='관광지 오픈 시간')
    url = models.URLField(max_length=200, help_text='관광지 관련 URL')
    trans = models.CharField(max_length=255, help_text='관광지 교통편')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='해시태그 목록',
        help_text='관광지 태그 목록')

    # my list
    release_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def _save_tags(self):
        """
        content에 포함된 해시태그 문자열 (ex: #Python)의 Tag들을 만들고,
        자신의 tags Many-to-many field에 추가한다
        """
        tag_name_list = re.findall(self.TAG_PATTERN, self.content)
        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_name_list]
        self.tags.set(tags)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._save_tags()


class PlaceReview(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE, help_text='리뷰 관련 관광지')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='후기 작성자')
    title = models.CharField(max_length=100, help_text='후기 타이들')
    content = models.TextField(help_text='후기 내용')
    evaluated_score = models.PositiveSmallIntegerField(default=0, help_text='관광지 평가 점수')
    release_date = models.DateTimeField(auto_now_add=True, help_text='후기 생성된 시간')

    # def __str__(self):
    #     return f'{self.place}의 후기 {self.title}'


class PlaceLike(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    release_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.place}장소 좋아요'


class ReviewComment(models.Model):
    review = models.ForeignKey('PlaceReview', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, )
    title = models.CharField(max_length=100)
    content = models.TextField()
    release_date = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.review}의 댓글'


class CelebrityCategory(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE)
    celebrity = models.ForeignKey('Celebrity', on_delete=models.CASCADE)
    release_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.celebrity}와 관련된 {self.place} 관광지'


class Celebrity(models.Model):
    PROFESSION = (
        ('SINGER', 'SINGER'),
        ('ACTOR', 'ACTOR'),
        ('TALENT', 'TALENT'),
        ('DIRECTOR', 'DIRECTOR')
    )
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=20, choices=PROFESSION)

    def __str__(self):
        return f'연예인 {self.name}'


class KPopContent(models.Model):
    TYPE_MOIVE = 'mv'
    TYPE_MUSIC = 'mu'
    TYPE_TELEVISION = 'tv'
    TYPE_KOREA_CULTURE = 'kc'
    TYPE_CELEB = 'cb'
    TYPE_GROUP = 'gp'
    CHOICES_TYPE = (
        (TYPE_MOIVE, '영화'),
        (TYPE_MUSIC, '음악'),
        (TYPE_TELEVISION, '방송'),
        (TYPE_KOREA_CULTURE, '문화'),
        (TYPE_CELEB, '셀럽'),
        (TYPE_GROUP, '그룹'),
    )
    place = models.ForeignKey('Place', related_name='kpopcategories', on_delete=models.CASCADE)
    content_type = models.CharField('타입', max_length=2, choices=CHOICES_TYPE, default=TYPE_KOREA_CULTURE)
    title = models.CharField('컨텐츠 제목', max_length=100)
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        # 컨텐츠와 관련된 주연배우들 모두를 표현하하고 싶음
        return f'카테고리 {self.content_type}의 제목은 {self.title} 입니다'
