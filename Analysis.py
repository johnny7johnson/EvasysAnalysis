import pandas as pd 
from Questionaire import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from QuestVis import visualize_statistics

N_GES = 19  #count subject
PATH = 'data/Fragebogen_data_rare.csv'   #path to questionaire results from evasys as csv

def get_rare_data():
    data_rare = pd.read_csv(PATH, sep = ";", encoding = "ISO-8859-1", error_bad_lines = False,  na_values=['NaN', '[IMAGE]'])
    return data_rare


def split_into_questionaire(data_rare):   #central method to adjust for other questionaires
    data_agreement = data_rare.loc[data_rare.iloc[:, 1] == 1] #check if user agreed to dataprocessing
    data = data_agreement.iloc[:,3:58] #just data without id, timestamp, etc. 
    
    #split dataframe into categories
    cat3 = data_agreement.iloc[:, 3:5] #iloc last indes of [x:y] statement (y) is not included -> cat 3 includes indices 3 and 4
    cat4 = data_agreement.iloc[:, 5:7]
    cat5 = data_agreement.iloc[:, 7:17] 
    cat6 = data_agreement.iloc[:, 17:39] 
    cat7 = data_agreement.iloc[:, 39:53] 
    cat8 = data_agreement.iloc[:, 53:56] 
    cat9 = data_agreement.iloc[:, 56] 
    cat10 = data_agreement.iloc[:, 57]

    #Split categories into questions and group them
    cat3_q1 = Question(text = cat3.columns.values[0], s_c_answers=cat3.iloc[:, 0], answer_range_start=1, answer_range_end=2)
    cat3_q2 = Question(text = cat3.columns.values[1], s_c_answers=cat3.iloc[:, 1], answer_range_start=1, answer_range_end=2)
    cat3_quests = [cat3_q1, cat3_q2]

    cat4_q1 = Question(text = cat4.columns.values[0], s_c_answers=cat4.iloc[:, 0], answer_range_start=1, answer_range_end=2)
    cat4_q2 = Question(text = cat4.columns.values[1], t_answer=cat4.iloc[:, 1])
    cat4_quests = [cat4_q1, cat4_q2]

    cat5_q1 = Question(text = cat5.columns.values[0], s_c_answers=cat5.iloc[:, 0], answer_range_start=1, answer_range_end=5) #scala
    cat5_q2 = Question(text = "Welche Arten von Arbeiten werden benötigt?" , multiple_choice = True, m_c_answers=cat5.iloc[:, 1:6]) 
    cat5_q3 = Question(text = "Wozu werden die Arbeiten genutzt?" , multiple_choice = True, m_c_answers=cat5.iloc[:, 6:10]) 
    cat5_quests = [cat5_q1, cat5_q2, cat5_q3]

    cat6_q1 = Question(text = cat6.columns.values[0], s_c_answers=cat6.iloc[:, 0], answer_range_start=1, answer_range_end=2)
    cat6_q2 = Question(text = "Ich beschaffe mir Bücher, die ich benötige …" , multiple_choice = True
        , m_c_answers=cat6.iloc[:, 1:7]) 
    cat6_q3 = Question(text = cat6.columns.values[7], t_answer=cat6.iloc[:, 7])
    cat6_q4 = Question(text = "Ich beschaffe mir wissenschaftliche Paper, die ich benötige …" , multiple_choice = True
        , m_c_answers=cat6.iloc[:, 8:14]) 
    cat6_q5 = Question(text = cat6.columns.values[14], t_answer=cat6.iloc[:, 14])
    cat6_q6 = Question(text = "Ich beschaffe mir Zeitschrifen (CT, Chip, o.ä.), die ich benötige …" , multiple_choice = True
        , m_c_answers=cat6.iloc[:, 15:21]) 
    cat6_q7 = Question(text = cat6.columns.values[21], t_answer=cat6.iloc[:, 21])
    cat6_quests = [cat6_q1, cat6_q2, cat6_q3, cat6_q4, cat6_q5, cat6_q6, cat6_q7]
    
    cat7_q1 = Question(text = "Ich erfahre von den Arbeiten, die ich nutze …" , multiple_choice = True
        , m_c_answers=cat7.iloc[:, 0:6]) 
    cat7_q2 = Question(text = cat7.columns.values[6], t_answer=cat7.iloc[:, 6])
    cat7_q3 = Question(text = "Wenn ich im Internet nach wissenschaftlichen Arbeiten recherchiere, nutze ich dafür …." , multiple_choice = True
        , m_c_answers=cat7.iloc[:, 7:13])
    cat7_q4 = Question(text = cat7.columns.values[13], t_answer=cat7.iloc[:, 13])
    cat7_quests = [cat7_q1, cat7_q2, cat7_q3, cat7_q4]

    cat8_q1 = Question(text = cat8.columns.values[0], s_c_answers=cat8.iloc[:, 0], answer_range_start=1, answer_range_end=2)
    cat8_q2 = Question(text = cat8.columns.values[1], s_c_answers=cat8.iloc[:, 1], answer_range_start=1, answer_range_end=5) #scala
    cat8_q3 = Question(text = cat8.columns.values[2], s_c_answers=cat8.iloc[:, 2], answer_range_start=1, answer_range_end=4)
    cat8_quests = [cat8_q1, cat8_q2, cat8_q3]

    cat9_q1 = Question(text = cat9.name, s_c_answers=cat9, answer_range_start=1, answer_range_end=5) #scala
    cat9_quests = [cat9_q1]

    cat10_q1 = Question(text = cat10.name, t_answer=cat10) 
    cat10_quests = [cat10_q1]

    #insert into questionaire
    catlist = [Category(questions=cat3_quests), Category(questions=cat4_quests), Category(questions=cat5_quests)
        , Category(questions=cat6_quests), Category(questions=cat7_quests), Category(questions=cat8_quests)
        , Category(questions=cat9_quests), Category(questions=cat10_quests)]

    questionaire = Questionaire(categories = catlist)

    return questionaire


def normalize_questionaire(questionaire):
    #z-transforamtion or normalization to [0 ... 1] (Prozentrangbildung?)
    for cat in questionaire.categories:
        quests = cat.questions;
        for quest in quests:
            quest.normalize_answers();
    #TODO: just normalize values that must be normalized
    return questionaire


def calc_statistics():
    #TODO
    return None




def main():
    data_rare = get_rare_data()
    splitted = split_into_questionaire(data_rare)
    print(splitted.categories[0].get_questions())
    # normalized = normalize_questionaire(splitted)
    # print(normalized.categories[0].get_questions())
    visualize_statistics(splitted, filtered=True, heuristics=False)


if __name__ == "__main__":
    main()
