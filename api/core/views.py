from rest_framework import viewsets, permissions, pagination, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from taggit.models import Tag

from .serializers import PostSerializer, TagSerializer, ContactSerializer, UserSerializer, RegisterSerializer, CommentSerializer
from .models import Post, Comment

# Create your views here.
class PageNumberSetpagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    # ordering = '-created_at'


class PostViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter, )
    search_fields = ['content', 'h1']
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created_at')
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetpagination
    

class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberSetpagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag).order_by('-created_at')


class TagView(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [permissions.AllowAny]
    

class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:5]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_mail = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'From {name} | {subject}', message, from_mail, ['admin@admin.com'])
            return Response({'success': 'Sent'})
        return Response({'error': 'error'})


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Пользователь успешно создан',
        })
    

class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            'user': UserSerializer(request.user, context=self.get_serializer_context()).data,
        })
    

class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_slug = self.kwargs.get('post_slug').lower()
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)
    