import pandas as pd
import numpy as np
import re
import pickle
import sklearn
import xgboost
import lightgbm
import warnings

warnings.filterwarnings("ignore")

map = {
    "subtype": ["forward", "local", "ips"],
    "level": ["notice", "warning", "alert"],
    "srccountry": [
        "India",
        "Reserved",
        "United States",
        "Somalia",
        "Netherlands",
        "Australia",
        "Germany",
        "Bulgaria",
        "Cyprus",
        "France",
        "Unknown",
        "Japan",
        "Malaysia",
        "United Arab Emirates",
        "Ireland",
        "Canada",
        "United Kingdom",
        "Hong Kong",
        "Bahrain",
        "Italy",
        "Singapore",
        "Sweden",
        "Brazil",
        "South Africa",
        "Korea, Republic of",
        "Czech Republic",
        "Pakistan",
        "Russian Federation",
        "Thailand",
        "Lithuania",
        "Ecuador",
        "Uzbekistan",
        "Chile",
        "Denmark",
        "Maldives",
        "Portugal",
        "China",
        "Ukraine",
        "New Zealand",
        "Mali",
        "Mongolia",
        "Ghana",
        "Oman",
        "Georgia",
        "Mauritius",
        "Turkey",
        "Taiwan",
        "Spain",
        "Argentina",
        "Saudi Arabia",
        "Finland",
        "Egypt",
        "Romania",
        "Slovenia",
        "Iraq",
        "Belize",
        "Cambodia",
        "Switzerland",
        "Sri Lanka",
        "Philippines",
        "Nigeria",
        "Ethiopia",
        "Serbia",
        "Iran, Islamic Republic of",
        "Armenia",
        "Tunisia",
        "Israel",
        "Belgium",
        "Mexico",
        "Tanzania, United Republic of",
        "Colombia",
        "Isle of Man",
        "El Salvador",
        "Azerbaijan",
        "Indonesia",
        "Greece",
        "Malta",
        "Jordan",
        "Kenya",
        "Belarus",
        "Kazakhstan",
        "Bosnia and Herzegovina",
        "Croatia",
        "Hungary",
        "Qatar",
        "Latvia",
        "Vietnam",
        "Bangladesh",
        "Estonia",
        "Kyrgyzstan",
        "Benin",
        "Albania",
        "Myanmar",
    ],
    "srcintf": ["LLB- Connect", "Local_LAN", "unknown-0", "root"],
    "srcintfrole": ["wan", "undefined"],
    "dstintf": ["Local_LAN", "LLB- Connect"],
    "dstintfrole": ["undefined", "wan"],
    "action": [
        "client-rst",
        "close",
        "accept",
        "server-rst",
        "deny",
        "timeout",
        "ip-conn",
        "dns",
        "dropped",
    ],
    "service": [
        "HTTPS",
        "FTPS",
        "tcp/3349",
        "PING",
        "tcp/44094",
        "ForFTP_DATA",
        "tcp/7143",
        "NHP-FLUX",
        "DNS",
        "icmp/0/8",
        "tcp/51179",
        "tcp/2705",
        "tcp/8501",
        "tcp/8085",
        "tcp/16322",
        "udp/8081",
        "udp/5353",
        "tcp/43894",
        "tcp/58591",
        "tcp/1800",
        "tcp/2023",
        "udp/8083",
        "udp/8080",
        "tcp/9001",
        "HTTP",
        "tcp/43893",
        "tcp/6443",
        "tcp/33335",
        "tcp/8888",
        "tcp/13333",
        "tcp/40501",
        "tcp/1240",
        "tcp/11115",
        "tcp/2005",
        "tcp/2091",
        "tcp/2101",
        "tcp/2090",
        "tcp/33010",
        "udp/1027",
        "RTSP",
        "tcp/32914",
        "udp/8082",
        "tcp/30089",
        "tcp/33389",
        "SMTPS",
        "tcp/26657",
        "tcp/7366",
        "tcp/4433",
        "tcp/33896",
        "tcp/5678",
        "tcp/33000",
        "tcp/26659",
        "tcp/8546",
        "tcp/33892",
        "tcp/41433",
        "tcp/21912",
        "tcp/10433",
        "tcp/5601",
        "tcp/24413",
        "tcp/9650",
        "tcp/18546",
        "tcp/8545",
        "tcp/3789",
        "tcp/1389",
        "VDOLIVE",
        "tcp/9990",
        "tcp/61014",
        "tcp/18545",
        "tcp/16589",
        "tcp/11000",
        "tcp/7433",
        "tcp/22020",
        "tcp/55366",
        "NTP",
        "tcp/26660",
        "tcp/32371",
        "tcp/8815",
        "X-WINDOWS",
        "tcp/43389",
        "tcp/20201",
        "tcp/48942",
        "TELNET",
        "FTP",
        "tcp/8547",
        "udp/22",
        "tcp/50005",
        "tcp/5005",
        "tcp/42914",
        "tcp/49389",
        "tcp/17882",
        "tcp/8845",
        "SNMP",
        "tcp/13384",
        "tcp/1017",
        "tcp/8548",
        "udp/4000",
        "tcp/888",
        "tcp/8819",
        "tcp/8807",
        "tcp/62922",
        "tcp/8820",
        "tcp/14433",
        "tcp/8854",
        "tcp/11114",
        "tcp/15006",
        "tcp/5500",
        "tcp/54077",
        "udp/11211",
        "tcp/2006",
        "tcp/8818",
        "tcp/12433",
        "tcp/34130",
        "tcp/35366",
        "tcp/3200",
        "tcp/14330",
        "tcp/49676",
        "tcp/8934",
        "tcp/6089",
        "tcp/9089",
        "tcp/13389",
        "tcp/39389",
        "tcp/8989",
        "MS-SQL",
        "tcp/11118",
        "tcp/33905",
        "tcp/2999",
        "tcp/44273",
        "tcp/32288",
        "tcp/20412",
        "tcp/41832",
        "tcp/28222",
        "tcp/25898",
        "tcp/9195",
        "tcp/3030",
        "tcp/5107",
        "tcp/21988",
        "tcp/3433",
        "tcp/24444",
        "tcp/5050",
        "tcp/8521",
        "tcp/23390",
        "tcp/15555",
        "tcp/48380",
        "tcp/9433",
        "tcp/6802",
        "tcp/40389",
        "tcp/3189",
        "tcp/17433",
        "tcp/33809",
        "tcp/16101",
        "tcp/43898",
        "tcp/3369",
        "tcp/10000",
        "tcp/2085",
        "tcp/2105",
        "tcp/3438",
        "tcp/13571",
        "tcp/2078",
        "tcp/2108",
        "tcp/1435",
        "SIP",
        "tcp/2107",
        "tcp/2103",
        "tcp/11117",
        "tcp/21181",
        "tcp/3111",
        "tcp/3198",
        "tcp/42130",
        "tcp/3333",
        "udp/8000",
        "tcp/59101",
        "tcp/5901",
        "tcp/9527",
        "KERBEROS",
        "gre",
        "tcp/8120",
        "tcp/36584",
        "udp/1900",
        "tcp/24722",
        "tcp/5555",
        "tcp/10037",
        "tcp/46389",
        "tcp/18389",
        "tcp/5515",
        "tcp/8122",
        "tcp/8121",
        "tcp/1551",
        "tcp/14444",
        "udp/30301",
        "tcp/8512",
        "tcp/9026",
        "tcp/7234",
        "tcp/8443",
        "tcp/5539",
        "tcp/3395",
        "tcp/14578",
        "tcp/3381",
        "tcp/33069",
        "tcp/40002",
        "tcp/3397",
        "tcp/1456",
        "tcp/666",
        "tcp/5366",
        "tcp/311",
        "tcp/1110",
        "tcp/33894",
        "tcp/51433",
        "tcp/7498",
        "tcp/33189",
        "tcp/7384",
        "tcp/50988",
        "tcp/35389",
        "tcp/30000",
        "tcp/45389",
        "tcp/8125",
        "tcp/12203",
        "tcp/3137",
        "tcp/12199",
        "tcp/12201",
        "tcp/12207",
        "tcp/26",
        "tcp/3319",
        "tcp/41389",
        "tcp/50014",
        "tcp/43451",
        "tcp/22589",
        "tcp/35222",
        "tcp/39106",
        "tcp/58053",
        "tcp/50429",
        "tcp/58008",
        "tcp/15180",
        "tcp/8983",
        "tcp/51389",
        "tcp/12204",
        "tcp/8129",
        "tcp/7788",
        "tcp/2109",
        "tcp/29494",
        "tcp/8124",
        "tcp/21609",
        "DCE-RPC",
        "tcp/8117",
        "tcp/15433",
        "tcp/22051",
        "udp/19",
        "tcp/2289",
        "tcp/25637",
        "tcp/50374",
        "tcp/1414",
        "tcp/8128",
        "tcp/1015",
        "tcp/4444",
        "tcp/8127",
        "tcp/9110",
        "tcp/53890",
        "tcp/3110",
        "tcp/8119",
        "tcp/4389",
        "tcp/3365",
        "tcp/1919",
        "tcp/10026",
        "tcp/5433",
        "tcp/16666",
        "tcp/13433",
        "tcp/40994",
        "tcp/33033",
        "tcp/49830",
        "tcp/1002",
        "tcp/40995",
        "tcp/18433",
        "tcp/62044",
        "tcp/3390",
        "tcp/27429",
        "tcp/57018",
        "tcp/3387",
        "tcp/1106",
        "tcp/3309",
        "tcp/60230",
        "tcp/830",
        "tcp/11111",
        "tcp/31111",
        "tcp/541",
        "tcp/33339",
        "tcp/59963",
        "tcp/12205",
        "HQssh",
        "tcp/56295",
        "tcp/12208",
        "tcp/6366",
        "tcp/12200",
        "tcp/9179",
        "tcp/51194",
        "tcp/1741",
        "tcp/6618",
        "tcp/3005",
        "udp/7474",
        "tcp/43891",
        "tcp/40957",
        "tcp/31433",
        "tcp/33289",
        "tcp/3388",
        "tcp/6535",
        "tcp/2290",
        "tcp/646",
        "FTP_1",
        "tcp/43399",
        "tcp/41005",
        "tcp/11116",
        "tcp/20433",
        "tcp/8513",
        "tcp/151",
        "tcp/16095",
        "tcp/53389",
        "tcp/3479",
        "tcp/25555",
        "tcp/33089",
        "tcp/63390",
        "tcp/5010",
        "tcp/1911",
        "tcp/9100",
        "tcp/15005",
        "tcp/2389",
        "tcp/2299",
        "tcp/11593",
        "tcp/22015",
        "tcp/1501",
        "tcp/24424",
        "RDP",
        "tcp/131",
        "tcp/2761",
        "tcp/15366",
        "tcp/202",
        "tcp/175",
        "tcp/223",
        "tcp/1656",
        "tcp/12206",
        "tcp/28573",
        "tcp/19651",
        "tcp/63030",
        "tcp/65153",
        "tcp/26442",
        "tcp/36483",
        "tcp/23465",
        "tcp/19715",
        "tcp/12202",
        "tcp/8602",
        "tcp/8500",
        "tcp/16389",
        "tcp/3589",
        "tcp/9292",
        "tcp/2562",
        "tcp/2762",
        "tcp/21847",
        "tcp/33093",
        "tcp/23723",
        "tcp/6700",
        "tcp/19635",
        "tcp/36215",
        "tcp/21587",
        "tcp/7186",
        "tcp/7487",
        "tcp/40929",
        "tcp/801",
        "tcp/8855",
        "tcp/14000",
        "tcp/9036",
        "tcp/38409",
        "tcp/55142",
        "tcp/31906",
        "tcp/12504",
        "tcp/21126",
        "tcp/33219",
        "tcp/21961",
        "tcp/8433",
        "tcp/64338",
        "tcp/3000",
        "tcp/43890",
        "tcp/48000",
        "tcp/49999",
        "tcp/5613",
        "Tomcat-Apache",
        "tcp/21247",
        "tcp/8530",
        "tcp/38923",
        "tcp/5367",
        "udp/6881",
        "tcp/38912",
        "tcp/33333",
        "tcp/5938",
        "tcp/38955",
        "tcp/3889",
        "tcp/17316",
        "tcp/7777",
        "tcp/40404",
        "SOCKS",
        "tcp/45133",
        "tcp/38916",
        "tcp/51165",
        "tcp/1444",
        "tcp/38937",
        "tcp/50007",
        "tcp/7351",
        "tcp/803",
        "tcp/802",
        "tcp/3391",
        "tcp/2018",
        "tcp/777",
        "tcp/3392",
        "tcp/4899",
        "tcp/3394",
        "tcp/1521",
        "tcp/1214",
        "tcp/38957",
        "tcp/1212",
        "tcp/48389",
        "tcp/3393",
        "IKE",
        "tcp/3385",
        "tcp/7194",
        "tcp/3386",
        "tcp/38919",
        "tcp/51154",
        "tcp/37628",
        "tcp/45366",
        "tcp/7089",
        "tcp/23341",
        "tcp/60083",
        "tcp/7488",
        "tcp/39099",
        "tcp/21466",
        "tcp/33332",
        "tcp/38954",
        "tcp/41007",
        "tcp/24567",
        "tcp/41023",
        "tcp/7322",
        "tcp/62584",
        "tcp/16240",
        "tcp/32928",
        "tcp/40839",
        "tcp/47347",
        "tcp/45360",
        "tcp/47260",
        "tcp/62767",
        "tcp/38905",
        "tcp/46715",
        "tcp/2468",
        "tcp/31389",
        "tcp/7276",
        "tcp/30015",
        "tcp/14333",
        "tcp/3131",
        "tcp/1109",
        "tcp/19389",
        "tcp/38917",
        "tcp/4089",
        "tcp/53892",
        "tcp/6565",
        "tcp/1981",
        "tcp/33110",
        "tcp/33331",
        "tcp/38906",
        "test1",
        "tcp/12100",
        "udp/427",
        "udp/139",
        "tcp/8880",
        "tcp/8531",
        "tcp/31853",
        "tcp/45107",
        "tcp/16173",
        "tcp/45890",
        "tcp/5513",
        "tcp/17703",
        "tcp/9736",
        "tcp/51140",
        "tcp/1244",
        "tcp/43771",
        "tcp/34123",
        "tcp/10039",
        "tcp/7789",
        "tcp/1022",
        "tcp/2224",
        "tcp/38913",
        "tcp/999",
        "tcp/52529",
        "IRC",
        "tcp/7353",
        "tcp/2300",
        "MYSQL",
        "tcp/41056",
        "tcp/43897",
        "tcp/41024",
        "tcp/1727",
        "tcp/10001",
        "tcp/41059",
        "tcp/8812",
        "tcp/38918",
        "tcp/26666",
        "tcp/41039",
        "tcp/32001",
        "tcp/33899",
        "tcp/41035",
        "tcp/36745",
        "tcp/29002",
        "tcp/58680",
        "tcp/39172",
        "tcp/53255",
        "tcp/53883",
        "tcp/28871",
        "tcp/64367",
        "tcp/6389",
        "tcp/26948",
        "tcp/2526",
        "tcp/19872",
        "tcp/4489",
        "tcp/12345",
        "tcp/2727",
        "tcp/21234",
        "tcp/26805",
        "tcp/32400",
        "tcp/28100",
        "tcp/31317",
        "tcp/8291",
        "tcp/38922",
        "tcp/32022",
        "tcp/3399",
        "tcp/21505",
        "tcp/5369",
        "tcp/11433",
        "tcp/1455",
        "tcp/3289",
        "tcp/4003",
        "tcp/1533",
        "tcp/3383",
        "tcp/38964",
        "tcp/8181",
        "tcp/12126",
        "tcp/155",
        "tcp/7439",
        "tcp/21433",
        "tcp/32768",
        "tcp/6767",
        "tcp/3324",
        "tcp/13310",
        "tcp/6379",
        "tcp/36489",
        "tcp/8532",
        "tcp/33065",
        "tcp/13131",
        "PPTP",
        "tcp/850",
        "tcp/52385",
        "tcp/4171",
        "tcp/1575",
        "udp/1029",
        "tcp/1977",
        "tcp/8533",
        "tcp/12162",
        "tcp/16433",
        "tcp/8088",
        "tcp/53891",
        "tcp/20004",
        "tcp/38947",
        "tcp/23259",
        "tcp/1189",
        "tcp/7078",
        "tcp/3585",
        "tcp/5233",
        "tcp/10089",
        "tcp/8111",
        "tcp/8536",
        "tcp/7175",
        "tcp/3335",
        "tcp/6240",
        "tcp/39036",
        "tcp/39090",
        "tcp/15447",
        "tcp/27381",
        "tcp/53693",
        "tcp/51392",
        "tcp/31900",
        "tcp/37953",
        "tcp/62204",
        "tcp/18606",
        "tcp/43895",
        "tcp/27017",
        "tcp/4567",
        "tcp/17010",
        "tcp/16169",
        "tcp/9910",
        "tcp/12405",
        "tcp/8540",
        "tcp/7389",
        "tcp/5566",
        "tcp/40003",
        "tcp/38999",
        "tcp/47828",
        "tcp/34311",
        "tcp/11833",
        "tcp/5090",
        "tcp/15001",
        "tcp/6100",
        "tcp/8068",
        "tcp/13877",
        "tcp/35971",
        "tcp/9006",
        "tcp/21135",
        "tcp/5520",
        "tcp/33989",
        "tcp/3545",
        "tcp/33246",
        "tcp/1111",
        "tcp/60889",
        "tcp/45271",
        "tcp/3489",
        "tcp/5368",
        "tcp/30389",
        "tcp/2433",
        "tcp/804",
        "tcp/8544",
        "tcp/9000",
        "tcp/33898",
        "udp/1434",
        "tcp/34689",
        "tcp/10567",
        "tcp/23761",
        "tcp/57050",
        "tcp/57117",
        "tcp/32345",
        "tcp/8716",
        "tcp/41405",
        "tcp/40443",
        "tcp/56971",
        "tcp/6881",
        "tcp/37922",
        "tcp/37018",
        "tcp/33589",
        "tcp/22074",
        "tcp/48530",
        "tcp/34404",
        "tcp/3017",
        "tcp/1201",
        "tcp/9002",
        "tcp/50019",
        "tcp/50453",
        "tcp/39915",
        "tcp/39433",
        "tcp/45640",
        "tcp/12723",
        "tcp/41217",
        "tcp/32219",
        "tcp/15495",
        "tcp/8389",
        "tcp/52526",
        "tcp/8515",
        "tcp/1850",
        "tcp/11119",
        "tcp/8092",
        "tcp/8516",
        "tcp/1980",
        "tcp/50009",
        "tcp/8523",
        "tcp/17890",
        "tcp/1",
        "tcp/3398",
        "tcp/1352",
        "tcp/6671",
        "tcp/12587",
        "tcp/34673",
        "tcp/28109",
        "tcp/46432",
        "tcp/16175",
        "tcp/15831",
        "tcp/40945",
        "tcp/6433",
        "tcp/8800",
        "tcp/60042",
        "tcp/5984",
        "tcp/52389",
        "tcp/23389",
        "tcp/7380",
        "tcp/46130",
        "tcp/15871",
        "tcp/7071",
        "tcp/6900",
        "tcp/8139",
        "tcp/20266",
        "tcp/50804",
        "tcp/41285",
        "tcp/7264",
        "tcp/8079",
        "tcp/37182",
        "tcp/63955",
        "tcp/27502",
        "tcp/62218",
        "tcp/45541",
        "tcp/5522",
        "tcp/12363",
        "tcp/40596",
        "tcp/16699",
        "tcp/5255",
        "tcp/11888",
        "tcp/5256",
        "tcp/7491",
        "tcp/29665",
        "tcp/51172",
        "tcp/9500",
        "tcp/33096",
        "tcp/2022",
        "tcp/10035",
        "tcp/12967",
        "tcp/42575",
        "tcp/37875",
        "tcp/58228",
        "tcp/58837",
        "tcp/34415",
        "tcp/52103",
        "tcp/52304",
        "tcp/47786",
        "tcp/8327",
        "tcp/10714",
        "tcp/8453",
        "tcp/5254",
        "tcp/51129",
        "tcp/22587",
        "tcp/9977",
        "tcp/8933",
        "tcp/190",
        "tcp/5257",
        "tcp/44489",
        "IMAP",
        "tcp/33903",
        "tcp/40004",
        "tcp/25948",
        "tcp/62054",
        "tcp/18426",
        "tcp/27455",
        "tcp/34936",
        "tcp/48177",
        "tcp/32752",
        "tcp/60362",
        "tcp/9200",
        "tcp/4412",
        "tcp/43896",
        "tcp/15389",
        "udp/523",
        "tcp/47468",
        "tcp/5260",
        "tcp/3382",
        "tcp/9989",
        "tcp/5259",
        "tcp/6999",
        "tcp/21337",
        "tcp/6489",
        "tcp/5258",
        "tcp/12477",
        "tcp/5724",
        "tcp/15520",
        "tcp/16662",
        "tcp/47116",
        "tcp/53797",
        "tcp/65294",
        "tcp/42745",
        "tcp/42888",
        "tcp/1337",
        "tcp/40941",
        "tcp/17376",
        "tcp/5262",
        "tcp/43899",
        "tcp/5261",
        "tcp/8008",
        "tcp/1202",
        "tcp/41108",
        "tcp/40044",
        "tcp/8899",
        "tcp/5389",
        "tcp/24163",
        "tcp/15719",
        "tcp/55171",
        "tcp/58632",
        "tcp/11325",
        "tcp/49875",
        "tcp/30317",
        "tcp/11035",
        "tcp/20011",
        "tcp/35613",
        "tcp/32786",
        "tcp/3359",
        "tcp/40969",
        "tcp/6703",
        "tcp/60086",
        "tcp/154",
        "tcp/6697",
        "tcp/20681",
        "tcp/40940",
        "tcp/8090",
        "tcp/28828",
        "tcp/55078",
        "tcp/8223",
        "tcp/60846",
        "tcp/15246",
        "tcp/30199",
        "tcp/41490",
        "tcp/26893",
        "tcp/10036",
        "tcp/2003",
        "tcp/40952",
        "tcp/40971",
        "tcp/8549",
        "tcp/40953",
        "tcp/48097",
        "tcp/1979",
        "tcp/61927",
        "tcp/40982",
        "tcp/27786",
        "tcp/5263",
        "tcp/23577",
        "tcp/13000",
        "tcp/7394",
        "tcp/6500",
        "tcp/23177",
        "tcp/25163",
        "tcp/16134",
        "tcp/6908",
        "tcp/38402",
        "tcp/15852",
        "tcp/10326",
        "tcp/40818",
        "tcp/13020",
        "tcp/7178",
        "tcp/5563",
        "tcp/1089",
        "tcp/5061",
        "tcp/3379",
        "tcp/8873",
        "tcp/9315",
        "tcp/25366",
        "tcp/22731",
        "tcp/26180",
        "tcp/8874",
        "tcp/3396",
        "tcp/33090",
        "udp/40810",
        "tcp/51789",
        "tcp/44389",
        "tcp/213",
        "tcp/36389",
        "tcp/23260",
        "tcp/31388",
        "tcp/60890",
        "tcp/54469",
        "tcp/11569",
        "tcp/11442",
        "tcp/6090",
        "tcp/47209",
        "tcp/35157",
        "tcp/33390",
        "tcp/12000",
        "tcp/6560",
        "tcp/52314",
        "tcp/7204",
        "tcp/3339",
        "tcp/40356",
        "tcp/63564",
        "tcp/2020",
        "tcp/16457",
        "tcp/12350",
        "tcp/40983",
        "tcp/8011",
        "tcp/14673",
        "tcp/33891",
        "tcp/64256",
        "tcp/30405",
        "tcp/54589",
        "tcp/12058",
        "tcp/27297",
        "tcp/38403",
        "tcp/31936",
        "tcp/16682",
        "tcp/12354",
        "tcp/8044",
        "tcp/8591",
        "tcp/53767",
        "tcp/5400",
        "tcp/12355",
        "tcp/8589",
        "tcp/8517",
        "tcp/32182",
        "tcp/12353",
        "tcp/2001",
        "tcp/12349",
        "tcp/15000",
        "tcp/12351",
        "tcp/12352",
        "AOL",
        "tcp/7225",
        "tcp/48554",
        "tcp/24611",
        "tcp/16343",
        "tcp/57762",
        "tcp/5373",
        "tcp/49501",
        "tcp/6888",
        "tcp/54528",
        "tcp/65343",
        "tcp/23333",
        "tcp/33890",
        "tcp/55778",
        "tcp/51159",
        "tcp/6602",
        "tcp/40996",
        "tcp/22682",
        "tcp/32523",
        "tcp/12356",
        "tcp/444",
        "tcp/12357",
        "tcp/53208",
        "tcp/31023",
        "tcp/47389",
        "tcp/9028",
        "tcp/2362",
        "tcp/8333",
        "tcp/43594",
        "tcp/50835",
        "tcp/7895",
        "tcp/57205",
        "tcp/38049",
        "tcp/59469",
        "tcp/38866",
        "tcp/55573",
        "tcp/9034",
        "tcp/9031",
        "tcp/10223",
    ],
}

dtype_f64 = [
    'proto',
    'policyid',
    'duration',
    'sentbyte',
    'rcvdbyte',
    'crscore'
]

def parse_log(log):
    result = {}

    log_fields = [
        "type",
        "subtype",
        "level",
        "srccountry",
        "srcintf",
        "srcintfrole",
        "dstintf",
        "dstintfrole",
        "action",
        "proto",
        "service",
        "policyid",
        "appcat",
        "duration",
        "sentbyte",
        "rcvdbyte",
        "crscore",
    ]
    for field in log_fields:
        pattern = re.compile(r'\s{}=([^"\s]*)'.format(field))
        value1 = pattern.search(log)
        if value1:
            result[field] = value1.group(1)
        pattern = re.compile(r'\s{}="([^"]*)"\s'.format(field))
        value2 = pattern.search(log)
        if value2:
            result[field] = value2.group(1)
        if field not in result:
            result[field] = np.nan
    return result


def clean_data(df):
    df.crscore.fillna(0, inplace=True)
    df = df[~df.srcintf.isna()]
    df.srccountry.fillna("Unknown", inplace=True)
    df.duration.fillna(0, inplace=True)
    df.sentbyte.fillna(0, inplace=True)
    df.rcvdbyte.fillna(0, inplace=True)
    df.appcat = df.appcat.apply(lambda x: 1 if x == "unscanned" else 0)
    df.type = df.type.apply(lambda x: 1 if x == "utm" else 0)
    df[dtype_f64] = df[dtype_f64].astype("float64")
    cols = df.select_dtypes(include="object").columns.tolist()
    for col in cols:
        li = map[col]
        df[col] = df[col].apply(lambda x: li.index(x) if x in li else len(li))
    return df


def read_lines(file_path, n):
    n = n + 1
    with open(file_path, 'r') as file:
        file.seek(0, 2)
        end_position = file.tell()
        lines = []
        newline_count = 0
        while end_position > 0 and newline_count < n:
            end_position -= 1
            file.seek(end_position)
            char = file.read(1)
            if char == '\n':
                newline_count += 1
            if end_position == 0:
                file.seek(0)
                lines.append(file.read(end_position + 1))
            else:
                lines.append(char)
    lines = ''.join(lines[::-1]).split('\n')
    return lines[:-1]


def load_model(model_name):
    with open(model_name, 'rb') as file:
        model = pickle.load(file)
    return model

def detect(model, df):
    with open('scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
    df = scaler.transform(df)
    y_pred = model.predict(df)
    y_pred = pd.Series(y_pred)
    y_pred = y_pred.apply(lambda x: 1 if x == -1 else 0)
    return y_pred
    

def get_threats(y_pred, logs):
    li = []
    if sum(y_pred) > 0:
        for i in range(len(y_pred)):
            if y_pred[i] == 1:
                li.append(i)
    print("Detected {} malicious logs out of {} logs".format(sum(y_pred), len(logs)))
    return li


def load_classifier(model):
    model = load_model(model)
    return model


def classify(model, df, indices):
    df = pd.DataFrame([df.iloc[index] for index in indices])
    df = df.drop(['dstintfrole','proto','srcintfrole','srcintf','dstintf'], axis=1)
    li = model.predict(df)
    return li

def report(df):
    df = list(pd.Series(df).value_counts())
    for count in df:
        print(f'Level {df.index(count)+1} threats: {count}')



if __name__ == "__main__":
    file_path = 'log.txt'
    lines = read_lines(file_path, 5000)
    df1 = pd.DataFrame([parse_log(log) for log in lines])
    df2 = clean_data(df1)
    binclf = load_model('raksha_v3.0.pkl')
    pred = detect(binclf, df2)
    mltclf = load_classifier('raksha_ultra_xlf.pkl')
    indices = get_threats(pred, lines)
    df = classify(mltclf, df2, indices)
    report(df)
    print(f'pickle v{pickle.format_version}')
    print(f'scikit-learn v{sklearn.__version__}')