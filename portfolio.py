import pandas as pd
import sys
import matplotlib.pyplot as plt

salaries = pd.read_csv("salaries.csv")
salaries = salaries.drop(["employment_type","salary","salary_currency","employee_residence"], axis = 1)
salaries.rename(columns = {"work_year":"Year","experience_level":"Experience Level","job_title":"Job Title","salary_in_usd":"Salary in USD","remote_ratio":"Remote ratio","company_location":"Company Location","company_size":"Company Size"}, inplace=True)
salaries.replace({"Company Size":{"L":"Large","M":"Medium","S":"Small"}},inplace=True)
salaries.replace({"Experience Level":{"EN":"Entry","MI":"Middle","SE":"Senior","EX":"Executive"}},inplace=True)
salaries["Salary in Euro"] = salaries["Salary in USD"] * 0.91


salaries2 = salaries.groupby("Year",as_index=False).median("Salary in Euro")

salaries2.plot.bar(x = "Year", y = "Salary in Euro")