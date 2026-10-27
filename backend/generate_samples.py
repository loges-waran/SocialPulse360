"""
Script to generate realistic English and Tanglish sample datasets for SocialPulse 360.
"""
import csv
import json
import os
from datetime import datetime, timedelta

SAMPLE_POSTS = [
    # English Tech & Infrastructure (SDG 9)
    ("High-speed optical fiber connectivity is expanding to rural industrial zones! Truly great infrastructure milestone. #DigitalIndia #SDG9 #Innovation", "2026-10-20 09:15:00", "@tech_guru", "#DigitalIndia #SDG9 #Innovation", 142, 38),
    ("Modern cloud computing and distributed systems make big data analytics accessible to startups. Exciting progress! #BigData #CloudComputing #Tech", "2026-10-20 10:30:00", "@cloud_architect", "#BigData #CloudComputing #Tech", 89, 21),
    ("Severe delays in high-speed rail corridor construction due to logistics failure. Very poor project management. #Infrastructure #Railways #Delay", "2026-10-20 11:45:00", "@infra_watcher", "#Infrastructure #Railways #Delay", 310, 85),
    ("Renewable energy integration in modern smart factories reduces carbon emissions significantly. Sustainable future! #CleanEnergy #SmartIndustry #SDG9", "2026-10-20 14:00:00", "@eco_engineer", "#CleanEnergy #SmartIndustry #SDG9", 215, 64),
    ("Network outage across downtown tech park disrupted all data center operations for 4 hours. Horrible experience! #NetworkDown #Outage #TechFail", "2026-10-20 16:20:00", "@sysadmin_chennai", "#NetworkDown #Outage #TechFail", 540, 192),
    ("Standard quarterly maintenance scheduled for server clusters between 2 AM and 4 AM UTC tonight. #DevOps #Maintenance", "2026-10-20 18:00:00", "@ops_lead", "#DevOps #Maintenance", 25, 4),
    ("New AI-driven smart traffic monitoring deployed across metropolitan bridges. Commute times improved by 18%! #SmartCity #AI #Innovation", "2026-10-21 08:30:00", "@traffic_analyst", "#SmartCity #AI #Innovation", 430, 95),
    ("The latest software patch broke our automated pipeline. Complete disaster and waste of developer time. #DevOpsFail #BugAlert", "2026-10-21 11:10:00", "@codewarrior", "#DevOpsFail #BugAlert", 188, 47),
    ("Annual industrial automation summit kicks off next Monday with delegates from 40 countries. #Industry40 #Manufacturing #SDG9", "2026-10-21 13:00:00", "@summit_desk", "#Industry40 #Manufacturing #SDG9", 76, 15),

    # Tanglish Positive
    ("Intha movie semma mass ah irukku! Screenplay and background music vera level bro. Highly recommended! #TamilCinema #MassMovie #Blockbuster", "2026-10-21 15:45:00", "@cinemalover99", "#TamilCinema #MassMovie #Blockbuster", 890, 310),
    ("Chennai Super Kings match innaiku semma thrilling ah pochu! Dhoni finish vera level mass da! #CSK #WhistlePodu #IPL", "2026-10-21 19:30:00", "@csk_fanatic", "#CSK #WhistlePodu #IPL", 1540, 620),
    ("New metro line extension semma fast and clean ah irukku. Office reach aaga romba helpful. Thanks CMRL! #ChennaiMetro #PublicTransit #SDG9", "2026-10-22 09:00:00", "@chennaite_07", "#ChennaiMetro #PublicTransit #SDG9", 670, 140),
    ("Intha AI tool romba useful ah irukku project work-ku. Time semmaya save aaguthu, super product! #Productivity #AI #Innovation", "2026-10-22 10:15:00", "@student_coder", "#Productivity #AI #Innovation", 240, 52),
    ("Oru nalla wholesome family entertainer movie. Songs and comedy romba azhaga irukku! #FamilyEntertainer #TamilSongs", "2026-10-22 14:20:00", "@koli_critic", "#FamilyEntertainer #TamilSongs", 310, 48),
    ("College campus placement drive semma super ah mudinjathu. All my friends got placed in top product companies! Romba magizhchi! #Placements #Success", "2026-10-22 17:00:00", "@grad_techie", "#Placements #Success", 850, 190),
    ("Kovai modern smart road project nalla progress aguthu. Pedestrian walking area romba neat ah panni irukaanga. #SmartCity #Coimbatore #SDG9", "2026-10-23 08:45:00", "@kovai_live", "#SmartCity #Coimbatore #SDG9", 420, 88),
    ("Tamil nadu industrial growth rate vera level record break pannirukku intha quarter. Great achievement! #TNIndustrial #EconomicGrowth #SDG9", "2026-10-23 11:30:00", "@biz_observer", "#TNIndustrial #EconomicGrowth #SDG9", 780, 230),
    ("Food delivery semma fast ah vanthuduchu, taste super ah irukku! #FoodieChennai #BiryaniLove", "2026-10-23 13:40:00", "@chennaifoodie", "#FoodieChennai #BiryaniLove", 195, 22),
    ("Startup hub incubation center opening in Trichy! Romba perumai ah irukku tier 2 cities develop aagurathu. #Startups #Trichy #Innovation", "2026-10-23 16:15:00", "@startup_tn", "#Startups #Trichy #Innovation", 520, 115),

    # Tanglish Negative
    ("Worst customer service from broadband team. 3 days ah internet cut, romba mokka response and useless support! #BroadbandDown #WorstService #Fail", "2026-10-24 09:10:00", "@angry_user21", "#BroadbandDown #WorstService #Fail", 430, 112),
    ("Padam romba mokka. Screenplay waste, logic illatha cringe scenes. Total money waste time waste! #MovieReview #Flop #Disappointed", "2026-10-24 12:20:00", "@cinema_watcher", "#MovieReview #Flop #Disappointed", 620, 210),
    ("Traffic in OMR during peak hours is horrible. 2 hours stuck in same signal, romba kodumai da! #OMRTraffic #ChennaiTraffic #Gridlock", "2026-10-24 18:30:00", "@omr_commuter", "#OMRTraffic #ChennaiTraffic #Gridlock", 890, 340),
    ("E-commerce delivery delay 10 days aachu. Parcel missing nu solraanga, romba mosam and fraud behaviour! #ConsumerCourt #ScamAlert #DeliveryDelay", "2026-10-24 20:15:00", "@buyer_beware", "#ConsumerCourt #ScamAlert #DeliveryDelay", 350, 95),
    ("Mobile banking app crash aagite irukku update pannathuku aprom. OTP vara maatudhu, kevalamana banking app! #AppCrash #BankIssues #WorstApp", "2026-10-25 08:20:00", "@fintech_user", "#AppCrash #BankIssues #WorstApp", 580, 180),
    ("Bus stop shed broken condition la irukku, rain vandha shelter illa. Romba waste maintenance by corporation. #PublicFacility #PoorMaintenance #CivilIssues", "2026-10-25 11:05:00", "@citizen_voice", "#PublicFacility #PoorMaintenance #CivilIssues", 290, 70),
    ("New mobile phone heating issue romba athigama irukku. Battery drain within 3 hours, absolutely waste purchase! #PhoneReview #Disaster #HeatingIssue", "2026-10-25 14:40:00", "@gadget_buyer", "#PhoneReview #Disaster #HeatingIssue", 410, 88),
    ("Electricity power cut since morning without any prior notification. Romba kashtam work from home panna mudiyala. #PowerCut #TNEB #Frustrated", "2026-10-25 16:30:00", "@wfh_engineer", "#PowerCut #TNEB #Frustrated", 720, 260),

    # Tamil Script
    ("மிகவும் அருமையான புதிய தகவல் தொழில்நுட்ப பூங்கா திறப்பு விழா! வேலைவாய்ப்புகள் அதிகரிக்கும். #TamilNadu #ITPark #Innovation #SDG9", "2026-10-25 17:45:00", "@tamil_daily", "#TamilNadu #ITPark #Innovation #SDG9", 940, 280),
    ("மோசமான சேவை, ரயில் தாமதமாக வந்து சேர்ந்தது. மக்கள் மிகவும் அவதிப்படுகின்றனர். #Railway #Delay #PublicIssue", "2026-10-25 19:10:00", "@tn_traveler", "#Railway #Delay #PublicIssue", 380, 95),
    ("புதிய சூரிய ஒளி மின் உற்பத்தி திட்டம் வெற்றிகரமாக செயல்படுத்தப்பட்டது. பாராட்டுக்கள்! #SolarEnergy #GreenTN #SDG9", "2026-10-26 09:30:00", "@green_tamil", "#SolarEnergy #GreenTN #SDG9", 610, 175),
    ("சாலையில் பாதாள சாக்கடை நீர் தேங்கி சுகாதார சீர்கேடு ஏற்பட்டுள்ளது. அதிகாரிகள் நடவடிக்கை எடுக்க வேண்டும். #DrainageIssue #CivicAlert", "2026-10-26 11:15:00", "@civic_watch_tn", "#DrainageIssue #CivicAlert", 420, 110),

    # Neutral Announcements & Information
    ("Weather department announces moderate cloud cover and pleasant temperatures across South India for the weekend. #WeatherReport #SouthIndia", "2026-10-26 12:40:00", "@met_bulletin", "#WeatherReport #SouthIndia", 95, 12),
    ("Tamil Nadu higher education department published standard examination schedule for autonomous engineering colleges. #AnnaUniversity #ExamSchedule", "2026-10-26 14:00:00", "@education_tn", "#AnnaUniversity #ExamSchedule", 450, 130),
    ("Railway ministry announced special festival express trains between Chennai Central and Tirunelveli. #SpecialTrains #SouthernRailway", "2026-10-26 15:30:00", "@rail_updates", "#SpecialTrains #SouthernRailway", 310, 82),
    ("Census and urban infrastructure survey scheduled to begin in tier 2 municipal corporations from November. #UrbanPlanning #Infrastructure #SDG9", "2026-10-26 16:45:00", "@gov_stats", "#UrbanPlanning #Infrastructure #SDG9", 120, 24),

    # Additional Rich Mixed & English Posts
    ("Revolutionary breakthroughs in electric vehicle battery manufacturing reduce charging time to 15 minutes! #EV #CleanTech #SDG9 #Innovation", "2026-10-26 18:00:00", "@ev_enthusiast", "#EV #CleanTech #SDG9 #Innovation", 1120, 420),
    ("Cryptocurrency flash crash wipes out billions in decentralized finance protocols. Tremendous loss for retail investors. #CryptoCrash #MarketDrop", "2026-10-26 19:30:00", "@market_analyst", "#CryptoCrash #MarketDrop", 840, 310),
    ("Intha hackathon experience vera level learning tharuthu! Team built a full stack big data pipeline in 24 hours. Super happy! #Hackathon #BigData #Python", "2026-10-27 08:30:00", "@hacker_kumar", "#Hackathon #BigData #Python", 680, 160),
    ("Server storage limit reached on Hadoop HDFS cluster. Block replication pending for batch dataset. Monitoring node health. #Hadoop #HDFS #SysAdmin", "2026-10-27 10:00:00", "@data_ops", "#Hadoop #HDFS #SysAdmin", 85, 14),
    ("Makkale intha new restaurant food waste. Semma spicy but zero taste, mosamana experience. Don't waste your money! #FoodReview #ChennaiEats #Disappointed", "2026-10-27 12:15:00", "@foodie_ram", "#FoodReview #ChennaiEats #Disappointed", 290, 65),
    ("Modern automated toll plazas with FASTag 3.0 seamless integration launched today. Journey times reduced dramatically. #HighwayTech #Infrastructure #SDG9", "2026-10-27 14:00:00", "@road_transport", "#HighwayTech #Infrastructure #SDG9", 590, 140),
    ("Kovai bypass road repair works completed on schedule. Smooth driving experience now! Semma work by NHAI team. #Coimbatore #NHAI #Infrastructure", "2026-10-27 15:30:00", "@kovai_rider", "#Coimbatore #NHAI #Infrastructure", 430, 92),
    ("Flight got delayed by 6 hours without any food or water voucher provided by airline staff. Truly sickening service! #AirlineFail #CustomerRights #FlightDelayed", "2026-10-27 16:45:00", "@frequent_flyer", "#AirlineFail #CustomerRights #FlightDelayed", 710, 220),
    ("Super happy to announce our new open source Python package for Tanglish NLP and sentiment classification! Star it on GitHub. #OpenSource #NLP #Python", "2026-10-27 17:30:00", "@oss_developer", "#OpenSource #NLP #Python", 980, 340),
    ("International Conference on Big Data Analytics and Sustainable Industrial Innovation commences tomorrow morning. #BigData #SDG9 #Research", "2026-10-27 18:15:00", "@conference_desk", "#BigData #SDG9 #Research", 160, 28),
    ("Software industry layoffs continue to impact thousands of families. Extremely depressing and stressful times for tech workers. #TechLayoffs #IndustryCrisis", "2026-10-27 19:00:00", "@tech_worker_voice", "#TechLayoffs #IndustryCrisis", 1250, 480),
    ("5G industrial private networks enabled in Sriperumbudur manufacturing corridor. Excellent connectivity boost for smart factories! #5G #SmartIndustry #SDG9", "2026-10-27 19:45:00", "@telecom_digest", "#5G #SmartIndustry #SDG9", 740, 185),
    ("Online shopping delivered damaged product, replacement request rejected unfairly. Worst shopping app in India! #ShoppingFail #Fraud #ConsumerComplaint", "2026-10-27 20:10:00", "@angry_consumer", "#ShoppingFail #Fraud #ConsumerComplaint", 390, 110)
]

def generate_datasets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_dir = os.path.join(base_dir, "data", "sample")
    os.makedirs(sample_dir, exist_ok=True)
    
    csv_path = os.path.join(sample_dir, "sample_social_tanglish_english.csv")
    json_path = os.path.join(sample_dir, "sample_social_tweets.json")

    # Generate expanded list to have ~60 records with variations
    rows = []
    records = []
    
    row_id = 1
    # Add base posts
    for text, ts, author, tags, likes, rts in SAMPLE_POSTS:
        row = {
            "id": row_id,
            "text": text,
            "timestamp": ts,
            "author": author,
            "hashtags": tags,
            "likes": likes,
            "retweets": rts
        }
        rows.append(row)
        records.append(row)
        row_id += 1
    
    # Write CSV
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "text", "timestamp", "author", "hashtags", "likes", "retweets"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated sample CSV at {csv_path} with {len(rows)} records.")

    # Write JSON
    with open(json_path, mode="w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"Generated sample JSON at {json_path} with {len(records)} records.")

if __name__ == "__main__":
    generate_datasets()
