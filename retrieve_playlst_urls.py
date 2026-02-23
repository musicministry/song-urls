import yaml
import yt_dlp
import datetime as dt
from typing import List, Dict

# URL of any video in the YouTube playlist of interest
playlist_url = "https://www.youtube.com/watch?v=4yPHj2DFoC4&list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os"

# Year
year = dt.datetime.today().year

def video_name_psalm(feast, year=None):
    """Return the YouTube video name for the given feast `feast`. If `year` is
    None, defaults to this year."""
    if not year:
        import datetime as dt
        year = dt.datetime.today().year
    return(f"Respond & Acclaim {year} - {feast} - Psalm")

def video_name_acclm(feast, year):
    """Return the YouTube video name for the given feast `feast`. If `year` is
    None, defaults to this year."""
    if not year:
        import datetime as dt
        year = dt.datetime.today().year
    return(f"Respond & Acclaim {year} - {feast} - Gospel Acclamation")

class PlaylistRetriever:
    """Retrieve videos from YouTube playlist in sequential order"""
    
    def __init__(self, playlist_url: str):
        """
        Initialize with playlist URL
        
        Args:
            playlist_url: Full YouTube playlist URL
        """
        # Validate the URL
        self.playlist_url = self._validate_url(playlist_url)
        
    @staticmethod
    def _validate_url(url: str) -> str:
        """Validate the playlist URL"""
        # Is it actually a URL?
        if not isinstance(url, str):
            raise ValueError("URL must be a string")
        
        # Clean up, if needed
        url = url.strip()
        
        # Make sure the URL is part of a playlist
        if 'list=' not in url and not (len(url) == 34 and url.startswith('PL')):
            raise ValueError("Invalid YouTube playlist URL")
        
        # If everything passes, return the URL
        return url
    
    def get_all_videos(self, verbose: bool = False) -> List[Dict[str, str]]:
        """
        Retrieve all videos from playlist in sequential order
        
        Args:
            verbose: If True, print detailed error information
        
        Returns:
            List of dictionaries with video information (title, url, index)
        """
        ydl_opts = {
            'quiet': not verbose,
            'no_warnings': not verbose,
            'extract_flat': 'in_playlist',  # Changed from True
            'ignoreerrors': True,
            'no_color': True,
            'skip_download': True,
            'force_generic_extractor': False,
        }
        
        # Add verbose logging if requested
        if verbose:
            ydl_opts['verbose'] = True
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if verbose:
                    print(f"Fetching playlist: {self.playlist_url}")
                
                # Get playlist info
                playlist_info = ydl.extract_info(self.playlist_url, download=False)
                
                # Debug information
                if verbose:
                    print(f"Playlist info keys: {playlist_info.keys() if playlist_info else 'None'}")
                    if playlist_info and 'entries' in playlist_info:
                        print(f"Number of entries: {len(list(playlist_info['entries']))}")
                
                if not playlist_info:
                    raise RuntimeError("playlist_info is None - could not extract any information")
                
                if 'entries' not in playlist_info:
                    # Sometimes the structure is different
                    if verbose:
                        print("Available keys:", list(playlist_info.keys()))
                    raise RuntimeError(f"No 'entries' key found. Available keys: {list(playlist_info.keys())}")
                
                # List the videos in the playlist and keep track of how many
                # videos there are
                videos = []
                entry_count = 0
                none_count = 0
                
                # Loop through the playlist results
                for index, video in enumerate(playlist_info['entries'], start=1):
                    entry_count += 1
                    # There may be no available URL
                    if video is None:
                        none_count += 1
                        if verbose:
                            print(f"Entry {index}: None (skipped - likely private/deleted)")
                        continue
                    
                    # Check for video ID
                    if 'id' not in video:
                        if verbose:
                            print(f"Entry {index}: No ID field - {video.keys()}")
                        continue
                    
                    # Assemble a dictionary with video info
                    video_data = {
                        'title': video.get('title', 'Unknown Title'),
                        'index': len(videos) + 1,  # Sequential numbering of valid videos
                        'original_index': index,    # Original position including deleted videos
                        'id': video['id'],
                        'url': f"https://www.youtube.com/watch?v={video['id']}",
                        'duration': video.get('duration', 0)
                    }
                    
                    videos.append(video_data)
                    
                    if verbose:
                        print(f"✓ Entry {index}: {video_data['title']}")
                
                if verbose:
                    print(f"\nSummary: {entry_count} total entries, {none_count} unavailable, {len(videos)} valid videos")
                
                if not videos:
                    raise RuntimeError(f"No valid videos found. Processed {entry_count} entries, {none_count} were None")
                
                return videos
        
        # Handle possible (anticipated) exceptions
        except yt_dlp.utils.DownloadError as e:
            raise RuntimeError(f"yt-dlp download error: {str(e)}")
        except yt_dlp.utils.ExtractorError as e:
            raise RuntimeError(f"yt-dlp extractor error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error loading playlist: {type(e).__name__}: {str(e)}")
    
    def get_video_by_index(self, index: int) -> Dict[str, str]:
        """
        Get a specific video by its position in the playlist
        
        Args:
            index: Position in playlist (1-based indexing)
            
        Returns:
            Video information dictionary
        """
        videos = self.get_all_videos()
        
        if index < 1 or index > len(videos):
            raise ValueError(f"Index out of range. Playlist has {len(videos)} videos.")
        
        # Python zero-based indexing
        return videos[index - 1]
    
    def get_video_urls(self) -> List[str]:
        """
        Get just the URLs of all videos in order
        
        Returns:
            List of video URLs
        """
        videos = self.get_all_videos()
        return [video['url'] for video in videos]

# Get videos and feast
retriever = PlaylistRetriever(playlist_url)
videos = retriever.get_all_videos(verbose=False)

# Write to file
video_dict = {i['title'].split(f'{year} -')[1].strip():i for i in videos[1:]}
with open('ra-video-urls.yml', 'w') as file:
    yaml.safe_dump(video_dict, file)

# Feast names in YouTube playlist
video_feasts = list(dict.fromkeys([i['title'].split('-')[1].strip() for i in videos[1:]]))

# Load and sort R&A index
with open('ra-index.yml', 'r') as file:
    ra_index = yaml.safe_load(file)
ra_index = dict(sorted(ra_index.items(), key=lambda item: item[1]))

# Feast names in R&A index
ra_index_feasts = [i.split(' - ')[1].strip() for i in ra_index.keys()]
ra_index_feasts

# Map the two (generated by claude.ai and manually completed)
# Hopefully the video titles (and R&A index format) remain consistent from year
# to year. If not, this will need to be modified annually.
feast_mapping = {
    'First Sunday of Advent': 'Advent 1',
    'Second Sunday of Advent': 'Advent 2',
    'Immaculate Conception of the Blessed Virgin Mary': 'Immaculate Conception',
    'Our Lady of Guadalupe': 'Our Lady of Guadalupe',
    'Third Sunday of Advent': 'Advent 3',
    'Fourth Sunday of Advent': 'Advent 4',
    'Nativity of the Lord (Christmas): Vigil Mass': 'Nativity of the Lord: Vigil',
    'Nativity of the Lord (Christmas): Mass during the Night': 'Nativity of the Lord: Night',
    'Nativity of the Lord (Christmas): Mass at Dawn': 'Nativity of the Lord: Dawn',
    'Nativity of the Lord (Christmas): Mass during the Day': 'Nativity of the Lord: Day',
    'Holy Family of Jesus, Mary and Joseph': 'Holy Family',
    'Solemnity of Mary, the Holy Mother of God': 'Mary, Mother of God',
    'Epiphany of the Lord': 'Epiphany',
    'Baptism of the Lord': 'Baptism of the Lord',
    'Second Sunday in Ordinary Time': 'Ordinary Time 2',
    'Third Sunday in Ordinary Time': 'Ordinary Time 3',
    'Fourth Sunday in Ordinary Time': 'Ordinary Time 4',
    'Fifth Sunday in Ordinary Time': 'Ordinary Time 5',
    'Sixth Sunday in Ordinary Time': 'Ordinary Time 6',
    'Ash Wednesday': 'Ash Wednesday',
    'First Sunday of Lent': 'Lent 1',
    'Second Sunday of Lent': 'Lent 2',
    'Third Sunday of Lent': 'Lent 3',
    'Fourth Sunday of Lent': 'Lent 4',
    'Fifth Sunday of Lent': 'Lent 5',
    'Palm Sunday of the Passion of the Lord': 'Palm Sunday',
    "Thursday of the Lord's Supper (Holy Thursday): Evening Mass": 'Holy Thursday',
    'Friday of the Passion of the Lord (Good Friday)': 'Good Friday',
    'Easter Vigil in the Holy Night: After First Reading': 'Easter Vigil after First Reading',
    'Easter Vigil in the Holy Night: After First Reading (second option)': 'Easter Vigil after First Reading, second option',
    'Easter Vigil in the Holy Night: After Second Reading': 'Easter Vigil after Second Reading',
    'Easter Vigil in the Holy Night: After Third Reading': 'Easter Vigil after Third Reading',
    'Easter Vigil in the Holy Night: After Fourth Reading': 'Easter Vigil after Fourth Reading',
    'Easter Vigil in the Holy Night: After Fifth Reading': 'Easter Vigil after Fifth Reading',
    'Easter Vigil in the Holy Night: After Sixth Reading': 'Easter Vigil after Sixth Reading',
    'Easter Vigil in the Holy Night: After Seventh Reading, Baptim': 'Easter Vigil after Seventh Reading, Baptism',
    'Easter Vigil in the Holy Night: After Seventh Reading (second option)': 'Easter Vigil after Seventh Reading, second option',
    'Easter Vigil in the Holy Night: After Seventh Reading (third option)': 'Easter Vigil after Seventh Reading, third option',
    'Easter Vigil in the Holy Night: After the Epistle': 'Easter Vigil after the Epistle',
    'Easter Sunday of the Resurrection of the Lord: Mass during the Day': 'Easter Sunday',
    'Second Sunday of Easter (or Sunday of Divine Mercy)': 'Easter 2',
    'Third Sunday of Easter': 'Easter 3',
    'Fourth Sunday of Easter': 'Easter 4',
    'Fifth Sunday of Easter': 'Easter 5',
    'Sixth Sunday of Easter': 'Easter 6',
    'Ascension of the Lord': 'Ascension',
    'Seventh Sunday of Easter': 'Easter 7',
    "Pentecost Sunday: Vigil Mass (Extended Form): After First Reading": 'Pentecost Vigil after First Reading',
    "Pentecost Sunday: Vigil Mass (Extended Form): After Second Reading": 'Pentecost Vigil after Second Reading',
    "Pentecost Sunday: Vigil Mass (Extended Form): After Second Reading (second option)": 'Pentecost Vigil after Second Reading, second option',
    "Pentecost Sunday: Vigil Mass (Extended Form): After Third Reading": 'Pentecost Vigil after Third Reading',
    "Pentecost Sunday: Vigil Mass (Extended Form): After Fourth Reading": 'Pentecost Vigil after Fourth Reading',
    'Pentecost Sunday: Mass during the Day': 'Pentecost Sunday',
    'Most Holy Trinity': 'Most Holy Trinity',
    'Most Holy Body and Blood of Christ (Corpus Christi)': 'Corpus Christi',
    'Eleventh Sunday in Ordinary Time': 'Ordinary Time 11',
    'Twelfth Sunday in Ordinary Time': 'Ordinary Time 12',
    'Thirteenth Sunday in Ordinary Time': 'Ordinary Time 13',
    'Fourteenth Sunday in Ordinary Time': 'Ordinary Time 14',
    'Fifteenth Sunday in Ordinary Time': 'Ordinary Time 15',
    'Sixteenth Sunday in Ordinary Time': 'Ordinary Time 16',
    'Seventeenth Sunday in Ordinary Time': 'Ordinary Time 17',
    'Eighteenth Sunday in Ordinary Time': 'Ordinary Time 18',
    'Nineteenth Sunday in Ordinary Time': 'Ordinary Time 19',
    'Assumption of the Blessed Virgin Mary: Vigil Mass': 'Assumption: Vigil',
    'Assumption of the Blessed Virgin Mary: Mass during the Day': 'Assumption',
    'Twentieth Sunday in Ordinary Time': 'Ordinary Time 20',
    'Twenty-First Sunday in Ordinary Time': 'Ordinary Time 21',
    'Twenty-Second Sunday in Ordinary Time': 'Ordinary Time 22',
    'Twenty-Third Sunday in Ordinary Time': 'Ordinary Time 23',
    'Twenty-Fourth Sunday in Ordinary Time': 'Ordinary Time 24',
    'Twenty-Fifth Sunday in Ordinary Time': 'Ordinary Time 25',
    'Twenty-Sixth Sunday in Ordinary Time': 'Ordinary Time 26',
    'Twenty-Seventh Sunday in Ordinary Time': 'Ordinary Time 27',
    'Twenty-Eighth Sunday in Ordinary Time': 'Ordinary Time 28',
    'Twenty-Ninth Sunday in Ordinary Time': 'Ordinary Time 29',
    'Thirtieth Sunday in Ordinary Time': 'Ordinary Time 30',
    'All Saints': 'All Saints',
    'All Souls': 'All Souls',
    'Thirtieth-First Sunday in Ordinary Time': 'Ordinary Time 31',
    'Thirty-Second Sunday in Ordinary Time': 'Ordinary Time 32',
    'Thirty-Third Sunday in Ordinary Time': 'Ordinary Time 33',
    'Our Lord Jesus Christ, King of the Universe': 'Christ the King',
    'Thanksgiving Day': 'Thanksgiving',
}

# Write to file
with open('feast-mapping.yml', 'w') as file:
    yaml.safe_dump(feast_mapping, file)
