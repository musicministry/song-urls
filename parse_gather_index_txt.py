# =============================================================================
# parse_gather_index_txt.py
#
# This script takes the Gather index, extracted from the PDF document and
# converted to simple text by claude.ai, and parses it into a Python dictionary
# with the song name as the key and the number as the value. This dictionary is
# written to file `gather.py` along with some utility functions for querying
# the dictionary.
# 
# The script looks for a new line starting with a number; lines that start with
# text are taken to be continuations of the previous line. Minor corrections
# have been made manually to facilitate this process.
#
# =============================================================================
"""
Parse hymnal index from document text and create Python data file.

The complete text from the PDF was extracted by claude.ai into one long text
string, which is then parsed by the functions below.
"""
import re

def parse_hymnal_complete():
    """Parse complete hymnal index from document text."""
    
    # Complete text from your PDF
    text = """664 A Celtic Rune
545 A Hymn of Glory Let Us Sing!
677 A Living Faith
687 A Mighty Fortress Is Our God
971 A Nuptial Blessing
812 A Place at the Table
416 A Voice Cries Out
811 Abundant Life
621 Ad Te Jesu Christe
439 Adéste Fidéles / O Come, All Ye 
Faithful / Venid, Fieles Todos 
476 Adorámus Te Christe
411 Advent Alleluia
405 Advent Gathering Song
487 Again We Keep This Solemn Fast
881 Alcen la Cruz / Lift High the Cross
850 All Are Welcome
611 All Creatures of Our God and King
605 All Glory Is Yours
498 All Glory, Laud, and Honor
570 All Hail the Power of Jesus' Name!
853 All People That on Earth Do Dwell
892 All that I am sings 
792 All that I counted as gain
746 All That Is Hidden
604 All the Ends of the Earth
70 All the Ends of the Earth - Psalm 98
541 All Things New
925 All Who Hunger (Moore)
852 All Who Hunger, Gather Gladly 
(HOLY MANNA)
693 All Will Be Well
575 All You Works of God
518 Alleluia, Christ Is Risen
844 Alleluia! Give the Glory
524 Alleluia No. 1
949 Alleluia! Sing to Jesus!
645 Amazing Grace
684 Amazing grace (Goebel-Komala)
912 Amén. El Cuerpo de Cristo
984 America the Beautiful
888 Among All
102 And holy is your name
438 Angels, from the Realms of Glory
430 Angels We Have Heard on High
778 Anthem
744 As a Fire Is Meant for Burning
839 As We Gather at Your Table
906 As we journeyed on our way
465 As with Gladness Men of Old
962 Ashes
857 At Evening
914 At That First Eucharist (Lord, Who at 
Your First Eucharist)
488 At the Cross Her Station Keeping
536 At the Lamb's High Feast We Sing
569 At the Name of Jesus
948 At the Table of Jesus
887 Ave María (Chant)
891 Ave María (Kantor)
423 Awake! Awake, and Greet the New 
Morn
766 Awake from your slumber
399 Awake to the Day
448 Away in a Manger
755 Bambelela / Never Give Up
903 Baptized in Water
526 Be Joyful, Mary
51 Be Merciful, O Lord - Psalm 51 
(Haugen)
52 Be Merciful, O Lord - Psalm 51 
(Pishner)
54 Be Merciful, O Lord - Psalm 51 (Tate)
683 Be Not Afraid (Dufford)
516 Be Not Afraid (Taizé)
65 Be with Me - Psalm 91
22 Before the ending of the day
939 Behold the Lamb
514 Behold the Wood
789 Bendecidos, Somos Santos / Blest Are 
We
735 Benditos los Pobres / Blest Are They
620 Bless the Lord
592 Blessed are they who are poor in spirit
900 Blessed be God!
735 Blest Are They / Benditos los Pobres
86 Blest Are Those Who Love You - 
Psalm 128
789 Blest Are We / Bendecidos, Somos 
Santos
686 Blest Be the Lord
700 Boundless Love / Tình Chúa Cao Vòi
947 Bread of Life, Cup of Blessing
943 Bread of Life from Heaven / Pan de 
Vida Eterna
734 Bring Forth the Kingdom
754 Build Us a Table
672 By the Waters of Babylon
767 Called by Christ
924 Canción del Cuerpo de Cristo / Song 
of the Body of Christ
539 Canten con Gloriosos Fieles / Sing 
with All the Saints in Glory
99 Canticle of Daniel - Daniel 3:57-88
576 Canticle of the Sun
622 Canticle of the Turning
443 Carol at the Manger
679 Center of My Life
493 Change Our Hearts
431 Child of Mercy
452 Chill of the nightfall
896 Christ Be in Your Senses
590 Christ, Be Our Light!
760 Christ Has No Body Now But Yours
851 Christ Has Promised to Be Present
530 Christ Has Risen
522 Christ is alive and goes before us
745 Christ Is Made the Sure Foundation
521 Christ Is Risen! Shout Hosanna!
571 Christ Is the King!
523 Christ the Lord Is Risen Today
766 City of God
442 Cold are the people
849 Come All You People / Uyai Mose 
942 Come and Eat This Living Bread
637 Come and Fill Our Hearts / Confitémini 
Dómino
800 Come and Follow Me
788 Come and Journey with a Savior
714 Come and rest in the arms of God
484 Come back to me
800 Come, be my light
405 Come, come Emmanuel
838 Come, come to the banquet
556 Come Down, O Love Divine
559 Come, Holy Ghost
846 Come, Host of Heaven's High Dwelling 
Place
807 Come! Live in the light!
552 Come, Lord Jesus
577 Come, O God of all the earth
482 Come, O God, renew your people
403 Come, O Long-Expected Jesus
562 Come Now, Almighty King
739 Come now, the feast is spread
720 Come to Me (Bell)
731 Come to Me (Joncas)
871 Come to me, all you weary
842 Come to me, come to us
727 Come to Me, O Weary Traveler
931 Come to the Banquet
585 Come to the Feast
838 Come to the Feast / Ven al Banquete
584 Come to the Water (Foley)
899 Come to the water
842 Come to Us
533 Come, You Faithful, Raise the Strain
634 Come, You Thankful People, Come
413 Comfort, Comfort, O My People
396 Comfort, My People
836 Coming Together for Wine and for 
Bread
637 Confitémini Dómino / Come and Fill 
Our Hearts
721 Contigo Estoy / You Are Mine
904 Covenant Hymn
420 Creator of the Stars of Night
574 Crown Him with Many Crowns
918 Cuando Partimos el Pan del Señor / In 
the Breaking of the Bread
99 Daniel 3:57-88: Canticle of Daniel
434 Dark is the night
858 Day Is Done
486 Deep Within
750 Deliver Us, O Lord of Truth
676 Digo "Sí," Señor / I Say "Yes," Lord
833 Diverse in Culture, Nation, Race
869 Do Not Let Your Hearts Be Troubled
506 Do you know what I have done
719 Don't Be Afraid
711 Don't be afraid, for I am with you
822 Dona Nobis Pacem
935 Draw Near
425 Dream a Dream
468 Dust and Ashes
976 Dwellers in the Holy City
678 Dwelling Place 
974 Dying you destroyed our death
419 Each Winter As the Year Grows Older
691 Eagle's Wings
531 Earth, Earth, Awake!
537 Easter Alleluia
941 Eat This Bread
79 El Cáliz que Bendecimos - Psalm 116
599 El Cielo Canta Alegría / Heaven Is 
Singing for Joy
786 El Corazón de un Buen Pastor / Heart 
of a Shepherd
74 El Señor Es Compasivo - Psalm 103
36 El Señor Es Mi Pastor - Psalm 23
906 Emmaus
105 Emptied and humbled, obedient to 
death
415 En el Silencio Te Aguardo / My Soul 
in Stillness Waits
462 Epiphany Carol
710 Even though the rain hides the stars
60 Every Nation on Earth - Psalm 72
462 Every nation sees the glory
517 Ewe, Thina / We Walk His Way
95 Exodus 15: Song at the Sea
96 Exodus 15: Song of Moses
728 Eye Has Not Seen
677 Faith of our fathers 
702 Faith, Hope and Love
700 Far beyond the reach of endless sky
43 Father, into Your Hands - Psalm 31
632 Father, We Thank You, Who Have 
Planted
489 Feed us and guide us
884 For All the Saints
885 For All the Saints Who've Shown Your 
Love
64 For Ever I Will Sing - Psalm 89
812 For everyone born, a place at the table
580 For God So Loved the World
927 For Living, for Dying
633 For the Beauty of the Earth
631 For the bread and wine 
883 For the Faithful Who Have Answered
803 For the Healing of the Nations
901 For the Life of the World
415 For you, O Lord, my soul
608 For your sun that brightens the day
965 Forgive Our Sins
483 Forty Days and Forty Nights
814 Freedom Is Coming
587 Fresh as the Morning
474 From Ashes to the Living Font
936 Gather in Your Name
848 Gather Us In
489 Gather your people (Alonso)
837 Gather Your People (Hurd)
841 Gathered as One
940 Gift of Finest Wheat
422 Gift of God
826 Give Us Your Peace
426 Glória, Glória
606 Glory and Praise to Our God
501 Glory in the Cross
771 Go in Peace, Go in Love
775 Go Make a Difference
769 Go Make of All Disciples
762 Go Out to the World
428 Go Tell It on the Mountain
546 Go to the World!
761 God Has Chosen Me
959 God Is Forgiveness
843 God Is Here! As We His People
699 God Is Love
99 God is praised and exalted
595 God Is Still Speaking
50 God Mounts His Throne - Psalm 47
982 God of Adam, God of Joseph
412 God of All People
412 God of all places
859 God of Day and God of Darkness
983 God of Eve and God of Mary
587 God of the Bible
669 God Remembers
435 God Rest You Merry, Gentlemen
759 God Sends Us Forth
673 God Weeps with Us Who Weep and 
Mourn
715 God Will Wipe the Tears
970 God, in the Planning
813 God, Whose Purpose Is to Kindle
661 God, you have moved upon the waters
440 Good Christian Friends, Rejoice
768 Good News
528 Goodness Is Stronger than Evil
397 Gracious God of wisdom
780 Guide My Feet 
915 Gusten y Vean / Taste and See
879 Hail, Holy Queen Enthroned Above
891 Hail Mary, full of grace (Kantor)
889 Hail Mary, full of grace (Landry)
889 Hail Mary: Gentle Woman
509 Hail Our Savior's Glorious Body / 
Pange Lingua
880 Hail, Queen of Heaven / Salve, Regína
543 Hail the Day That Sees Him Rise
626 Halleluya! We Sing Your Praises
954 Hands of Healing
424 Hark! The Herald Angels Sing
53 Have Mercy, Lord - Psalm 51
429 He Came Down
953 He Healed the Darkness of My Mind
960 Healer of Our Every Ill
643 Healing River
665 Healing River of the Spirit
786 Heart of a Shepherd / El Corazón de 
un Buen Pastor
599 Heaven Is Singing for Joy / El Cielo 
Canta Alegría
804 Here Am I
48 Here I Am - Psalm 40 (Alonso)
49 Here I Am - Psalm 40 (Cooney)
777 Here I Am, Lord
907 Here in the Bread that is broken
848 Here in this place
494 Hold Us in Your Mercy: Penitential 
Litany
652 Hold Us, Jesus
561 Holy and blessed Three
443 Holy child within the manger
629 Holy God
615 Holy God, We Praise Thy Name
567 Holy, Holy, Holy! Lord God Almighty!
102 Holy Is Your Name - Luke 1:46-55
547 Holy Spirit, Come to Us
499 Hosanna
484 Hosea
685 How Can I Keep from Singing?
772 How Can We Be Silent
694 How Firm a Foundation
877 How Good, Lord, to Be Here!
578 How Great Thou Art
667 How Shall We Name God?
563 How Wonderful the Three-in-One
69 Hoy Nos Ha Nacido un Salvador - 
Psalm 96
924 Hoy venimos a contar
794 I Am for You
682 I Am Sure I Shall See
945 I Am the Bread of Life / Yo Soy el Pan 
de Vida
816 I am the hungry
758 I baptize you in the name of the Father
919 I Come with Joy
796 I Danced in the Morning 
678 I fall on my knees
718 I Have Been Anointed
492 I have fixed my eyes
588 I Have Loved You
724 I Heard the Voice of Jesus Say
527 I Know That My Redeemer Lives! 
(DUKE STREET)
972 I Know That My Redeemer Lives 
(Haas)
973 I Know That My Redeemer Lives 
(Hughes)
659 I Lift My Soul to You
916 I Receive the Living God
676 I Say "Yes," Lord / Digo "Sí," Señor
758 I Send You Out
458 I Sing a Maid
777 I, the Lord, of sea and sky
593 I Want to Walk as a Child of the Light
872 I Will Be the Vine
802 I Will Choose Christ
721 I will come to you in the silence
93 I Will Praise the Lord - Psalm 146
42 I Will Praise You, Lord - Psalm 30
92 I Will Praise Your Name - Psalm 145
603 I Will Sing a Song of Love
96 I will sing, I will sing to the God who 
sets me free
957 If I Have Been the Source of Pain / Si 
Fui Motivo de Dolor
66 If Today You Hear God's Voice - 
Psalm 95
818 If You Believe and I Believe
787 If you lose your life
786 If you love me, feed my lambs
746 If you would follow me
886 Immaculate Mary
447 In a far-off place, Jesus comes to earth
832 In Christ There Is No East or West
716 In Every Age
513 In Manus Tuas, Pater
977 In Paradísum / May Choirs of Angels
944 In Remembrance of You
714 In the Arms of God
918 In the Breaking of the Bread / Cuando 
Partimos el Pan del Señor
515 In the Cross of Christ
639 In the Lord I'll Be Ever Thankful
655 Increase Our Faith
445 Infant Holy, Infant Lowly
97 Isaiah 12: With Joy You Shall Draw 
Water
98 Isaiah 12: You Will Draw Water 
Joyfully / Sacarán Aguas con Alegría 
433 It Came upon the Midnight Clear
492 Jerusalem, My Destiny
870 Jerusalem, My Happy Home
505 Jesu, Jesu
847 Jesucristo Ayer / Jesus Christ, 
Yesterday, Today, and for Ever
105 Jesus Christ Is Lord! - Philippians 2:6-11
540 Jesus Christ Is Risen Today
847 Jesus Christ, Yesterday, Today, and for 
Ever / Jesucristo Ayer
447 Jesus Comes
826 Jesus, give us your peace
952 Jesus, Heal Us
944 Jesus, hope for all
909 Jesus, Hope of the World
757 Jesus in the Morning
934 Jesus Is Here Right Now
840 Jesus Is the Resurrection
589 Jésus le Christ / Lord Jesus Christ
732 Jesus, Lead the Way
507 Jesus, our teacher and our Lord
510 Jesus, Remember Me
921 Jesus, the living Bread of God
491 Jesus, the Lord
752 Jesus, Your Spirit in Us
437 Joy to the World
614 Joyful, Joyful, We Adore You
929 Joyous Cup
618 Jubiláte, Sérvite
646 Keep in Mind
29 Keep Me Safe, O God - Psalm 16
674 Ki Ri Su To No / May the Peace of 
Christ Be with You
495 Kneeling in the garden grass
472 Kýrie (Browning)
490 Kýrie (Haugen)
820 La Paz de la Tierra / The Peace of the 
Earth
623 Laudáte Dóminum
601 Laudáte, Laudáte Dóminum
656 Lead Me, Guide Me
827 Lead us from death to life
619 Let All Mortal Flesh Keep Silence
59 Let All the Earth - Psalm 66
635 Let All Things Now Living
810 Let Justice Roll Like a River
954 Let our hands be hands of healing
561 Let There Be Light
829 Let There Be Peace on Earth
946 Let Us Be Bread
850 Let us build a house
84 Let Us Go Rejoicing - Psalm 122
81 Let Us Rejoice - Psalm 118
823 Let your gentleness be known
44 Let Your Mercy Be on Us - Psalm 33
890 Letanía de la Santísima Virgen María / 
Litany of Mary
926 Life-Giving Bread, Saving Cup
881 Lift High the Cross / Alcen la Cruz
624 Lift Up Your Hearts
408 Like a Bird
402 Like a Shepherd
890 Litany of Mary / Letanía de la 
Santísima Virgen María
549 Living Spirit, Holy Fire
451 Lo, How a Rose E'er Blooming
583 Long before my journey's start
716 Long before the mountains came to be
590 Longing for light
779 Look to Christ
664 Lord, hear our prayer
602 Lord, I Lift Your Name on High
655 Lord, increase our faith
477 Lord Jesus Christ
589 Lord Jesus Christ / Jésus le Christ
62 Lord, Let Us See Your Kindness - 
Psalm 85
662 Lord, make us worthy
663 Lord of All Hopefulness
703 Lord of All Nations, Grant Me Grace
76 Lord, Send Out Your Spirit - Psalm 104 (Lisicky)
77 Lord, Send Out Your Spirit - Psalm 104 (Proulx)
464 Lord, Today
781 Lord, When You Came / Pescador de 
Hombres
914 Lord, Who at Your First Eucharist
479 Lord, Who throughout These Forty 
Days
764 Lord, Whose Love in Humble Service
544 Lord, You Give the Great Commission
32 Lord, You Have the Words - Psalm 19 
(Alonso)
31 Lord, You Have the Words - Psalm 19 
(Haas)
799 Lord, you lead through sea and desert
641 Love Divine, All Loves Excelling
698 Love Endures All Things
969 Love Has Brought Us Here Together
90 Love Is Never Ending - Psalm 136
967 Love Is the Sunlight
100 Luke 1:46-53: My Soul Gives Glory
102 Luke 1:46-55: Holy Is Your Name
101 Luke 1:46-55: Magníficat
103 Luke 1:68-79: Now Bless the God of 
Israel
104 Luke 2:29-34: Nunc Dimíttis
892 Magníficat (Haas)
101 Magníficat - Luke 1:46-55 
(Chepponis)
630 Magníficat (Taizé)
828 Make Me a Channel of Your Peace
958 Make Us Turn to You
662 Make Us Worthy
845 Making Their Way
911 Many and Great
841 Many faces, the young and the old
410 Maranatha, Come
397 Maranatha, Lord Messiah
893 Mary, First among Believers
977 May Choirs of Angels / In Paradísum
675 May God Bless and Keep You
971 May God bless you
978 May Holy Angels Lead You
980 May the Angels Lead You into 
Paradise 
674 May the Peace of Christ Be with You / 
Ki Ri Su To No
793 May the Spirit of Christ
394 May We Be One (Communion Hymn)
393 May We Be One (Communion Litany)
806 May we find richness
489 Merciful God
480 Mercy, O God
985 Mine Eyes Have Seen the Glory
831 Miren Qué Bueno / Oh, Look and 
Wonder
54 Misericordia, Señor - Psalm 51
855 Morning Has Broken
834 Muchos Miembros Hay / We Are 
Many Parts
988 My Country, 'Tis of Thee
33 My God, My God - Psalm 22
685 My life flows on in endless song
723 My shepherd is the Lord (O'Brien)
34 My Shepherd Is the Lord - Psalm 23
704 My Song Will Be for You Forever
622 My soul cries out
894 My Soul Gives Glory (Duncan)
100 My Soul Gives Glory - Luke 1:46-53 
(Joncas)
415 My Soul in Stillness Waits / En el 
Silencio Te Aguardo
89 My Soul Is Still - Psalm 131
55 My Soul Is Thirsting - Psalm 63 
(Joncas)
56 My Soul Is Thirsting - Psalm 63 
(Proulx)
73 My Soul, Give Thanks to the Lord - 
Psalm 103
733 Nada Te Turbe / Nothing Can Trouble
432 Nativity Carol
647 Neither Death nor Life
755 Never Give Up / Bambelela
442 Night of Silence
701 No Greater Love
876 No Wind at the Window 
441 Noche de Paz / Silent Night
709 Not for Tongues of Heaven's Angels
697 Nothing Can Ever
733 Nothing Can Trouble / Nada Te Turbe
927 Nourish us well
103 Now Bless the God of Israel - Luke 
1:68-79
937 Now in This Banquet
857 Now it is evening
874 Now Let Your Servant Go in Peace
104 Now, O Lord, dismiss your servants
636 Now Thank We All Our God
534 Now the Green Blade Rises
785 Now We Remain
104 Nunc Dimíttis - Luke 2:29-34
984 O beautiful for spacious skies
902 O Breathe on Me, O Breath of God
439 O Come, All Ye Faithful / Venid, Fieles 
Todos / Adéste Fidéles 
401 O Come, Divine Messiah!
395 O Come, O Come, Emmanuel
814 O Freedom
566 O God, Almighty Father
598 O God beyond All Praising
825 O God of Every Nation
648 O God of Exodus
688 O God, Our Help in Ages Past
37 O God, This Is the People - Psalm 24
668 O God, Why Are You Silent?
581 O God, You Search Me
863 O Holy City, Seen of John
551 O Holy Spirit, by Whose Breath
584 O let all who thirst
446 O Little Town of Bethlehem
666 O Lord, Hear My Prayer
695 O Lord, I know you are near
578 O Lord my God, when I in awesome 
wonder
654 O Lord, the Guardian of My Heart
679 O Lord, you are the center of my life
895 O Most Holy One / O Sanctíssima
13 O radiant light
512 O Sacred Head Surrounded / Oh 
Rostro Ensangrentado
895 O Sanctíssima / O Most Holy One
532 O Sons and Daughters
553 O Spirit All-Embracing
917 O Taste and See
864 O the weary world is trudging
427 Of the Father's Love Begotten
512 Oh Rostro Ensangrentado / O Sacred 
Head Surrounded
585 Oh, everyone who thirsts
831 Oh, Look and Wonder / Miren Qué 
Bueno
691 On Eagle's Wings
809 On Holy Ground
418 On Jordan's Bank
862 On That Day
538 On the Journey to Emmaus
455 Once in Royal David's City
932 One Bread, One Body
770 One Lord
782 Only This I Want
729 Only You, O God
651 Open My Eyes
79 Our Blessing-Cup - Psalm 116 
(Alonso)
78 Our Blessing-Cup - Psalm 116 
(Haugen)
956 Our Father, We Have Wandered
83 Our Help Comes from the Lord - 
Psalm 121
88 Out of the Depths - Psalm 130
579 Over My Head
43 Padre, a Tus Manos - Psalm 31
32 Palabras de Vida Eterna - Psalm 19
496 Palm Sunday Processional
920 Pan de Vida
943 Pan de Vida Eterna / Bread of Life 
from Heaven
509 Pange Lingua / Hail Our Savior's 
Glorious Body
473 Parce Dómine
830 Peace, Be Not Anxious
975 Peace Be with Those
821 Peace before us, peace behind us
819 Peace Is Flowing Like a River
409 People, Look East
407 People of the Night
781 Pescador de Hombres / Lord, When 
You Came
105 Philippians 2:6-11: Jesus Christ Is 
Lord!
861 Praise and Thanksgiving
94 Praise God in This Holy Dwelling - 
Psalm 150
613 Praise, My Soul, the King of Heaven
597 Praise Our God and Savior
565 Praise the God who changes places
625 Praise the One Who Breaks the 
Darkness
616 Praise to the Lord, the Almighty
596 Praise to You, O Christ, Our Savior
875 Praise We the Lord This Day
821 Prayer of Peace
955 Precious Lord, Take My Hand
504 Prepare a Room for Me
398 Prepare! Prepare!
400 Prepare the Way of the Lord
101 Proclaim the greatness of God
67 Proclaim to All the Nations - Psalm 96
28 Psalm 15: They Who Do Justice
29 Psalm 16: Keep Me Safe, O God
30 Psalm 16: You Will Show Me the Path 
of Life
31 Psalm 19: Lord, You Have the Words
32 Psalm 19: Words of Everlasting Life / 
Palabras de Vida Eterna
33 Psalm 22: My God, My God
34 Psalm 23: My Shepherd Is the Lord
35 Psalm 23: Shepherd Me, O God
36 Psalm 23: The Lord Is My Shepherd / 
El Señor Es Mi Pastor
37 Psalm 24: We Long to See Your Face
38 Psalm 25: Remember Your Mercies
39 Psalm 25: To You, O Lord (Haugen)
40 Psalm 25: To You, O Lord (Pishner)
41 Psalm 27: The Lord Is My Light
42 Psalm 30: I Will Praise You, Lord
43 Psalm 31: Father, into Your Hands / 
Padre, a Tus Manos
44 Psalm 33: Let Your Mercy Be on Us / 
Señor, Que Tu Misericordia
45 Psalm 34: Taste and See (Haugen)
46 Psalm 34: Taste and See (Guimont)
47 Psalm 34: The Cry of the Poor
48 Psalm 40: Here I Am (Alonso)
49 Psalm 40: Here I Am (Cooney)
50 Psalm 47: God Mounts His Throne
51 Psalm 51: Be Merciful, O Lord 
(Haugen)
52 Psalm 51: Be Merciful, O Lord 
(Pishner)
53 Psalm 51: Have Mercy, Lord
54 Psalm 51: Misericordia, Señor / Be 
Merciful, O Lord
55 Psalm 63: My Soul Is Thirsting 
(Joncas)
56 Psalm 63: My Soul Is Thirsting 
(Proulx)
57 Psalm 63: My Soul Is Thirsting 
(Angrisano)
58 Psalm 63: Your Love Is Finer than Life
59 Psalm 66: Let All the Earth
60 Psalm 72: Every Nation on Earth
61 Psalm 84: How Lovely Is Your 
Dwelling Place
62 Psalm 85: Lord, Let Us See Your 
Kindness
63 Psalm 88: Day and Night
64 Psalm 89: For Ever I Will Sing
65 Psalm 91: Be with Me
33 Psalm 95: If Today You Hear God's
Voice
67 Psalm 96: Proclaim to All the Nations
68 Psalm 96: Today Is Born Our Savior
69 Psalm 96: Today Is Born Our Savior /
Hoy Nos Ha Nacido un Salvador
70 Psalm 98: All the Ends of the Earth
71 Psalm 100: We Are God's People
73 Psalm 103: My Soul, Give Thanks to
the Lord
72 Psalm 103: The Lord Is Kind and
Merciful (Cotter)
75 Psalm 103: The Lord Is Kind and
Merciful (Haugen)
74 Psalm 103: The Lord Is Kind and
Merciful / El Señor Es Compasivo
76 Psalm 104: Lord, Send Out Your Spirit
(Lisicky)
77 Psalm 104: Lord, Send Out Your Spirit
(Proulx)
78 Psalm 116: Our Blessing-Cup
79 Psalm 116: Our Blessing-Cup / El
Cáliz que Bendecimos
80 Psalm 116: The Name of God
81 Psalm 118: Let Us Rejoice
82 Psalm 118: This Is the Day
83 Psalm 121: Our Help Comes from the
Lord
84 Psalm 122: Let Us Go Rejoicing
(Joncas)
85 Psalm 122: Let Us Go Rejoicing
(Roberts)
86 Psalm 128: Blest Are Those Who Love
You
88 Psalm 130: Out of the Depths
87 Psalm 130: With the Lord There Is
Mercy
89 Psalm 131: My Soul Is Still
90 Psalm 136: Love Is Never Ending
91 Psalm 138: The Fragrance of Christ
92 Psalm 145: I Will Praise Your Name
93 Psalm 146: I Will Praise the Lord
94 Psalm 150: Praise God in This Holy
Dwelling
684 Psalm of Hope
756 Pues Si Vivimos / When We Are Living
824 Put Peace into Each Other's Hands
713 Quietly, Peacefully
582 Rain Down
568 Rejoice, the Lord Is King!
469 Remember You Are Dust
961 Remember Your Love
38 Remember Your Mercies - Psalm 25
711 Rest Now in Me
535 Resucitó
478 Return to God / Volvamos Hoy a
Nuestro Dios
471 Return to the Lord
497 Ride On, Jesus, Ride
453 Rise Up, Shepherd, and Follow
98 Sacarán Aguas con Alegría / You Will
Draw Water Joyfully - Isaiah 12
880 Salve, Regína / Hail, Queen of Heaven
421 Savior of the Nations, Come
658 Seek Ye First
557 Send Down the Fire
776 Send Me, Jesus / Thuma Mina
552 Send Us Your Spirit
44 Señor, Que Tu Misericordia - Psalm 33
1065 Sequence for Easter
1084 Sequence for Pentecost
708 Set Your Heart on the Higher Gifts
649 Shall Tribulation or Distress
873 Shall We Gather at the River
717 Shelter Me, O God
35 Shepherd Me, O God - Psalm 23
723 Shepherd of My Heart
910 Shepherd of Souls
957 Si Fui Motivo de Dolor / If I Have
Been the Source of Pain
786 Si me amas
489 Sign us with ashes
441 Silent Night / Noche de Paz
432 Silent, in the chill of midnight
743 Sing a New Church
541 Sing a new song (Cooney)
607 Sing a New Song (Schutte)
627 Sing a New Song to the Lord
434 Sing Alleluia
457 Sing of Mary, Pure and Lowly
610 Sing of the Lord's Goodness
577 Sing Out, Earth and Skies!
600 Sing Praise to God
519 Sing to the Mountains
539 Sing with All the Saints in Glory /
Canten con Gloriosos Fieles
3 Sing your joy, proclaim God's glory!
670 Sitting with a child in sickness
594 Siyahamba / We Are Marching
929 Slaves and children, take a stand
507 So You Must Do
963 Softly and Tenderly Jesus Is Calling
470 Somebody's Knockin' at Your Door
741 Somos el Cuerpo de Cristo / We Are
the Body of Christ
95 Song at the Sea - Exodus 15
974 Song of Farewell
96 Song of Moses - Exodus 15
793 Song of St. Patrick
924 Song of the Body of Christ / Canción
del Cuerpo de Cristo
506 Song of the Lord's Command
508 Song of the Lord's Supper
452 Song of the Stable
661 Song over the Waters
459 Songs of Thankfulness and Praise
865 Soon and Very Soon
667 Source and sovereign, rock and cloud
473 Spare us, gracious Lord
555 Spirit Blowing through Creation
554 Spirit of God
560 Spirit Wind
763 Stand Firm
763 Stand, O stand firm
565 Stand Up, Friends!
449 Star-Child
495 Stations of the Cross
502 Stay Here and Keep Watch
868 Steal Away to Jesus
743 Summoned by the God who made us
529 Surréxit Christus
899 Sweet Refreshment
923 Table Song
950 Take and Eat
928 Take and Eat This Bread
908 Take and Eat, This Is My Body
866 Take Me Home
650 Take my heart, O Lord
801 Take Up Your Cross (ERHALT UNS
HERR)
787 Take Up Your Cross (Haas)
795 Take, O Take Me As I Am
930 Taste and See
45 Taste and See - Psalm 34
915 Taste and See / Gusten y Vean
542 That Easter Day with Joy Was Bright
456 The Aye Carol
707 The Call Is Clear and Simple
765 The Church of Christ
742 The Church's One Foundation
710 The Clouds' Veil
482 The Cross of Jesus
47 The Cry of the Poor - Psalm 34
460 The First Nowell
91 The Fragrance of Christ - Psalm 138
481 The Glory of These Forty Days
989 The God of All Eternity
981 The Hand of God Shall Hold You
806 The Harvest of Justice
576 The heavens are telling the glory of
God
809 The heavens embrace the earth
572 The King of Glory
712 The King of Love My Shepherd Is
414 The King Shall Come When Morning
Dawns
736 The Kingdom of God (LAUDATE
DOMINUM)
740 The Kingdom of God (Taizé)
921 The Living Bread of God
72 The Lord Is Kind and Merciful -
Psalm 103 (Cotter)
74 The Lord Is Kind and Merciful -
Psalm 103 (Alonso)
75 The Lord Is Kind and Merciful -
Psalm 103 (Haugen)
690 The Lord Is My Light (Bouknight)
41 The Lord Is My Light - Psalm 27
(Haas)
36 The Lord Is My Shepherd - Psalm 23
692 The Lord Is Near
730 The Lord Will Heal the Broken Heart
792 The Love of the Lord
964 The Master Came to Bring Good News
80 The Name of God - Psalm 116
823 The Peace of God
820 The Peace of the Earth / La Paz de la
Tierra
444 The People Who Walked in Darkness
564 The Play of the Godhead
738 The Reign of God
751 The Servant Song
525 The Strife Is O'er
790 The Summons
815 The Thirsty Cry for Water, Lord
864 The Trumpet in the Morning
454 The Virgin Mary Had a Baby Boy
867 There Are Many Rooms
640 There Is a Balm in Gilead
653 There Is a Longing
794 There is a mountain
979 There Is a Place
701 There is no greater love
905 There Is One Lord
453 There's a star in the east
979 There's a time for remembering
644 There's a Wideness in God's Mercy
650 These Alone Are Enough
28 They Who Do Justice - Psalm 15
835 They'll Know We Are Christians
856 This Day God Gives Me
522 This Is a Day of New Beginnings
503 This Is My Example
986 This Is My Song
951 This Is the Body of Christ
82 This Is the Day - Psalm 118
520 This Is the Feast of Victory
591 This Little Light of Mine
939 Those who were in the dark
689 Though the Mountains May Fall
776 Thuma Mina / Send Me, Jesus
700 Tình Chúa Cao Vòi / Boundless Love
748 'Tis the Gift to Be Simple
773 To bring glad tidings to the lowly
573 To Jesus Christ, Our Sovereign King
605 To you, O God
39 To You, O Lord - Psalm 25 (Haugen)
40 To You, O Lord - Psalm 25 (Pishner)
68 Today Is Born Our Savior - Psalm 96
(Hughes)
69 Today Is Born Our Savior - Psalm 96
(Krisman)
805 Touch the Earth Lightly
878 Transform Us
475 Tree of Life
32 Tú tienes, Señor
469 Turn away from sin
660 Turn My Heart, O God
485 Turn to the Living God
798 Two Fishermen
696 Ubi Cáritas (Hurd)
500 Ubi Cáritas (Taizé)
705 Ubi Cáritas / Where True Love and
Charity Are Found (Chant)
783 Unless a Grain of Wheat
849 Uyai Mose / Come All You People
838 Ven al Banquete / Come to the Feast
558 Veni Creátor Spíritus
550 Veni Sancte Spíritus
439 Venid, Fieles Todos / O Come, All Ye
Faithful / Adéste Fidéles
478 Volvamos Hoy a Nuestro Dios / Return
to God
898 Wade in the Water
406 Wait for the Lord
417 Warm the Time of Winter
860 Watch, O Lord
807 We Are Called
778 We are called, we are chosen
71 We Are God's People - Psalm 100
834 We Are Many Parts / Muchos
Miembros Hay
594 We Are Marching / Siyahamba
913 We Are One (de Silva)
548 We Are One (Wright)
835 We are one in the Spirit
923 We are the body of Christ (Haas)
741 We Are the Body of Christ / Somos el
Cuerpo de Cristo (Cortez)
592 We Are the Light of the World
407 We are your people of the night
854 We Arise
670 We Await with Wakeful Care
657 We Cannot Measure How You Heal
811 We cannot own the sunlit sky
924 We come to share our story
938 We Come to Your Feast
808 We Come with Joy
638 We Gather Together
631 We Give You Thanks
987 We Have a Dream
784 We Have Been Told
785 We hold the death of the Lord
37 We Long to See Your Face - Psalm 24
938 We place upon your table
617 We Praise You (Dameans)
608 We Praise You (Haas)
681 We Remember
508 We remember one who loved us well
962 We rise again from ashes
817 We Shall Overcome
871 We Shall Rise Again
501 We should glory in the cross
463 We Three Kings of Orient Are
680 We Walk by Faith
517 We Walk His Way / Ewe, Thina
753 We Will Serve the Lord
737 We Will Walk with God
753 Wealth can be an idol
791 Were I the Perfect Child of God
511 Were You There
466 What Child Is This
461 What Star Is This
642 What Wondrous Love Is This
816 What You Have Done for Me
747 Whatever Be the Love
450 When a star is shining
722 When I'm feeling all alone
612 When in Our Music God Is Glorified
768 When Jesus worked here on earth
467 When John Baptized by Jordan's River
966 When Love Is Found
404 When the King Shall Come Again
417 When the wind of winter blows
496 When they heard that Jesus was
coming
936 When two or more gather
756 When We Are Living / Pues Si
Vivimos
706 Where Charity and Love Prevail
450 Where the Promise Shines
705 Where True Love and Charity Are
Found / Ubi Cáritas
907 Where Two or Three Are Gathered
749 Where Your Treasure Is
968 Wherever You Go
904 Wherever you go, I will follow
900 Who Calls You by Name
456 Who is the baby
671 Why Stand So Far Away
790 Will you come and follow me
751 Will you let me be your servant
583 Wisdom, My Road
725 With a Shepherd's Care
762 With hands of justice and faith
97 With Joy You Shall Draw Water -
Isaiah 12
87 With the Lord There Is Mercy - Psalm 130
933 With This Bread
722 With You by My Side
739 Within the Reign of God
922 Without Seeing You
436 Wood of the Cradle
32 Words of Everlasting Life - Psalm 19
827 World Peace Prayer
882 Ye Watchers and Ye Holy Ones
945 Yo Soy el Pan de Vida / I Am the
Bread of Life
734 You are salt for the earth
726 You Are All I Want
586 You Are All We Have
774 You Are Called to Tell the Story
721 You Are Mine / Contigo Estoy
695 You Are Near
799 You Are Strong, You Are Holy
609 You Are the Voice
773 You Have Anointed Me
897 You Have Been Enlightened
940 You Satisfy the Hungry Heart
683 You shall cross the barren desert
797 You Walk along Our Shoreline
691 You who dwell in the shelter of the
Lord
98 You Will Draw Water Joyfully /
Sacarán Aguas con Alegría - Isaiah12
30 You Will Show Me the Path of Life -
Psalm 16
628 You, Lord, Are Both Lamb and
Shepherd
58 Your Love Is Finer Than Life - Psalm 63
"""

    # Dictionary to fill
    hymns = {}

    # Keep track of number and name of the song being processed
    # Used to re-assemble song names that spill onto multiple lines
    current_number = None
    current_title_parts = []

    # Split the index text by line
    lines = text.split('\n')

    # Loop through each line in the index
    for line in lines:
        # Remove leading or trailing white space
        line = line.strip()
        
        # Ignore empty lines
        if not line:
            continue
        
        # Check if line starts with a number
        match = re.match(r'^(\d+)\s+(.+)$', line)
        
        # If the line does start with a number:
        if match:
            # If we've hit a new number and there are still items in
            # current_title_parts, then we've hit a new entry and the previous
            # entry needs to saved. Save previous entry if exists
            if current_number is not None and current_title_parts:
                # Assemble the song name
                title = ' '.join(current_title_parts)
                # Match it with the previous number
                hymns[title] = current_number
            
            # Otherwise, start new entry
            # Hold the current number
            current_number = int(match.group(1))
            # Store the text that follows (need to wait until the next line to
            # ensure it does not contain a continuation of this line)
            current_title_parts = [match.group(2)]
        # If the line does not start with a number, then it belongs to the
        # previous line
        else:
            # Continuation of previous title
            if current_number is not None:
                current_title_parts.append(line)

    # Don't forget the last entry
    if current_number is not None and current_title_parts:
        title = ' '.join(current_title_parts)
        hymns[title] = current_number

    return hymns

def save_hymns_as_package(hymns_dict, output_path='hymns_data.py'):
    """Save hymns dictionary as Python package file in original order."""
    with open(output_path, 'w', encoding='utf-8') as f:
        # Header
        f.write('"""Hymnal Index Data - Gather"""\n\n')
        
        f.write('# Dictionary of hymn titles to numbers\n')
        f.write('# Entries are in the same order as the original hymnal index\n\n')
        
        # Write dictionary
        f.write('hymns = {\n')
        
        for title, number in hymns_dict.items():
            # Escape quotes in titles
            title_escaped = title.replace('"', '\\"')
            f.write(f'    "{title_escaped}": {number},\n')
        
        f.write('}\n\n')
        
        # Add helper function to get hymn number from name
        f.write('\ndef get_hymn_number(title):\n')
        f.write('    """Get hymn number by exact title match."""\n')
        f.write('    return hymns.get(title)\n\n\n')
        
        # Helper function to get hymn number by partial name match
        f.write('def search_hymns(search_term, case_sensitive=False):\n')
        f.write('    """Search for hymns by partial title match.\n')
        f.write('    \n')
        f.write('    Args:\n')
        f.write('        search_term: Text to search for in hymn titles\n')
        f.write('        case_sensitive: Whether search should be case-sensitive\n')
        f.write('    \n')
        f.write('    Returns:\n')
        f.write('        dict: Dictionary of matching hymn titles and numbers\n')
        f.write('    """\n')
        f.write('    if case_sensitive:\n')
        f.write('        return {title: num for title, num in hymns.items()\n')
        f.write('                if search_term in title}\n')
        f.write('    else:\n')
        f.write('        search_lower = search_term.lower()\n')
        f.write('        return {title: num for title, num in hymns.items()\n')
        f.write('                if search_lower in title.lower()}\n\n\n')
        
        # Helper function to get all hymns in the dictionary
        f.write('def get_all_hymns():\n')
        f.write('    """Get complete dictionary of all hymns."""\n')
        f.write('    return hymns.copy()\n\n\n')
        
        # Helper function to count entries
        f.write('def count_hymns():\n')
        f.write('    """Get total number of hymns in index."""\n')
        f.write('    return len(hymns)\n\n\n')
        
        f.write('# Export main symbols\n')
        f.write('__all__ = ["hymns", "get_hymn_number", "search_hymns", "get_all_hymns", "count_hymns"]\n')

if __name__ == '__main__':
    print("Parsing hymnal index...")
    # Parse the text
    hymns = parse_hymnal_complete()

    # Print status
    print(f"✓ Parsed {len(hymns)} hymns")

    # Show first and last 5 entries
    print("\nFirst 5 entries:")
    for i, (title, number) in enumerate(list(hymns.items())[:5], 1):
        print(f"  {i}. {number}: {title}")

    print("\nLast 5 entries:")
    total = len(hymns)
    for i, (title, number) in enumerate(list(hymns.items())[-5:], start=total-4):
        print(f"  {i}. {number}: {title}")

    # Save to file
    output_path = 'gather.py'
    save_hymns_as_package(hymns, output_path)
    print(f"\n✓ Saved to {output_path} (in original order)")

    # Test a few lookups
    print("\nTest lookups:")
    test_titles = [
        "A Celtic Rune",
        "Amazing Grace",
        "O Come, All Ye Faithful / Venid, Fieles Todos / Adéste Fidéles"
    ]

    for title in test_titles:
        number = hymns.get(title)
        if number:
            print(f"  ✓ '{title}': {number}")
        else:
            print(f"  ✗ '{title}': Not found")
