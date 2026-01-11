# Song URLs

This repository contains video recordings, mostly from [YouTube](https://www.youtube.com), for hymns, psalms, and service music solely for rehearsal purposes. This branch, `gather`, is unique to \[GIA\](<https://giamusic.com/sacred-music>)'s: [*Gather Third Edition*](https://giamusic.com/hymnals-gather-3) hymnal.

### `gather.yml`

This YAML file contains the full *Gather* alphabetized index, with each song title converted to hyphenated-lowercase format as the first-level key. Each song then contains a dictionary that includes the original song title from the index (`original_title`), the song number from the hymnal (`number`), and a URL[^1] for a sample YouTube video (`url`).

[^1]: URLs are manually populated as needed. Not all songs have URLS, but all have a `url` key as a placeholder.

For example, the hymn "A Hymn of Glory Let Us Sing!" is keyed `a-hymn-of-glory-let-us-sing` and contains the following:

``` yaml
a-hymn-of-glory-let-us-sing:
  number: 545
  original_title: A Hymn of Glory Let Us Sing!
  url: https://www.youtube.com/...
```

### `mass-settings.yml`

This YAML file contains a collection of Mass settings and parts, some of which are in *Gather*, others of which are not. Dictionary structure is the same as above; for example:

``` yaml
christ-the-savior-gloria:
  original_title: 'Mass of Christ the Savior: Gloria'
  number: NA
  URL: https://www.youtube.com/...
```

### `gather` module

Also included here is a Python package to look up hymn numbers from GIA's Gather hymnal:

#### Installation

``` bash
pip install git+https://github.com/your-username/song-urls.git@gather
```

#### Usage

``` python
from gather import hymns, get_hymn_number, search_hymns

# Get hymn number
number = get_hymn_number('A Hymn of Glory Let Us Sing!')

# Search hymns
results = search_hymns('Glory')
```

### *Gather* Index Creation

`gather3_index.pdf` is the original alphabetized index provided by GIA (specifically, the "Index of First Lines and Common Titles."). The [claude.ai](https://claude.ai/) Sonnet 4.5 large language model (LLM) was used to extract the content of the PDF into plain text and create functions for parsing the index into Python dictionaries. These functions and the plain-text output are found in the executable script `parse_gather_index_txt.py`. Running this script produced a cleaned[^2] and formatted YAML where each song title is a key and the song number is the value. This can be found in `gather-index.yml`.

[^2]: Mostly clean. Some manual revision was needed, but very little.

Lastly, the `gather-index.yml` structure was expanded into the full `gather.yml` [described above](#gatheryml).

### Disclaimer

Inclusion here does not indicate personal endorsements of any kind for any YouTube channel, publishing company, or any of the music herein. All music rights belong to the composer and/or publishing company unless otherwise noted in the video. I am not responsible for any copyright violations made by any content creator or video poster. Videos found to be in violation of copyright laws or YouTube terms of service are usually taken down by YouTube. These lists will be updated whenever that is found to have happened.