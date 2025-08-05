"""
Management command to sync movie genres from TMDb API.
"""
from django.core.management.base import BaseCommand
from movies.services import TMDbService
from movies.models import Genre


class Command(BaseCommand):
    """Sync movie genres from TMDb API."""
    
    help = 'Sync movie genres from TMDb API'

    def handle(self, *args, **options):
        """Execute the command."""
        try:
            tmdb_service = TMDbService()
            self.stdout.write('Fetching genres from TMDb...')
            
            genres_data = tmdb_service.get_genres()
            if not genres_data:
                self.stdout.write(
                    self.style.ERROR('Failed to fetch genres from TMDb API')
                )
                return
            
            genres = genres_data.get('genres', [])
            created_count = 0
            updated_count = 0
            
            for genre_data in genres:
                genre, created = Genre.objects.update_or_create(
                    tmdb_id=genre_data['id'],
                    defaults={'name': genre_data['name']}
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'Created genre: {genre.name}')
                else:
                    updated_count += 1
                    self.stdout.write(f'Updated genre: {genre.name}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully synced genres: {created_count} created, {updated_count} updated'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error syncing genres: {str(e)}')
            )
