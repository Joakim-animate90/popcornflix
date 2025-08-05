"""
Movie models for the popcornflix application.
"""
from django.db import models
from typing import Optional


class Movie(models.Model):
    """Movie model to store movie information from TMDb API."""
    
    # TMDb fields
    tmdb_id = models.IntegerField(unique=True, help_text="TMDb movie ID")
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    overview = models.TextField(blank=True)
    
    # Release information
    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True, help_text="Runtime in minutes")
    
    # Ratings and popularity
    vote_average = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    vote_count = models.IntegerField(default=0)
    popularity = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    
    # Images
    poster_path = models.CharField(max_length=255, blank=True)
    backdrop_path = models.CharField(max_length=255, blank=True)
    
    # Additional info
    adult = models.BooleanField(default=False)
    video = models.BooleanField(default=False)
    original_language = models.CharField(max_length=10, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-popularity', '-vote_average']
        
    def __str__(self):
        return f"{self.title} ({self.release_date.year if self.release_date else 'Unknown'})"
    
    @property
    def poster_url(self) -> Optional[str]:
        """Get full poster URL."""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None
    
    @property
    def backdrop_url(self) -> Optional[str]:
        """Get full backdrop URL."""
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/w1280{self.backdrop_path}"
        return None


class Genre(models.Model):
    """Genre model for movie genres."""
    
    tmdb_id = models.IntegerField(unique=True, help_text="TMDb genre ID")
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class MovieGenre(models.Model):
    """Many-to-many relationship between movies and genres."""
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movie_genres')
    
    class Meta:
        unique_together = ('movie', 'genre')
