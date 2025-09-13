from google.cloud import vision

def main():
    client = vision.ImageAnnotatorClient()
    print("Google Cloud Vision API is working!")

if __name__ == "__main__":
    main()