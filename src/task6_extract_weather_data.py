import csv
import re
from typing import Any, List, Dict


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    return (line.replace("\u00a0", " ")
                .replace("\u2103", "C")
                .encode("ascii", "ignore")
                .decode("ascii")
                .strip())


def extract_weather_data(text_file: str) -> List[Dict[str, Any]]:
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.

    Raises:
        FileNotFoundError: If the text file does not exist.
    """
    pattern = re.compile(
        r"Date:\s*(?P<date>[^,]+),\s*"
        r"Max Temp:\s*(?P<max>-?\d+(?:\.\d+)?)\s*°?C,\s*"
        r"Min Temp:\s*(?P<min>-?\d+(?:\.\d+)?)\s*°?C,\s*"
        r"Humidity:\s*(?P<humidity>\d+(?:\.\d+)?)\s*%,\s*"
        r"Precipitation:\s*(?P<precipitation>-?\d+(?:\.\d+)?)\s*mm"
    )
    result = []
    with open(text_file, "r", encoding="utf-8") as source:
        for raw_line in source:
            match = pattern.search(clean_text(raw_line))
            if match:
                result.append({
                    "date": match.group("date").strip(),
                    "max_temperature": float(match.group("max")),
                    "min_temperature": float(match.group("min")),
                    "humidity": int(float(match.group("humidity"))),
                    "precipitation": float(match.group("precipitation")),
                })
    return result


def save_to_csv(data: List[Dict[str, Any]], filename: str = "extracted_weather_data.csv") -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]
    with open(filename, "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        for day in data:
            writer.writerow({
                "Date": day["date"],
                "Max Temperature": day["max_temperature"],
                "Min Temperature": day["min_temperature"],
                "Humidity": day["humidity"],
                "Precipitation": day["precipitation"],
            })


if __name__ == "__main__":
    try:
        # Extract data from the text file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        # Save the extracted data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")
