import pandas as pd
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

salaries = pd.read_csv("salaries.csv")
salaries = salaries.drop(["employment_type","salary","salary_currency","employee_residence"], axis = 1)
salaries.rename(columns = {"work_year":"Year","experience_level":"Experience Level","job_title":"Job Title","salary_in_usd":"Salary in USD","remote_ratio":"Remote ratio","company_location":"Company Location","company_size":"Company Size"}, inplace=True)
salaries.replace({"Company Size":{"L":"Large","M":"Medium","S":"Small"}},inplace=True)
salaries.replace({"Experience Level":{"EN":"Entry","MI":"Middle","SE":"Senior","EX":"Executive"}},inplace=True)
salaries["Salary in Euro"] = salaries["Salary in USD"] * 0.91
salaries["Experience Level"] = salaries["Experience Level"].astype("category")
#salaries["Year"] = pd.to_datetime(salaries["Year"], format="%Y")

salaries_year  = salaries.groupby("Year",as_index=False,).median("Salary in Euro")
#year_formatter = mdates.DateFormatter("%Y")
salaries_year.plot.bar(x = "Year", y = "Salary in Euro")
salaries_23 = salaries([salaries["Year"] = "2023"])
salaries["Average Salary"] = salaries["Salary in Euro"].mean()
salaries_job_title = salaries.nlargest(10,"Average Salary")

salaries_job_title.plot.bar(x = "Job Title", y = "Average Salary")

