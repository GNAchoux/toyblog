from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from blog.models import Blog, Comment


class BlogListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Blog.objects.create(title="게시글1", body="내용1")
        Blog.objects.create(title="게시글2", body="내용2")

    def test_get_blog_list(self):
        response = self.client.get("/blogs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn("id", response.data[0])
        self.assertIn("title", response.data[0])
        self.assertIn("body", response.data[0])
        self.assertIn("created_at", response.data[0])

    def test_create_blog(self):
        data = {"title": "게시글", "body": "내용"}
        response = self.client.post("/blogs/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "게시글")
        self.assertEqual(response.data["body"], "내용")
        self.assertEqual(Blog.objects.count(), 3)

    def test_create_blog_missing_title(self):
        data = {"body": "제목 없는 글"}
        response = self.client.post("/blogs/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BlogDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.blog = Blog.objects.create(title="상세 게시글", body="상세 내용")
        Comment.objects.create(blog=self.blog, comment="첫 댓글")

    def test_get_blog_detail(self):
        response = self.client.get(f"/blogs/{self.blog.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "상세 게시글")
        self.assertIn("comments", response.data)
        self.assertEqual(len(response.data["comments"]), 1)

    def test_get_blog_detail_not_found(self):
        response = self.client.get("/blogs/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_blog(self):
        data = {"title": "수정된 제목"}
        response = self.client.patch(f"/blogs/{self.blog.pk}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "수정된 제목")
        self.assertEqual(response.data["body"], "상세 내용")

    def test_patch_blog_not_found(self):
        response = self.client.patch("/blogs/9999/", {"title": "없는 글"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_blog(self):
        response = self.client.delete(f"/blogs/{self.blog.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Blog.objects.filter(pk=self.blog.pk).exists())

    def test_delete_blog_not_found(self):
        response = self.client.delete("/blogs/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.blog = Blog.objects.create(title="댓글 테스트용 게시글", body="내용")
        Comment.objects.create(blog=self.blog, comment="댓글1")
        Comment.objects.create(blog=self.blog, comment="댓글2")

    def test_get_comment_list(self):
        response = self.client.get(f"/blogs/{self.blog.pk}/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn("id", response.data[0])
        self.assertIn("blog_id", response.data[0])
        self.assertIn("comment", response.data[0])
        self.assertIn("created_at", response.data[0])
        self.assertEqual(response.data[0]["blog_id"], self.blog.pk)

    def test_get_comment_list_blog_not_found(self):
        response = self.client.get("/blogs/9999/comments/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment(self):
        data = {"comment": "새 댓글"}
        response = self.client.post(f"/blogs/{self.blog.pk}/comments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["comment"], "새 댓글")
        self.assertEqual(response.data["blog_id"], self.blog.pk)
        self.assertEqual(Comment.objects.filter(blog=self.blog).count(), 3)

    def test_create_comment_missing_body(self):
        response = self.client.post(f"/blogs/{self.blog.pk}/comments/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_blog_not_found(self):
        data = {"comment": "없는 게시글에 댓글"}
        response = self.client.post("/blogs/9999/comments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
