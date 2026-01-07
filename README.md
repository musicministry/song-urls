# Song URLs

This repository contains video recordings, mostly from [YouTube](https://www.youtube.com), for hymns, psalms, and service music solely for rehearsal purposes:

- `hymns.yml` contains **hymns**, **songs**, **psalms**, and **anthems**
- `mass-settings.yml` contains **parts of the Mass** and other **service music**

Inclusion here does not indicate personal endorsements of any kind for any YouTube channel, publishing company, or any of the music herein. All music rights belong to the composer and/or publishing company unless otherwise noted in the video. I am not responsible for any copyright violations made by any content creator or video poster. Videos found to be in violation of copyright laws or YouTube terms of service are usually taken down by YouTube. These lists will be updated whenever that is found to have happened.

Entries are provided in `key: value` YAML format, with the name of the song as the key and the corresponding video URL as the value. When multiple versions of a song exist, such as the same text put to different melodies or multiple songs by different composers having the same name, the key includes either the hymn tune or the composer's last name, as appropriate. Psalms and other music corresponding to Bible passages generally include the scripture citation (book chapter:verse) corresponding to the refrain. For example:

```yaml
luke-1-my-soul-rejoices: https://www.youtube.com/watch?v=u9wHr_DPUhY
```

Mass parts are listed separately for each mass setting with the name of the mass setting as the top-level key and the mass parts nested beneath. For example:

```yaml
christ-the-savior:
    composer: "Dan Schutte"
    kyrie: https://youtu.be/-WKUvor5b0U?list=OLAK5uy_kQuUStdQWJnmXAvXIIF4QNXVjeqo9r1KQ
    gloria: https://www.youtube.com/watch?v=UwHpbRNYDyw&list=OLAK5uy_kQuUStdQWJnmXAvXIIF4QNXVjeqo9r1KQ
    holy: https://www.youtube.com/watch?v=a7RAweDJUPA&list=OLAK5uy_kQuUStdQWJnmXAvXIIF4QNXVjeqo9r1KQ
    memorial-acclamation-a: https://www.youtube.com/watch?v=tNKvk9Kn70Y&list=OLAK5uy_kQuUStdQWJnmXAvXIIF4QNXVjeqo9r1KQ
    memorial-acclamation-b: https://www.youtube.com/watch?v=nsGftHkvoHk&list=OLAK5uy_kQuUStdQWJnmXAvXIIF4QNXVjeqo9r1KQ
    memorial-acclamation-c: https://www.youtube.com/watch?v=pNoteywgi6M&list=OLAK5uy_kQuUStdQWJnmXAvXIIF4QNXVjeqo9r1KQ
    amen: https://www.youtube.com/watch?v=iSaIKVjsEjk&list=OLAK5uy_kQuUStdQWJnmXAvXIIF4QNXVjeqo9r1KQ
    lamb-of-god: https://www.youtube.com/watch?v=_1_sN3o9f0c&list=OLAK5uy_kQuUStdQWJnmXAvXIIF4QNXVjeqo9r1KQ
```

Both files are added to and updated regularly as needed.

Also included here is a Python package to look up hymn numbers from GIA's Gather hymnal, with others to implemented in the future. Instructions are as follows:

## Installation
```bash
pip install git+https://github.com/your-username/hymnal-data.git
```

## Usage
```python
from gather import hymns, get_hymn_number, search_hymns

# Get hymn number
number = get_hymn_number('A Hymn of Glory Let Us Sing!')

# Search hymns
results = search_hymns('Glory')
```