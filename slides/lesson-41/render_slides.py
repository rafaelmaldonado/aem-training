"""Render illustrated Session 41 PNGs in the technical-atlas style of Session 37."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "origin_image"
OUT.mkdir(exist_ok=True)
W, H = 1672, 941
PAPER = (252, 249, 245)
GRID = (246, 241, 235)
NAVY = "#05104e"
BLUE = "#1135f5"
PURPLE = "#7b079a"
ORANGE = "#f04b12"
GREEN = "#06551d"
SOFT = "#ffffff"
HEAD = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
BODY = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"


def font(size, head=False):
    return ImageFont.truetype(HEAD if head else BODY, size)


def background():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 29):
        d.line((x, 0, x, H), fill=GRID, width=1)
    for y in range(0, H, 29):
        d.line((0, y, W, y), fill=GRID, width=1)
    return im, d


def title(number, section, heading, sub=None):
    im, d = background()
    d.text((44, 22), f"{number:02d} · {section.upper()}", font=font(38, True), fill=NAVY)
    d.text((44, 77), heading, font=font(82, True), fill=NAVY)
    if sub:
        d.text((47, 155), sub, font=font(34), fill=NAVY)
    d.line((44, 206 if sub else 184, W - 48, 206 if sub else 184), fill=BLUE, width=3)
    return im, d


def save(im, n):
    im.save(OUT / f"slide_{n:02d}.png")


def arrow(d, x1, y, x2, color=BLUE):
    d.line((x1, y, x2, y), fill=color, width=5)
    d.polygon([(x2, y), (x2-18, y-12), (x2-18, y+12)], fill=color)


MONO = "/System/Library/Fonts/Supplemental/Courier New.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
PALE = "#eef3ff"
PALE_GREEN = "#edf8f1"
PALE_ORANGE = "#fff1eb"
PALE_PURPLE = "#f5effb"
MUTED = "#62708c"


def t(d, x, y, value, size=27, color=NAVY, face=BODY):
    d.text((x, y), value, font=ImageFont.truetype(face, size), fill=color)


def pane(d, xy, heading, crumb, color=BLUE):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=12, fill=SOFT, outline=color, width=3)
    fill = PALE_PURPLE if color == PURPLE else PALE_GREEN if color == GREEN else PALE
    d.rounded_rectangle((x1+2,y1+2,x2-2,y1+57),radius=10,fill=fill)
    d.rectangle((x1+2,y1+40,x2-2,y1+57),fill=fill)
    d.line((x1,y1+57,x2,y1+57),fill=color,width=3)
    d.ellipse((x1+18,y1+22,x1+31,y1+35),fill=color)
    d.ellipse((x1+42,y1+22,x1+55,y1+35),outline=color,width=2)
    t(d,x1+73,y1+12,heading,32,NAVY,HEAD)
    t(d,x1+19,y1+69,crumb,20,MUTED)


def box(d,xy,color=BLUE,fill=SOFT):
    d.rounded_rectangle(xy,radius=8,fill=fill,outline=color,width=2)


def pill(d,x,y,label,color=BLUE,fill=PALE):
    w=max(110,len(label)*15+25)
    box(d,(x,y,x+w,y+44),color,fill)
    t(d,x+12,y+8,label,23,color,BOLD)


def takeaway(d,message,color=BLUE,fill=PALE):
    box(d,(48,817,1624,904),color,fill)
    d.ellipse((69,838,110,879),outline=color,width=3)
    t(d,82,839,"i",31,color,BOLD)
    t(d,132,839,message,39,color,HEAD)


def mark(d,x,y,kind,color=BLUE):
    if kind == "doc":
        d.rounded_rectangle((x,y,x+53,y+67),radius=5,outline=color,width=4)
        for yy in (y+22,y+35,y+48):d.line((x+11,yy,x+42,yy),fill=color,width=3)
    elif kind == "queue":
        for i in range(3):
            d.rounded_rectangle((x,y+i*21,x+63,y+16+i*21),radius=4,outline=color,width=3)
            d.ellipse((x+9,y+5+i*21,x+17,y+13+i*21),fill=color)
    elif kind == "gear":
        d.ellipse((x+5,y+5,x+59,y+59),outline=color,width=4)
        d.ellipse((x+23,y+23,x+41,y+41),outline=color,width=4)
        for xx,yy in ((32,0),(32,65),(0,32),(65,32)):
            d.line((x+32,y+32,x+xx,y+yy),fill=color,width=4)
    elif kind == "db":
        d.ellipse((x,y+2,x+64,y+24),outline=color,width=3)
        d.line((x,y+13,x,y+59),fill=color,width=3)
        d.line((x+64,y+13,x+64,y+59),fill=color,width=3)
        d.arc((x,y+48,x+64,y+71),0,180,fill=color,width=3)
    elif kind == "check":
        d.ellipse((x,y,x+64,y+64),outline=color,width=4)
        d.line((x+15,y+32,x+28,y+46,x+51,y+17),fill=color,width=5)


# Cover: Session 37's title scale and illustrated vertical agenda.
im,d=background()
t(d,48,24,"Class 41 · Week 9 · Monday, October 12, 2026",36,NAVY,BOLD)
d.line((48,91,923,91),fill=BLUE,width=4)
t(d,56,188,"Make asynchronous",119,NAVY,HEAD)
t(d,56,314,"work retryable",119,NAVY,HEAD)
t(d,61,488,"Retries · idempotency · resumable work",43,BLUE,BOLD)
d.line((56,622,920,622),fill=BLUE,width=3)
mark(d,68,665,"queue",BLUE);t(d,155,672,"30-minute technical session",40,BLUE,HEAD)
mark(d,68,755,"doc",NAVY);t(d,155,760,"Juan Maldonado",39,NAVY,HEAD)
for i,(kind,title_,detail,color) in enumerate((("gear","1. Trigger","Launcher + workflow",GREEN),("queue","2. Process","Sling Job + retry",PURPLE),("db","3. Protect","State + checkpoint",BLUE))):
    y=179+i*218
    d.ellipse((1075,y,1180,y+105),fill=SOFT,outline=color,width=4)
    mark(d,1096,y+20,kind,color)
    t(d,1210,y+7,title_,49,NAVY,HEAD)
    t(d,1210,y+65,detail,27,color,BOLD)
    if i<2:d.line((1128,y+107,1128,y+218),fill=color,width=3)
save(im,1)

# Three responsibilities: launcher form, workflow canvas and queued job.
im,d=title(2,"Three responsibilities","Launcher, workflow and Sling Job","An event becomes an instance, then queued work.")
for x,label,kind,color in ((65,"EVENT","doc",GREEN),(615,"MODEL","gear",PURPLE),(1165,"QUEUE","queue",BLUE)):
    mark(d,x,242,kind,color);t(d,x+83,253,label,37,color,HEAD)
arrow(d,535,276,598);arrow(d,1085,276,1148)
pane(d,(51,333,543,772),"Workflow Launcher","Tools / Workflow / Launchers",GREEN)
for y,k,v in ((450,"Event","Modified"),(516,"Path","/content/.../control"),(582,"Condition","requestedVersion==v1")):
    t(d,73,y,k,24,MUTED,BOLD);t(d,218,y,v,22,NAVY,MONO)
pill(d,74,684,"Enabled",GREEN,PALE_GREEN)
pane(d,(594,333,1093,772),"Workflow Model","Start / Process Step / End",PURPLE)
for x,label,color in ((618,"START",GREEN),(758,"PROCESS",PURPLE),(934,"END",BLUE)):
    box(d,(x,492,x+118,582),color);t(d,x+13,523,label,30,color,HEAD)
arrow(d,737,537,754,PURPLE);arrow(d,878,537,930,PURPLE)
t(d,625,662,"Process Step queues the job",26,NAVY,BOLD)
pane(d,(1144,333,1621,772),"Sling Job","topic: training/session41/guides")
t(d,1165,451,"version",24,MUTED,BOLD);t(d,1325,451,"v1",27,NAVY,MONO)
t(d,1165,519,"consumer",24,MUTED,BOLD);t(d,1325,519,"GuideBatchJobConsumer",21,NAVY,MONO)
pill(d,1166,633,"RETRYABLE",BLUE,PALE)
takeaway(d,"Workflow End confirms dispatch; inspect the job for the effect.")
save(im,2)

# At-least-once: illustrative error.log beside the effect/ack timeline.
im,d=title(3,"At least once","A job may arrive again","Content and job completion are separate commits.")
pane(d,(51,258,868,780),"error.log · illustrative","crx-quickstart/logs/error.log")
box(d,(70,362,847,745),NAVY,NAVY)
for i,(line,color) in enumerate((("[INFO] job=J41 version=v1 started",SOFT),("[INFO] job=J41 applied=guide-a count=1","#a7f3ba"),("[WARN] job=J41 deliberate failure","#ffb79f"),("[INFO] job=J41 retry=1 started",SOFT),("[INFO] job=J41 skip=guide-a","#b9c8ff"))):
    t(d,89,389+i*65,line,26,color,MONO)
pane(d,(894,258,1621,780),"Delivery timeline","effect saved / acknowledgement pending",PURPLE)
d.line((974,386,974,688),fill=PURPLE,width=3)
for i,(head,detail,color) in enumerate((("Receive","Consumer reads job",BLUE),("Commit","Effect becomes durable",GREEN),("Gap","Job ACK is not saved",ORANGE),("Retry","Consumer reads state again",PURPLE))):
    y=376+i*94;d.ellipse((950,y,998,y+48),fill=SOFT,outline=color,width=4)
    t(d,963,y+6,str(i+1),30,color,HEAD);t(d,1020,y-4,head,37,color,HEAD);t(d,1020,y+42,detail,24,NAVY)
takeaway(d,"At least once requires replay-safe business effects.",ORANGE,PALE_ORANGE)
save(im,3)

# Idempotency: different delivery IDs, same business key and persisted target.
im,d=title(4,"Idempotency","Recognize the same operation","The business key stays stable even when the job ID changes.")
pane(d,(51,263,784,768),"Job deliveries","Properties / topic / version",PURPLE)
for y,jid,result,color,fill in ((389,"job-802","APPLY",GREEN,PALE_GREEN),(508,"job-827","SKIP",PURPLE,PALE_PURPLE)):
    box(d,(77,y,759,y+94),color);mark(d,95,y+14,"queue",color)
    t(d,180,y+12,jid,28,NAVY,MONO);t(d,180,y+52,"guide-a · version=v1",25,MUTED,MONO)
    pill(d,613,y+27,result,color,fill)
t(d,85,684,"Business key = target + version",28,PURPLE,BOLD)
pane(d,(807,263,1621,768),"CRXDE Lite · properties","/content/session-41-demo/guides/guide-a")
for y,key,val in ((394,"processedVersion","v1"),(485,"applyCount","1")):
    t(d,846,y,key,28,NAVY,MONO);t(d,1394,y,val,30,GREEN,MONO)
    d.line((839,y+70,1587,y+70),fill="#d8e1f0",width=2)
box(d,(841,602,1585,708),GREEN,PALE_GREEN);mark(d,860,624,"check",GREEN)
t(d,952,606,"Already at v1?",36,GREEN,HEAD)
t(d,952,655,"Return OK; do not increment again.",26,NAVY)
takeaway(d,"Read state first; save the effect and its marker together.")
save(im,4)

# Outcome table plus queue configuration values.
im,d=title(5,"Job outcomes","Return a deliberate job result","The consumer chooses a result; the queue controls retries.")
pane(d,(51,263,1000,773),"JobConsumer outcomes · illustrative","process(Job job) → JobResult")
for x,h in ((82,"OBSERVED"),(412,"DECISION"),(798,"RESULT")):t(d,x,365,h,26,MUTED,BOLD)
d.line((78,411,974,411),fill=BLUE,width=3)
for i,(state,decision,result,color,fill) in enumerate((("Complete","Confirm or skip replay","OK",GREEN,PALE_GREEN),("Transient","Request another attempt","FAILED",ORANGE,PALE_ORANGE),("Permanent","Bad input or fixture","CANCEL",PURPLE,PALE_PURPLE))):
    y=438+i*93;box(d,(76,y,972,y+77),color,fill)
    t(d,93,y+23,state,26,NAVY,BOLD);t(d,424,y+23,decision,24,NAVY);t(d,814,y+20,result,30,color,HEAD)
pane(d,(1026,263,1621,773),"Queue configuration","config.author / QueueConfiguration",PURPLE)
box(d,(1046,359,1600,663),NAVY,NAVY)
for i,(line,color) in enumerate((("queue.topics = training/session41/guides",SOFT),("queue.type = ORDERED","#cfb8ff"),("queue.retries = 2","#a7f3ba"),("queue.retrydelay = 10000","#a7f3ba"))):
    t(d,1062,388+i*60,line,22,color,MONO)
t(d,1051,697,"10,000 ms = 10 seconds",25,PURPLE,BOLD)
takeaway(d,"FAILED retries only within the configured queue policy.",ORANGE,PALE_ORANGE)
save(im,5)

# Batching: repository tree and resume decisions.
im,d=title(6,"Resume work","Checkpoint after a small batch","Persist progress; recheck the interrupted item on retry.")
pane(d,(51,262,738,772),"Repository browser · illustrative","/content/session-41-demo/guides")
for y,name,state,color in ((393,"guide-a","processedVersion = v1",GREEN),(506,"guide-b","processedVersion = —",ORANGE),(619,"guide-c","not started",MUTED)):
    d.line((113,y-25,113,y+48),fill=BLUE,width=3);d.line((113,y+15,156,y+15),fill=BLUE,width=3)
    mark(d,168,y-13,"doc",color);t(d,254,y-16,name,36,NAVY,HEAD);t(d,254,y+30,state,24,color,MONO)
pane(d,(765,262,1621,772),"Resume decision","after retry or restart",PURPLE)
for i,(n,head,detail,color) in enumerate((("A","Checkpoint found","Skip the committed effect",GREEN),("B","State uncertain","Read again; apply if needed",ORANGE),("C","No checkpoint","Continue after B",BLUE))):
    y=376+i*122;d.ellipse((798,y,859,y+61),fill=SOFT,outline=color,width=3)
    t(d,815,y+9,n,36,color,HEAD);t(d,890,y-3,head,37,color,HEAD);t(d,890,y+45,detail,26,NAVY)
    if i<2:d.line((829,y+62,829,y+121),fill=color,width=3)
takeaway(d,"Each item needs a replay check at its checkpoint boundary.")
save(im,6)

# Demo: sequence in a log and final CRXDE properties.
im,d=title(7,"Local Author demo","Two Guides, three deliveries","Change requestedVersion to v1; follow the workflow and the job.")
for x,n,label,color in ((70,"1","Launch",GREEN),(434,"2","Retry",ORANGE),(798,"3","Replay",PURPLE)):
    d.ellipse((x,239,x+57,296),fill=SOFT,outline=color,width=3);t(d,x+18,247,n,34,color,HEAD)
    t(d,x+74,249,label,36,color,HEAD)
    if n!="3":arrow(d,x+240,266,x+347,color)
pane(d,(51,326,988,774),"error.log · condensed sequence","Filter: Session 41 · replay is a new job")
box(d,(72,424,967,742),NAVY,NAVY)
for i,(line,color) in enumerate((("queued job=J41 version=v1",SOFT),("applied=guide-a version=v1 count=1","#a7f3ba"),("deliberate failure after first batch","#ffb79f"),("skip=guide-a already at v1","#cfb8ff"),("applied=guide-b version=v1 count=1","#a7f3ba"),("replay J42: skip guide-a; skip guide-b","#cfb8ff"))):
    t(d,92,440+i*49,line,25,color,MONO)
pane(d,(1010,326,1621,774),"CRXDE Lite · final state","/content/session-41-demo/guides",GREEN)
for y,name in ((453,"guide-a"),(590,"guide-b")):
    mark(d,1039,y,"doc",GREEN);t(d,1122,y-6,name,38,NAVY,HEAD)
    t(d,1122,y+50,"processedVersion  v1",22,NAVY,MONO)
    t(d,1122,y+81,"applyCount        1",22,GREEN,MONO)
takeaway(d,"After replay, both Guides still have applyCount = 1.")
save(im,7)

# Loop prevention: launcher form, repository paths, and instance check.
im,d=title(8,"Loop prevention","Can the job trigger its own launcher?","Narrow the rule and check the workflow instance count.")
pane(d,(51,261,785,774),"Launcher rule · illustrative","Tools / Workflow / Launchers",PURPLE)
for y,key,val in ((381,"Event Type","Modified"),(452,"Nodetype","nt:unstructured"),(523,"Path","/content/.../control"),(594,"Condition","requestedVersion==v1")):
    t(d,76,y,key,25,MUTED,BOLD);box(d,(266,y-7,751,y+49),PURPLE)
    t(d,280,y+6,val,23,NAVY,MONO)
pane(d,(812,261,1621,774),"What the job changes","Repository paths and workflow instances",GREEN)
t(d,846,384,"TRIGGER",30,PURPLE,HEAD);t(d,1105,385,"/control",29,NAVY,MONO)
d.line((844,438,1582,438),fill="#d8e1f0",width=2)
t(d,846,465,"WRITE",30,GREEN,HEAD);t(d,1105,465,"/guides/guide-a",27,NAVY,MONO)
t(d,1105,511,"/guides/guide-b",27,NAVY,MONO)
box(d,(846,588,1584,716),GREEN,PALE_GREEN);mark(d,864,619,"check",GREEN)
t(d,955,598,"Workflow instances",36,GREEN,HEAD)
t(d,955,651,"1 launcher start; no second instance",25,NAVY)
takeaway(d,"A broad launcher can turn the consumer's writes into a loop.",ORANGE,PALE_ORANGE)
save(im,8)

# Summary as inspection checklist, matching Session 37's dense teaching panels.
im,d=title(9,"Key takeaways","Design for the second delivery","Five checks for any retryable background task.")
t(d,86,244,"PRINCIPLE",28,MUTED,BOLD);t(d,758,244,"EVIDENCE TO INSPECT",28,MUTED,BOLD)
for i,(head,evidence,kind,color) in enumerate((("At least once","A job can be delivered again","queue",BLUE),("Stable identity","Target + requested version","doc",PURPLE),("Durable progress","Persisted checkpoint per item","db",GREEN),("Explicit result","OK / FAILED / CANCEL","check",ORANGE),("No launcher loop","Trigger path excludes job writes","gear",BLUE))):
    y=293+i*102;box(d,(62,y,1613,y+88),color)
    mark(d,85,y+10,kind,color);t(d,184,y+18,head,39,color,HEAD)
    d.line((720,y+12,720,y+76),fill="#d8e1f0",width=2)
    t(d,758,y+27,evidence,28,NAVY,BOLD)
save(im,9)

# Passive close, with connected technical symbols.
im,d=title(10,"Questions","Questions","Thank you.")
for i,(kind,label,color) in enumerate((("doc","EVENT",GREEN),("gear","WORKFLOW",PURPLE),("queue","JOB",BLUE))):
    x=372+i*446;mark(d,x,576,kind,color);t(d,x-14,665,label,37,color,HEAD)
    if i<2:arrow(d,x+83,611,x+408,color)
save(im,10)

print(f"Rendered {len(list(OUT.glob('slide_*.png')))} slides in {OUT}")
