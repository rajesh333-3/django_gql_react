import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from .models import Movie, Director
import graphql_jwt
from graphql_jwt.decorators import login_required,permission_required
from graphene_django.filter import DjangoFilterConnectionField
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
class DirectorType(DjangoObjectType):
    class Meta:
        model = Director

#Relay implementation

class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        filter_fields = ['title', 'year']
        interfaces = (relay.Node,)

class RecentMovieNode(DjangoObjectType):
    class Meta:
        model =  Movie
        filter_fields = {
            'title': ['exact','icontains','istartswith'],
            'year':['icontains']
        }
        interfaces = (relay.Node,)
class Query(graphene.ObjectType):

    # all_movies = graphene.List(MovieType)
    #relay wala
    all_movies = DjangoFilterConnectionField(MovieNode)
    recent_movies = DjangoFilterConnectionField(RecentMovieNode)
    movie = graphene.Field(MovieType, title = graphene.String())
    all_directors = graphene.List(DirectorType)
    #no need of resolving for relay
    # @login_required
    # def resolve_all_movies(self, info, **kwargs):
    #     return Movie.objects.all() 

    def resolve_movie(self, info, **kwargs):
        title =  kwargs.get('title')
        if title is not None:
            return Movie.objects.get(title=title)  

    def resolve_all_directors(self, info, **kwargs):
        return Director.objects.all()            

class CreateMovieMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required = True)
        year = graphene.Int(required = True)

    movie = graphene.Field(MovieType)
    @login_required 
    #so in django admin a permission like 'api | movie | Can add movie' is
    #  written in code name as api.add_movie which can be used in permission required syntax 
    # or simply use the model name and action like movie.can_add as below
    @permission_required("movie.can_add")
    def mutate(self, info, title, year):
        movie = Movie.objects.create(title=title, year=year, director=Director.objects.all()[0])
        return CreateMovieMutation(movie=movie)

class UpdateMovieMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required = True)
        year = graphene.Int(required = True)
        id = graphene.Int(required = True)
    movie = graphene.Field(MovieType)
    
    def mutate(self, info, title, year, id):
        movie = Movie.objects.get(pk=id)
        if title:
            movie.title = title
        if year:
            movie.year = year
        movie.save()
        
        return UpdateMovieMutation(movie=movie)

class DeleteMovieMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
    movie = graphene.Field(MovieType)
    def mutate(self, info,  id):
        movie = Movie.objects.get(pk=id)
        movie.delete()
class Mutation:
    create_movie = CreateMovieMutation.Field()
    update_movie = UpdateMovieMutation.Field()
    delete_mutation = DeleteMovieMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    

    
