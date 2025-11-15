class URL:
    host = "p-on.ru"
    base_url = "https://" + host
    login = "/api/users/login"
    devices = "/api/devices"
    update = "/api/updates?ts="
    command = "/api/devices/command"
    profile = "/api/users/profile"
    alive = "/api/iamalive" #{"status":"you are alive"}
