from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

# Create your tests here.


class BlogTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="testpassword"
        )

        self.post = Post.objects.create(
            title="a good title", body="nice body content", author=self.user
        )

    def test_string_representation(self):
        post = Post(title="a nice title")
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", "a good title")
        self.assertEqual(f"{self.post.body}", "nice body content")
        self.assertEqual(f"{self.post.author}", "testuser")

    def test_post_list_view(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "nice body content")
        self.assertTemplateUsed(resp, "home.html")

    def test_post_detail_view(self):
        resp = self.client.get("/post/1/")
        no_resp = self.client.get("/post/100000/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(no_resp.status_code, 404)
        self.assertContains(resp, "a good title")
        self.assertTemplateUsed(resp, "post_detail.html")

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_post_create_view(self):
        resp = self.client.post(
            reverse("post_create"),
            {
                "title": "next title",
                "body": "next body",
                "author": self.user.id,
            },
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Post.objects.last().title, "next title")
        self.assertEqual(Post.objects.last().body, "next body")

    

    def test_post_update_view(self):
        resp = self.client.post(
            reverse("post_edit", args="1"),
            {
                "title": "updated title",
                "body": "updated body",
            },
        )

        self.assertEqual(resp.status_code, 302)

    def test_post_delete_view(self):
        resp = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(resp.status_code, 302)
