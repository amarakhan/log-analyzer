# log-analyzer
Command-line Python script for analyzing log files.

# Log Analyzer

A command-line tool written in Python that parses and analyzes log files. It provides insights such as error counts, user activity, and performance metrics, with the option to output results in either plain text or JSON format. To get scheduled insights from log files, this tool can be set up as a cron job.

## Features

- **Error Analysis:** Reports the number of errors in the log file.
- **User Activity:** Summarizes user activity found in the log file.
- **Performance Metrics:** Calculates performance-related metrics from the log file.
- **Flexible Output:** Supports output in both plain text and JSON format for easy integration with other tools or systems.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.6 or higher installed on your system.

## Running the Script

To run the script for error analysis, use the following command:

```bash
python log_analyzer.py --log_file /path/to/logfile.txt --analysis_type errors --output_format json

```

## Arguments

The script accepts the following arguments:

- `log_file`: The path to the log file to be analyzed.
- `analysis_type`: The type of analysis to perform (`errors`, `user_activity`, or `performance`).
- `output_format`: The format in which to output the results (`text` or `json`).
