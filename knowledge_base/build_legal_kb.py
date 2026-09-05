import os
import json
import csv

BASE_DIR = r"c:\Users\APURVA\Desktop\Hackathon\legal_metrology_KB_&_RB"
KB_DIR = os.path.join(BASE_DIR, "legal_knowledge_base")
NOTICES_DIR = os.path.join(KB_DIR, "notices")

os.makedirs(os.path.join(NOTICES_DIR, "improvement"), exist_ok=True)
os.makedirs(os.path.join(NOTICES_DIR, "seizure"), exist_ok=True)
os.makedirs(os.path.join(NOTICES_DIR, "panchanama"), exist_ok=True)
os.makedirs(os.path.join(NOTICES_DIR, "compounding"), exist_ok=True)

print("Created legal_knowledge_base directory structure.")
