from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from blog.models import Blog
from blog.serializers import BlogListSerializer, BlogDetailSerializer, CommentSerializer


class BlogListView(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogListSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Blog, pk=pk)

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogDetailSerializer(blog)
        return Response(serializer.data)

    def patch(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogListSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):
    def get_blog(self, pk):
        return get_object_or_404(Blog, pk=pk)

    def get(self, request, pk):
        blog = self.get_blog(pk)
        comments = blog.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        blog = self.get_blog(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(blog=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
