"""
API views for the movies application using Django REST Framework.
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from django.http import Http404
from .models import Movie, Genre
from .services import TMDbService
from .serializers import (
    MovieSerializer, 
    GenreSerializer, 
    TMDbMovieSerializer,
    TMDbMovieDetailSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema_view(
    get=extend_schema(
        tags=['Movies'],
        summary='List local movies',
        description='Retrieve a paginated list of movies stored in the local database.',
        responses={
            200: MovieSerializer(many=True),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class MovieListAPIView(generics.ListAPIView):
    """API view for listing local movies."""
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = StandardResultsSetPagination


@extend_schema_view(
    get=extend_schema(
        tags=['Movies'],
        summary='Get movie details',
        description='Retrieve detailed information about a specific movie from the local database.',
        responses={
            200: MovieSerializer,
            404: OpenApiResponse(description='Movie not found'),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class MovieDetailAPIView(generics.RetrieveAPIView):
    """API view for retrieving a single local movie."""
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'movie_id'


@extend_schema_view(
    get=extend_schema(
        tags=['Genres'],
        summary='List local genres',
        description='Retrieve all genres stored in the local database.',
        responses={
            200: GenreSerializer(many=True),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class GenreListAPIView(generics.ListAPIView):
    """API view for listing genres."""
    
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TMDbAPIBaseMixin:
    """Base mixin for TMDb API views."""
    
    def get_tmdb_service(self):
        """Get TMDb service instance."""
        try:
            return TMDbService(), None
        except ValueError as e:
            return None, str(e)
    
    def handle_tmdb_response(self, data, serializer_class=TMDbMovieSerializer):
        """Handle TMDb API response."""
        if not data:
            return Response(
                {'error': 'Unable to fetch data from TMDb API'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Serialize the results
        results = data.get('results', [])
        serializer = serializer_class(results, many=True)
        
        # Return paginated response
        return Response({
            'results': serializer.data,
            'page': data.get('page', 1),
            'total_pages': data.get('total_pages', 1),
            'total_results': data.get('total_results', 0)
        })


@extend_schema_view(
    get=extend_schema(
        tags=['Movies'],
        summary='Get popular movies',
        description='Fetch popular movies from TMDb API with pagination support.',
        parameters=[
            OpenApiParameter(
                name='page',
                description='Page number for pagination',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            )
        ],
        responses={
            200: TMDbMovieSerializer(many=True),
            400: OpenApiResponse(description='Invalid request parameters'),
            503: OpenApiResponse(description='TMDb API unavailable'),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class PopularMoviesAPIView(TMDbAPIBaseMixin, APIView):
    """API view for fetching popular movies from TMDb."""
    
    def get(self, request):
        """Get popular movies from TMDb API."""
        tmdb_service, error = self.get_tmdb_service()
        if not tmdb_service:
            return Response(
                {'error': f'TMDb API configuration error: {error}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            page = int(request.GET.get('page', 1))
            data = tmdb_service.get_popular_movies(page=page)
            return self.handle_tmdb_response(data)
        except ValueError:
            return Response(
                {'error': 'Invalid page number'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        tags=['Movies'],
        summary='Get top rated movies',
        description='Fetch top rated movies from TMDb API with pagination support.',
        parameters=[
            OpenApiParameter(
                name='page',
                description='Page number for pagination',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            )
        ],
        responses={
            200: TMDbMovieSerializer(many=True),
            400: OpenApiResponse(description='Invalid request parameters'),
            503: OpenApiResponse(description='TMDb API unavailable'),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class TopRatedMoviesAPIView(TMDbAPIBaseMixin, APIView):
    """API view for top rated movies from TMDb."""
    
    def get(self, request):
        tmdb_service, error = self.get_tmdb_service()
        if not tmdb_service:
            return Response(
                {'error': f'TMDb API configuration error: {error}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            page = int(request.GET.get('page', 1))
            data = tmdb_service.get_top_rated_movies(page=page)
            return self.handle_tmdb_response(data)
        except ValueError:
            return Response(
                {'error': 'Invalid page number'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        tags=['Movies'],
        summary='Get now playing movies',
        description='Fetch currently playing movies from TMDb API with pagination support.',
        parameters=[
            OpenApiParameter(
                name='page',
                description='Page number for pagination',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            )
        ],
        responses={
            200: TMDbMovieSerializer(many=True),
            400: OpenApiResponse(description='Invalid request parameters'),
            503: OpenApiResponse(description='TMDb API unavailable'),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class NowPlayingMoviesAPIView(TMDbAPIBaseMixin, APIView):
    """API view for now playing movies from TMDb."""
    
    def get(self, request):
        tmdb_service, error = self.get_tmdb_service()
        if not tmdb_service:
            return Response(
                {'error': f'TMDb API configuration error: {error}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            page = int(request.GET.get('page', 1))
            data = tmdb_service.get_now_playing_movies(page=page)
            return self.handle_tmdb_response(data)
        except ValueError:
            return Response(
                {'error': 'Invalid page number'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        tags=['Movies'],
        summary='Get upcoming movies',
        description='Fetch upcoming movies from TMDb API with pagination support.',
        parameters=[
            OpenApiParameter(
                name='page',
                description='Page number for pagination',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            )
        ],
        responses={
            200: TMDbMovieSerializer(many=True),
            400: OpenApiResponse(description='Invalid request parameters'),
            503: OpenApiResponse(description='TMDb API unavailable'),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class UpcomingMoviesAPIView(TMDbAPIBaseMixin, APIView):
    """API view for upcoming movies from TMDb."""
    
    def get(self, request):
        tmdb_service, error = self.get_tmdb_service()
        if not tmdb_service:
            return Response(
                {'error': f'TMDb API configuration error: {error}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            page = int(request.GET.get('page', 1))
            data = tmdb_service.get_upcoming_movies(page=page)
            return self.handle_tmdb_response(data)
        except ValueError:
            return Response(
                {'error': 'Invalid page number'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        tags=['Movies'],
        summary='Search movies',
        description='Search for movies on TMDb using a text query with pagination support.',
        parameters=[
            OpenApiParameter(
                name='q',
                description='Search query string (required)',
                required=True,
                type=OpenApiTypes.STR
            ),
            OpenApiParameter(
                name='page',
                description='Page number for pagination',
                required=False,
                type=OpenApiTypes.INT,
                default=1
            )
        ],
        responses={
            200: TMDbMovieSerializer(many=True),
            400: OpenApiResponse(description='Missing or invalid query parameter'),
            503: OpenApiResponse(description='TMDb API unavailable'),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class SearchMoviesAPIView(TMDbAPIBaseMixin, APIView):
    """API view for searching movies using TMDb."""
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response(
                {'error': 'Query parameter "q" is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tmdb_service, error = self.get_tmdb_service()
        if not tmdb_service:
            return Response(
                {'error': f'TMDb API configuration error: {error}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            page = int(request.GET.get('page', 1))
            data = tmdb_service.search_movies(query, page=page)
            
            if not data:
                return Response(
                    {'error': 'Unable to perform search'}, 
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            # Add query to response
            response_data = self.handle_tmdb_response(data).data
            response_data['query'] = query
            return Response(response_data)
            
        except ValueError:
            return Response(
                {'error': 'Invalid page number'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        tags=['Movies'],
        summary='Get movie details from TMDb',
        description='Retrieve detailed information about a specific movie from TMDb using its TMDb ID.',
        parameters=[
            OpenApiParameter(
                name='tmdb_id',
                description='TMDb movie ID',
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH
            )
        ],
        responses={
            200: TMDbMovieDetailSerializer,
            404: OpenApiResponse(description='Movie not found on TMDb'),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class TMDbMovieDetailAPIView(APIView):
    """API view for retrieving detailed movie information from TMDb."""
    
    def get(self, request, tmdb_id):
        try:
            tmdb_service = TMDbService()
        except ValueError as e:
            return Response(
                {'error': f'TMDb API configuration error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            movie_data = tmdb_service.get_movie_details(tmdb_id)
            
            if not movie_data:
                return Response(
                    {'error': 'Movie not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = TMDbMovieDetailSerializer(movie_data)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        tags=['Genres'],
        summary='Get movie genres',
        description='Retrieve all available movie genres from TMDb API.',
        responses={
            200: OpenApiResponse(description='List of movie genres'),
            503: OpenApiResponse(description='TMDb API unavailable'),
            500: OpenApiResponse(description='Internal server error')
        }
    )
)
class TMDbGenresAPIView(APIView):
    """API view for retrieving movie genres from TMDb."""
    
    def get(self, request):
        try:
            tmdb_service = TMDbService()
        except ValueError as e:
            return Response(
                {'error': f'TMDb API configuration error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            data = tmdb_service.get_genres()
            
            if not data:
                return Response(
                    {'error': 'Unable to fetch genres from TMDb API'}, 
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            return Response(data)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        tags=['Health'],
        summary='Health check',
        description='Check the health status of the API and its dependencies.',
        responses={
            200: OpenApiResponse(description='Service is healthy'),
            503: OpenApiResponse(description='Service is unhealthy')
        }
    )
)
class HealthCheckAPIView(APIView):
    """Health check API endpoint."""
    
    def get(self, request):
        return Response({
            "status": "healthy",
            "message": "Popcornflix Django API with TMDb integration is running!",
            "features": [
                "PostgreSQL database", 
                "TMDb API integration", 
                "Movie management",
                "REST API with DRF",
                "CORS enabled for React"
            ]
        })
