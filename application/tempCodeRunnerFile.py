    albums = Album.objects.filter(page_email = page).order_by('name')

    # self_follow = ProfileFollowsProfile.objects.filter(followed_profile_email = email).order_by('follower_profile_email')

    MAIN = Path(Path(__file__).resolve().parent.parent,'media',str(email))
    PROFILE_PICTURES =  Path(Path(__file__).resolve().parent.parent,'media',str(email),str(email))


    if not MAIN.exists():

        os.mkdir(MAIN)


    if not PROFILE_PICTURES.exists():

        profile_pics = Album.objects.create(page_email=page,name="Profile Pictures",num_photos=0)

        os.mkdir(PROFILE_PICTURES)