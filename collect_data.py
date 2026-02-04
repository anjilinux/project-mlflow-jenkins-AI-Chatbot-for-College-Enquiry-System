import pandas as pd

def collect_data():
    data = {
        "question": [
            "What courses are offered?",
            "What is the admission process?",
            "What are the hostel fees?",
            "Does the college provide placements?"
        ],
        "intent": [
            "courses",
            "admission",
            "fees",
            "placements"
        ]
    }

    df = pd.DataFrame(data)
    df.to_csv("data/raw/college_faq.csv", index=False)

if __name__ == "__main__":
    collect_data()
