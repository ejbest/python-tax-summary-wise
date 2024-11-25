import pandas as pd

# load the csv file
data_file = "statement.xlsx"
data = pd.read_excel(data_file)

# insure ammount column is numeric
data["Amount"] = pd.to_numeric(data["Amount"], errors="coerce")

# general summary: grouping by name
summary_by_name = data.groupby("Payee Name").agg(
    total_ammount = ("Amount","sum"),
    record_count = ("Amount","count")
).reset_index()

# specific summary for blank names
blank_data_summary = data[data["Payee Name"].isnull() | (data["Payee Name"].str.strip()=="")].groupby("Description").agg(
    total_ammount = ("Amount","sum"),
    record_count = ("Amount","count")
).reset_index()

# function to generate the reports
def generate_report(summary_by_name:pd.DataFrame, blank_data_summary:pd.DataFrame, output_file:str="report.txt"):
    with open(output_file,"w") as file:
        # general summary
        file.write("Summary by Name:\n")
        for _, row in summary_by_name.iterrows():
            file.write(f"{row['Payee Name']:<50} ${row['total_ammount']:.2f}   records {row["record_count"]}\n")
        
        # blank summary 
        file.write("\nSummary for blank names:\n")
        for _, row in blank_data_summary.iterrows():
            file.write(f"{row['Description']:<50} ${row['total_ammount']:.2f}   records {row["record_count"]}\n")
    
# Generate the report
report_output_file = "statement_summary_report.txt"
generate_report(summary_by_name,blank_data_summary,report_output_file)

# concatinating general grouping and blank grouping
blank_data_summary.columns = ["Payee Name", "total_ammount", "record_count"]
new_data = pd.concat([summary_by_name,blank_data_summary],ignore_index=True)

# converting to excel
transactions_summary_file = "statement_summary.xlsx"
new_data.to_excel(transactions_summary_file,index=False)

print(f"Report generated successfully: {report_output_file}")
print(f"Summary file generated successfully: {transactions_summary_file}")