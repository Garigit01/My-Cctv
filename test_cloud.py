import os
from supabase import create_client

# 1. Apni details yahan sahi se bhariye
URL = "https://xfgjjluogifdmgpabbgk.supabase.co" 
KEY = "sb_publishable_B6b9PHhWpmFMpnIS800t2g_kYw0B-aa" # Dashboards se 'anon public' key copy karein

supabase = create_client(URL, KEY)

def upload_test():
    # 2. Check karein ki kya 'cloud_test.jpg' aapke folder mein hai?
    file_path = "cloud_test.jpg" 
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} mil nahi rahi. Ek photo is naam se folder mein rakhein.")
        return

    try:
        with open(file_path, 'rb') as f:
            # 3. 'cctv-alerts' aapke bucket ka naam hona chahiye
            response = supabase.storage.from_("cctv-alerts").upload(
                path="test_upload.jpg", 
                file=f,
                file_options={"content-type": "image/jpeg"}
            )
        print("Mubarak ho! Supabase par photo upload ho gayi.")
    except Exception as e:
        print(f"Kuch gadbad hai: {e}")

# Run karne ke liye
upload_test()