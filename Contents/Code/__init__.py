################################################################################
#import anime_menu
import cherrytorrent_launcher
import movies_menu
import tvshows_menu

import tracking

################################################################################
TITLE  = 'BitTorrent'
ART    = 'art-default.jpg'
ICON   = 'icon-default.png'

################################################################################
def Start():
    DirectoryObject.thumb  = R(ICON)
    ObjectContainer.art    = R(ART)
    ObjectContainer.title1 = TITLE
    VideoClipObject.art    = R(ART)
    VideoClipObject.thumb  = R(ICON)

    Log.Info('============================================')
    Log.Info('Server:')
    Log.Info(' - OS:        {0}'.format(Platform.OS))
    Log.Info(' - CPU:       {0}'.format(Platform.CPU))
    Log.Info(' - Local IP:  {0}'.format(SharedCodeService.utils.get_local_host()))
    Log.Info(' - Public IP: {0}'.format(Network.PublicAddress))
    Log.Info('--------------------------------------------')
    Log.Info('Channel:')
    Log.Info(' - Version: {0}'.format(SharedCodeService.common.VERSION))
    Log.Info('--------------------------------------------')
    Log.Info('Preferences:')
    Log.Info(' - Cascade server URL:      {0}'.format(Prefs['CASCADE_URL']))
    Log.Info(' - Torrent incoming port:   {0}'.format(Prefs['INCOMING_PORT']))
    Log.Info(' - UPnP / NAT-PMP enabled:  {0}'.format(Prefs['UPNP_NATPMP_ENABLED']))
    Log.Info(' - Maximum download rate:   {0}'.format(Prefs['MAX_DOWNLOAD_RATE']))
    Log.Info(' - Maximum upload rate:     {0}'.format(Prefs['MAX_UPLOAD_RATE']))
    Log.Info(' - Keep files:              {0}'.format(Prefs['KEEP_FILES']))
    Log.Info(' - Anime enabled:           {0}'.format(Prefs['ANIME_ENABLED']))
    Log.Info(' - Anime download dir:      {0}'.format(Prefs['ANIME_DOWNLOAD_DIR']))
    Log.Info(' - Movies enabled:          {0}'.format(Prefs['MOVIES_ENABLED']))
    Log.Info(' - Movies download dir:     {0}'.format(Prefs['MOVIES_DOWNLOAD_DIR']))
    Log.Info(' - TV shows enabled:        {0}'.format(Prefs['TVSHOWS_ENABLED']))
    Log.Info(' - TV shows download dir:   {0}'.format(Prefs['TVSHOWS_DOWNLOAD_DIR']))
    Log.Info(' - VPN Fix enabled:         {0}'.format(Prefs['VPN_FIX']))
    Log.Info(' - Metadata timeout:        {0}'.format(Prefs['METADATA_TIMEOUT']))
    Log.Info(' - Torrent Proxy type:      {0}'.format(Prefs['TORRENT_PROXY_TYPE']))
    Log.Info(' - Torrent Proxy host:      {0}'.format(Prefs['TORRENT_PROXY_HOST']))
    Log.Info(' - Torrent Proxy port:      {0}'.format(Prefs['TORRENT_PROXY_PORT']))
    Log.Info('============================================')
    
    tracking.people_set()
    cherrytorrent_launcher.start_cherrytorrent()

################################################################################
@handler(SharedCodeService.common.PREFIX, TITLE, thumb=ICON, art=ART)
def Main():
    Log.Info('============================================')
    Log.Info('Client:')
    Log.Info(' - Product:  {0}'.format(Client.Product))
    Log.Info(' - Platform: {0}'.format(Client.Platform))
    Log.Info('============================================')

    object_container = ObjectContainer(title2=TITLE)
    
    #if Prefs['ANIME_ENABLED']:
    #    object_container.add(DirectoryObject(key=Callback(anime_menu.menu), title='Anime', summary='Browse anime'))
    
    if Prefs['MOVIES_ENABLED']:
        object_container.add(DirectoryObject(key=Callback(movies_menu.menu), title='Movies', summary='Browse movies'))
    
    if Prefs['TVSHOWS_ENABLED']:
        object_container.add(DirectoryObject(key=Callback(tvshows_menu.menu), title='TV Shows', summary="Browse TV shows"))
    
    object_container.add(PrefsObject(title='Preferences', summary='Preferences for BitTorrent channel'))
    object_container.add(DirectoryObject(key=Callback(about_menu, title='About'), title='About', summary='About BitTorrent channel', thumb=R('about.png')))
    return object_container

################################################################################
@route(SharedCodeService.common.PREFIX + '/about')
def about_menu(title):
    object_container = ObjectContainer(title2=title)

    # Channel Version
    object_container.add(DirectoryObject(key=Callback(empty_menu), title='Channel version: {0}'.format(SharedCodeService.common.VERSION), summary='Current version of the BitTorrent channel.'))
    
    # Cascade server
    cascade_server_result  = 'Available'
    cascade_server_summary = Prefs['CASCADE_URL'] + ' is available.'
    try:
        HTML.ElementFromURL(Prefs['CASCADE_URL'], timeout=5.0)
    except:
        cascade_server_result  = 'Unavailable'
        cascade_server_summary = Prefs['CASCADE_URL'] + ' is unavailable, check URL the in Preferences.'
    object_container.add(DirectoryObject(key=Callback(empty_menu), title='Cascade server: {0}'.format(cascade_server_result), summary=cascade_server_summary))

    # CherryTorrent
    cherrytorrent_result  = 'Running'
    cherrytorrent_summary = 'CherryTorrent is running correctly.'
    if not SharedCodeService.cherrytorrent.is_running():
        cherrytorrent_result  = 'ERROR'
        cherrytorrent_summary = 'CherryTorrent is not running.'
    object_container.add(DirectoryObject(key=Callback(empty_menu), title='CherryTorrent: {0}'.format(cherrytorrent_result), summary=cherrytorrent_summary))

    # Local IP
    local_ip = SharedCodeService.utils.get_local_host()
    if local_ip:
        local_ip_result  = local_ip
        local_ip_summary = 'Local IP is properly determined.'
    else:
        local_ip_result  = 'ERROR'
        local_ip_summary = 'Unable to determine local IP'
    object_container.add(DirectoryObject(key=Callback(empty_menu), title='Local IP: {0}'.format(local_ip_result), summary=local_ip_summary))

    # Public IP
    public_ip = Network.PublicAddress
    if public_ip:
        public_ip_result  = public_ip
        public_ip_summary = 'Public IP is properly determined.'
    else:
        public_ip_result  = 'ERROR'
        public_ip_summary = 'Unable to determine public IP'
    object_container.add(DirectoryObject(key=Callback(empty_menu), title='Public IP: {0}'.format(public_ip_result), summary=public_ip_summary))
    
    # Torrent Proxy
    if Prefs['TORRENT_PROXY_TYPE'] == 'None':
        torrent_proxy_result  = 'Unused'
        torrent_proxy_summary = 'No torrent proxy set.'
    else:
        torrent_proxy_result  = '{0}:{1}'.format(Prefs['TORRENT_PROXY_HOST'], Prefs['TORRENT_PROXY_PORT'])
        torrent_proxy_summary = 'Torrent proxy is working properly.'

        try:
            SharedCodeService.utils.try_connection()
        except Exception as exception:
            torrent_proxy_result  = 'ERROR'
            torrent_proxy_summary = 'Torrent proxy is not working properly: {0}'.format(exception)
            Log.Error(torrent_proxy_summary)
    object_container.add(DirectoryObject(key=Callback(empty_menu), title='Torrent Proxy: {0}'.format(torrent_proxy_result), summary=torrent_proxy_summary))

    return object_container

################################################################################
@route(SharedCodeService.common.PREFIX + '/empty')
def empty_menu():
    object_container = ObjectContainer(title2='Empty')
    return object_container
