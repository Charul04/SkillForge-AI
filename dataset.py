import pandas as pd
import random

careers = {
    "Data Scientist": [8,8,9,3,2,7,9,5,9,2],
    "ML Engineer": [8,7,8,4,2,6,8,5,8,2],
    "Frontend Developer": [5,3,2,9,8,8,6,2,3,1],
    "Backend Developer": [7,6,4,8,2,6,8,5,4,3],
    "UI UX Designer": [3,2,1,7,10,9,5,1,2,1],
    "Cybersecurity Analyst": [5,4,3,5,2,7,9,6,4,10],
    "Cloud Engineer": [7,7,5,6,2,6,8,10,6,4],
    "Software Engineer": [7,6,6,8,3,7,8,6,5,3]
}

data = []

for career, base in careers.items():
    for _ in range(150):

        row = [
            max(1,min(10,base[i] + random.randint(-2,2)))
            for i in range(len(base))
        ]

        row.append(career)

        data.append(row)

columns = [
    "Python",
    "SQL",
    "MachineLearning",
    "WebDevelopment",
    "UIUX",
    "Communication",
    "ProblemSolving",
    "Cloud",
    "DataAnalysis",
    "CyberSecurity",
    "Career"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("large_career_dataset.csv", index=False)

print(df.head())
print(df.shape)