#!/usr/bin/env python
import warnings
import pandas as pd
import re

from lead_qualification.crew import LeadQualification
from lead_qualification.email_sender import route_email
warnings.filterwarnings("ignore")


def run():
    try:
        # Read CSV file
        df = pd.read_csv("src/lead_qualification/leads.csv")

        print(f"\nFound {len(df)} leads to evaluate...\n")

        results = []

        for index, row in df.iterrows():

            print("\n" + "=" * 80)
            print(f"Processing Lead {index + 1}/{len(df)}")
            print(f"Name: {row['name']}")
            print("=" * 80)

            inputs = {
                "name": row["name"],
                "business_type": row["business_type"],
                "city": row["city"],
                "investment": str(row["investment"]),
                "occupation": row["occupation"]
            }

            result = LeadQualification().crew().kickoff(inputs=inputs)

            print("\nRESULT:")
            print(result)
            # Extract HOT / WARM / COLD status from CrewAI result
            result_text = str(result)

            status_match = re.search(
                r"Lead Status:\s*(HOT|WARM|COLD)",
                result_text,
                re.IGNORECASE
            )

            if status_match:
                lead_status = status_match.group(1).upper()
            else:
                lead_status = "UNKNOWN"

            print(f"\nDetected Lead Status: {lead_status}")

            # Route email according to lead status
            email_sent = False

            if lead_status in ["HOT", "WARM"]:
                email_sent = route_email(
                    lead_status=lead_status,
                    lead_name=row["name"],
                    lead_email=row["email"]
                )

            elif lead_status == "COLD":
                print(f"No email sent to {row['name']} because lead is COLD.")
            results.append({
                "name": row["name"],
                "email": row["email"],
                "lead_status": lead_status,
                "email_sent": email_sent,
                "result": str(result)
            })
        # Save output
        output_df = pd.DataFrame(results)
        output_df.to_csv("lead_results.csv", index=False)

        print("\n" + "=" * 80)
        print("ALL LEADS PROCESSED SUCCESSFULLY")
        print("Results saved to lead_results.csv")
        print("=" * 80)

    except Exception as e:
        print(f"\nERROR: {e}")


if __name__ == "__main__":
    run()