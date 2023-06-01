import pandas as pd
import sys
from matplotlib import pyplot as plt
from matplotlib import axis as axis
from matplotlib import dates as mpl_dates
import matplotlib.ticker as ticker
colors = ["#AC3E31", "#484848", "#DBAE58", "#DADADA", "#20283E", "#488A99"]


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
plt.bar(x, y, color = colors[0])

plt.title("Median Salary per Year")
plt.xlabel('Year')
plt.ylabel('Median Salary')
plt.tight_layout()
#plt.show()
plt.savefig('MedianPerYear.jpg')
plt.close()
#top 10
#filter 2023
fil2023 = (salaries["Year"] == 2023)
salaries2023 = salaries.loc[fil2023]
salaries_by_title = salaries2023.groupby("Job Title",as_index=False).median("Salary in Euro").sort_values("Salary in Euro", ascending = False).head(10)
salaries_by_title.plot.bar(x = "Job Title", y = "Salary in Euro", width = 0.9, title = "Top 10 median salary by Job Title",color = colors[0])

#Pie chart for exp
#list for chart
srt_list = ["Entry", "Middle", "Senior", "Executive"]
experience_pie = pd.DataFrame(salaries2023["Experience Level"].value_counts(normalize=True))
experience_pie.reindex(srt_list).plot.pie(y = "proportion", title = "Experience Level in 2023", legend = True, startangle = 90, ylabel = "", counterclock = False,colors = colors)

#salary by experience level
salary_experience = salaries2023.groupby(by="Experience Level",as_index=False)[["Experience Level", "Salary in Euro"]].median("Salary in Euro")
salary_experience["Experience Level"] = salary_experience["Experience Level"].astype("category")
salary_experience["Experience Level"] = salary_experience["Experience Level"].cat.as_ordered()
salary_experience["Experience Level"] = salary_experience["Experience Level"].cat.set_categories(srt_list)

salary_experience.sort_values("Experience Level").plot.bar(x = "Experience Level", y = "Salary in Euro", title = "Salary by experience Level", color = colors)
plt.show()
#salary trend per year
salaries_year = salaries.groupby(by=["Year", "Experience Level"], as_index=False)[["Year", "Experience Level", "Salary in Euro"]].median("Salary in Euro")
salaries_year["Experience Level"] = salaries_year["Experience Level"].astype("category")
salaries_year["Experience Level"] = salaries_year["Experience Level"].cat.as_ordered()
salaries_year["Experience Level"] = salaries_year["Experience Level"].cat.set_categories(srt_list)

# salaries_year.sort_values("Experience Level").plot.bar(x = "Year", y = ["Experience Level", "Salary in Euro"], title = "Salary by experience Level", color = colors)

x = salaries_year["Year"].unique().astype(int)
#y2020 = salaries_year.loc[salaries_year["Year"] == 2020].set_index("Experience Level")
y2021 = salaries_year.loc[salaries_year["Year"] == 2021].set_index("Experience Level").reindex(srt_list)
y2022 = salaries_year.loc[salaries_year["Year"] == 2022].set_index("Experience Level").reindex(srt_list)
y2023 = salaries_year.loc[salaries_year["Year"] == 2023].set_index("Experience Level").reindex(srt_list)
#plt.bar(x - 0.3 , y2020["Salary in Euro"], width = 0.2)
plt.bar(x - 0.2, y2021["Salary in Euro"], width = 0.2, color= colors[0])
plt.bar(x, y2022["Salary in Euro"], width = 0.2,color= colors[1])
plt.bar(x  + 0.2, y2023["Salary in Euro"], width = 0.2,color= colors[2] )

plt.tight_layout()

plt.xticks(ticks=[2020,2021,2022,2023], labels=["Entry","Middle","Senior","Executive"])
plt.legend(['2021','2022','2023' ])
# plt.set_major_locator(ticker.MaxNLocator(integer=True))
plt.show()
# salaries_year.sort_values("Experience Level").plot.bar(x = "Year" , y = "Salary in Euro", title = "Salary by experience Level", color = colors)
