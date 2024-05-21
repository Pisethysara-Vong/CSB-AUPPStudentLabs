import pandas as pd
from urllib.request import urlopen
import datetime


class SchoolAssessmentAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame()

    def process_file(self, file_path):
        # Open and read the content of the file
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            self.data = pd.read_excel(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                # Custom logic to process plain text file
                self.data = file.read()

    def transfer_data(self, source_file, destination_file):
        # Transfer data based on predefined criteria
        if source_file.endswith('.csv') and destination_file.endswith('.csv'):
            frames = [pd.read_csv(source_file), pd.read_csv(destination_file)]
            self.merged_file= pd.concat(frames, ignore_index=True)
        elif source_file.endswith('.xlsx') and destination_file.endswith('.xlsx'):
            frames = [pd.read_excel(source_file), pd.read_excel(destination_file)]
            self.merged_file = pd.concat(frames, ignore_index=True)
        else:
            return f'An error has occurred. Please check both of your files to see if there were any problems.'
        return self.merged_file

    def fetch_web_data(self, url):
        # Fetch data from school webpage using urlopen
        with urlopen(url) as response:
            # Custom logic to extract relevant information from the webpage
            self.response = response.read()

    def analyze_content(self, filename):
        # Custom logic to analyze assessment data (e.g., calculate averages, identify trends)
        self.process_file(filename)

        self.data['Total_score'] = self.data[['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']].sum(axis=1)
        TotalScore = self.data[['INF 652', 'CSC 241', 'ITM 101', 'ITM 371', 'COSC 201']].sum()
        self.average = TotalScore.mean()/self.data['Name'].count()
        self.Total_avg = TotalScore.mean()/5

        if self.average < 90:
            self.rec = ('Survey the students on whether or not the courses was too hard or were there any other '
                        'problems with the courses.')
        else:
            self.rec = "No recommendations."

        if self.average >= 90:
            self.note = "Most of the students got an A in each course."
        elif self.average >= 80:
            self.note = "Most of the students got a B in each course."
        elif self.average >= 70:
            self.note = "Most of the students got a C in each course."

        self.top_scorer = self.data.nlargest(3, 'Total_score')
        self.topScorerDict = self.top_scorer[['Name', 'Total_score']].to_dict(orient='records')
        self.top_25 = self.data.nlargest(25, 'Total_score')
        self.top25Dict = self.top_25[['Semester', 'Total_score']].to_dict(orient='records')

        counterSumm = 0
        counterSpring = 0
        counterFall = 0
        for i in range(25):
            items = self.top25Dict[i]['Semester']
            if items == 'Summer':
                counterSumm += 1
            elif items == 'Spring':
                counterSpring += 1
            elif items == 'Fall':
                counterFall += 1

        highest_counter = max(counterFall, counterSumm, counterSpring)
        if counterSpring == highest_counter:
            self.freq_list = ['Spring', f'{highest_counter}']
        elif counterFall == highest_counter:
            self.freq_list = ['Fall', f'{highest_counter}']
        elif counterSumm == highest_counter:
            self.freq_list = ['Summer', f'{highest_counter}']

        if self.freq_list[1] >= '10':
            self.rec2 = '-Survey the students on whether or not the semester that they study in, affects their grades.'
        elif self.freq_list[1] >= '10' and self.average < 90:
            self.rec2 = ''
        else:
            self.rec2 = "No recommendations."


        self.AvgScoreINF = sum(self.data['INF 652'])/self.data['Name'].count()
        self.AvgScoreCSC = sum(self.data['CSC 241'])/self.data['Name'].count()
        self.AvgScoreITM101 = sum(self.data['ITM 101'])/self.data['Name'].count()
        self.AvgScoreITM371 = sum(self.data['ITM 371'])/self.data['Name'].count()
        self.AvgScoreCOSC = sum(self.data['COSC 201'])/self.data['Name'].count()
        
        maximum = max(self.AvgScoreINF, self.AvgScoreCSC, self.AvgScoreITM101, self.AvgScoreITM371, self.AvgScoreCOSC)
        minimum = min(self.AvgScoreINF, self.AvgScoreCSC, self.AvgScoreITM101, self.AvgScoreITM371, self.AvgScoreCOSC)

        if maximum == self.AvgScoreINF:
            self.highest_avg_course = ['INF 652', f'{round(maximum,2)}']

        elif maximum == self.AvgScoreCSC:
            self.highest_avg_course = ['CSC 241', f'{round(maximum,2)}']
            
        elif maximum == self.AvgScoreITM101:
            self.highest_avg_course = ['ITM 101', f'{round(maximum,2)}']
            
        elif maximum == self.AvgScoreITM371:
            self.highest_avg_course = ['ITM 371', f'{round(maximum,2)}']
            
        elif maximum == self.AvgScoreCOSC:
            self.highest_avg_course = ['COSC 201', f'{round(maximum,2)}']

        if minimum == self.AvgScoreINF:
            self.lowest_avg_course = ['INF 652', f'{round(minimum, 2)}']

        elif minimum == self.AvgScoreCSC:
            self.lowest_avg_course = ['CSC 241', f'{round(minimum, 2)}']

        elif minimum == self.AvgScoreITM101:
            self.lowest_avg_course = ['ITM 101', f'{round(minimum, 2)}']

        elif minimum == self.AvgScoreITM371:
            self.lowest_avg_course = ['ITM 371', f'{round(minimum, 2)}']

        elif minimum == self.AvgScoreCOSC:
            self.lowest_avg_course = ['COSC 201', f'{round(minimum, 2)}']

        self.web_data = pd.read_csv('web log.csv')
        self.avg_time = sum(self.web_data['Time Spent'])/self.web_data['Name'].count()

    def generate_summary(self):
        # Generate summary for the school principal
        # Include key insights, trends, and areas of improvement
        print("School Assessment Summary Report\n")
        print(f"""1. Overall Performance of Students:
    -Average score in each course for each student:{self.average}
    -Top performing Students: 1. {self.topScorerDict[0]['Name']}, Total Score:{self.topScorerDict[0]['Total_score']}
                              2. {self.topScorerDict[1]['Name']}, Total Score:{self.topScorerDict[1]['Total_score']}
                              3. {self.topScorerDict[2]['Name']}, Total Score:{self.topScorerDict[2]['Total_score']}\n
2. Subject Wise Analysis:
    -Out of all the courses, students performs the best in {self.highest_avg_course[0]} with a an Average Score of:{self.highest_avg_course[1]}
    -Out of all the courses, students performs the worst in {self.lowest_avg_course[0]} with an Average Score of:{self.lowest_avg_course[1]}\n
3. Notable Observations:
    -{self.note}
    -Among the top 25 students, {self.freq_list[1]} students study in the {self.freq_list[0]} semester.\n
4. Webdata Insights:
    -Students spent an average time of {self.avg_time:.2f} minutes on the Web page.\n
5. Recommendations:
    -{self.rec}
    {self.rec2}

Reported Generated on: {datetime.date.today()}""")


analyzer = SchoolAssessmentAnalyzer()

merged_file = analyzer.transfer_data('Spring (1).csv', 'fall.csv')

analyzer.analyze_content('all_semester.csv')

analyzer.generate_summary()

# Analyze content & display result area
# Sample of Output:
"""
School Assessment Summary Report:

1. Overall Performance of Student A:
   - Average score: 85.5
   - Top-performing class: Grade 10B

2. Subject-wise Analysis:
   - Mathematics: Improved by 10% compared to the last assessment.
   - Science: Consistent performance across all classes.

3. Notable Observations:
   - Grade 8A shows a significant improvement in English proficiency.

4. Web Data Insights:
   - Online participation: 95% of students accessed assessment resources online.

5. Recommendations:
   - Consider additional support for Grade 9B in Mathematics.

Report generated on: 2024-01-14
"""
