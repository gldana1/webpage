import pandas as pd
import sys
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates



plt.style.use("fivethirtyeight")

salaries = pd.read_csv("salaries.csv")
salaries = salaries.drop(["employment_type","salary","salary_currency","employee_residence"], axis = 1)
salaries.rename(columns = {"work_year":"Year","experience_level":"Experience Level","job_title":"Job Title","salary_in_usd":"Salary in USD","remote_ratio":"Remote ratio","company_location":"Company Location","company_size":"Company Size"}, inplace=True)
salaries.replace({"Company Size":{"L":"Large","M":"Medium","S":"Small"}},inplace=True)
salaries.replace({"Experience Level":{"EN":"Entry","MI":"Middle","SE":"Senior","EX":"Executive"}},inplace=True)
salaries["Salary in Euro"] = salaries["Salary in USD"] * 0.91
salaries["Yeardt"] = pd.to_datetime(salaries["Year"], format="%Y")

salaries2 = salaries.groupby("Yeardt",as_index=False).median("Salary in Euro")
x = salaries2["Year"]
y = salaries2["Salary in Euro"]
plt.bar(x, y)
#date_year_format = mpl_dates.DateFormatter("%Y")
#years = mpl_dates.YearLocator()
#ax = plt.gca()
#ax.xaxis.set_major_locator(years)

#ax.xaxis.set_major_formatter(date_year_format)
#ax.autoscale_view()
plt.title("Median Salary per Year")
plt.xlabel('Year')
plt.ylabel('Median Salary')
plt.tight_layout()
#plt.show()
plt.savefig('MedianPerYear.jpg')

#top 10
#filter 2023
fil2023 = (salaries["Year"] == 2023)
salaries2023 = salaries.loc[fil2023]
salaries_by_title = salaries2023.groupby("Job Title",as_index=False).median("Salary in Euro").sort_values("Salary in Euro", ascending = False).head(10)
salaries_by_title.plot.bar(x = "Job Title", y = "Salary in Euro", width = 0.9, title = "Top 10 median salary by Job Title")

#Pie chart for exp
#list for chart
srt_list = ["Entry", "Middle", "Senior", "Executive"]
experience_pie = pd.DataFrame(salaries2023["Experience Level"].value_counts(normalize=True))
experience_pie.reindex(srt_list).plot.pie(y = "proportion", title = "Experience Level in 2023", legend = True, startangle = 90, ylabel = "", counterclock = False)
