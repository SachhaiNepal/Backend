from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.sub_models.member import Member
from accounts.sub_models.profile import Profile
from advertise.models import Advertisement
from article.sub_models.article import Article
from branch.models import Branch
from event.sub_models.event import Event
from multimedia.sub_models.multimedia import Multimedia


class ModelStatisticsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        profiles = Profile.objects.all()
        members = Member.objects.all()
        branches = Branch.objects.all()
        articles = Article.objects.all()
        multimedia = Multimedia.objects.all()
        events = Event.objects.all()
        advertisements = Advertisement.objects.all()

        return Response(
            {
                "followers": profiles.count(),
                "members": members.count(),
                "branches": branches.count(),
                "articles": articles.count(),
                "multimedias": multimedia.count(),
                "events": events.count(),
                "advertisements": advertisements.count(),
            }
        )
