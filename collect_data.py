import pandas as pd


def collect_data():
    data = {
        "question": [
            "What courses are offered?",
            "What is the admission process?",
            "Is hostel facility available?",
            "What are the placement opportunities?"
        ],
        "intent": [
            "courses",
            "admission",
            "hostel",
            "placements"
        ]
    }

    df = pd.DataFrame(data)

    # SAVE DIRECTLY IN ROOT
    df.to_csv("college_faq.csv", index=False)

    print("✅ Data saved to college_faq.csv (root directory)")


if __name__ == "__main__":
    collect_data()
