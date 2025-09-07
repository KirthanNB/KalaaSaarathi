import subprocess, os
def build_and_host(product_id: str):
    os.chdir("/c/CraftLink/shop")
    subprocess.run(["npm","run","export"], check=True)
    os.chdir("/c/CraftLink")
    # firebase hosting copy (we’ll do via cloudbuild tomorrow)
    return f"https://craftlink-ai.web.app/product/{product_id}"