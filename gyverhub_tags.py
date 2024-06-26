from enum import Enum, auto

# Tags are here https://github.com/GyverLibs/GyverHub/blob/00e1343ae12d9e5446e8418856ddb2fbc898f176/src/core/tags.h#L8


class GHTag (Enum):
    api_v = 0
    id = auto()
    client = auto()
    type = auto()
    update = auto()
    updates = auto()
    get = auto()
    last = auto()
    crc32 = auto()
    discover = auto()
    name = auto()
    prefix = auto()
    icon = auto()
    PIN = auto()
    version = auto()
    max_upl = auto()
    http_t = auto()
    ota_t = auto()
    ws_port = auto()
    modules = auto()
    total = auto()
    used = auto()
    code = auto()
    OK = auto()
    ack = auto()
    info = auto()
    controls = auto()
    ui = auto()
    files = auto()
    notice = auto()
    alert = auto()
    push = auto()
    script = auto()
    refresh = auto()
    print = auto()

    error = auto()
    fs_err = auto()
    ota_next = auto()
    ota_done = auto()
    ota_err = auto()
    fetch_start = auto()
    fetch_chunk = auto()
    fetch_err = auto()
    upload_next = auto()
    upload_done = auto()
    upload_err = auto()
    ota_url_err = auto()
    ota_url_ok = auto()

    value = auto()
    maxlen = auto()
    rows = auto()
    regex = auto()
    align = auto()
    min = auto()
    max = auto()
    step = auto()
    dec = auto()
    unit = auto()
    fsize = auto()
    action = auto()
    nolabel = auto()
    suffix = auto()
    notab = auto()
    square = auto()
    disable = auto()
    hint = auto()
    len = auto()
    wwidth = auto()
    wheight = auto()
    data = auto()
    func = auto()
    keep = auto()
    exp = auto()

    plugin = auto()
    js = auto()
    css = auto()
    ui_file = auto()
    stream = auto()
    port = auto()
    canvas = auto()
    width = auto()
    height = auto()
    active = auto()
    html = auto()
    dummy = auto()
    menu = auto()
    gauge = auto()
    gauge_r = auto()
    gauge_l = auto()
    led = auto()
    log = auto()
    table = auto()
    image = auto()
    text = auto()
    display = auto()
    text_f = auto()
    label = auto()
    title = auto()
    dpad = auto()
    joy = auto()
    flags = auto()
    tabs = auto()
    switch_t = auto()
    switch_i = auto()
    button = auto()
    color = auto()
    select = auto()
    spinner = auto()
    slider = auto()
    datetime = auto()
    date = auto()
    time = auto()
    confirm = auto()
    prompt = auto()
    area = auto()
    pass_ = auto()
    input = auto()
    hook = auto()
    row = auto()
    col = auto()
    space = auto()
    platform = auto()

if __name__ == "__main__":
    for t in GHTag:
        print(f"{t.value:x} {t}")