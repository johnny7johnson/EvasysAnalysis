import pandas as pd 
from Questionaire import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

N_GES = 19  #count subject
PATH = 'data/Fragebogen_data_rare.csv'   #path to questionaire results from evasys as csv

def get_rare_data():
    data_rare = pd.read_csv(PATH, sep = ";", encoding = "ISO-8859-1", error_bad_lines = False,  na_values=['NaN', '[IMAGE]'])
    return data_rare


def split_into_questionaire(data_rare):   #central method to adjust for other questionaires
    data_agreement = data_rare.loc[data_rare.iloc[:, 1] == 1] #check if user agreed to dataprocessing
    data = data_agreement.iloc[:,3:58] #just data without id, timestamp, etc. 
    
    #split into categories
    cat3 = data_agreement.iloc[:, 3:5] #iloc last indes of [x:y] statement (y) is not included -> cat 3 includes indices 3 and 4
    cat4 = data_agreement.iloc[:, 5:7]
    cat5 = data_agreement.iloc[:, 7:17] 
    cat6 = data_agreement.iloc[:, 17:39] 
    cat7 = data_agreement.iloc[:, 39:53] 
    cat8 = data_agreement.iloc[:, 53:56] 
    cat9 = data_agreement.iloc[:, 56] 
    cat10 = data_agreement.iloc[:, 57]

    #Split categories into questions
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


def visualize_statistics(questionaire): #adjust for own usage
    question_5_2 = questionaire.get_question_by_questionaire_nr(categoryNr = 5, questionNr = 2)
    plot_multiple_choice_question_heuristics(question_5_2)
    
    question_5_3 = questionaire.get_question_by_questionaire_nr(categoryNr = 5, questionNr = 3)
    plot_multiple_choice_question_heuristics(question_5_3)

    question_6_1 = questionaire.get_question_by_questionaire_nr(categoryNr = 6, questionNr = 1)
    plot_single_choice_question_heuristics(question_6_1
        , labels=['... nur, wenn sie kostenlos sind.', '... auch, wenn sie kostenpflichtig sind.']
        , free_text=['hello', 'world'])

    question_6_2 = questionaire.get_question_by_questionaire_nr(categoryNr = 6, questionNr = 2)
    question_6_3 = questionaire.get_question_by_questionaire_nr(categoryNr = 6, questionNr = 3)
    boolvec = ~question_6_3.text_answer.isnull()
    texts = question_6_3.text_answer.values[boolvec]
    plot_multiple_choice_question_heuristics(question_6_2
        , free_text=texts
        , free_text_question=question_6_3.text)

    plt.show()
    
    
    #Ideen:
    #1) Häufigkeiten der nutzung und Beschaffung von arbeiten als Tortendiagramm/Balkendiagramm
    #2) Histogramm über nutzung von Tools
    # Häufigkeiten Bereits Paper Vefasst und Noch kein Paper Vefasst -> nutzung der tools gegenüberstellen 
    # Median von Zufriedenheit mit der eigenen Vorgehensweise
    # Korrelation der Häufigkeiten der Tools mit der Zufriedenheit der Vorgehensweise?
    # Korrelation der Häufigkeiten der Tools mit Erfolg der letzten Arbeit?
    # Korrelation der Zufriedenheit der Vorgehensweise mit dem Erfolg der letzten Arbeit?

    return None
    

def plot_single_choice_question_heuristics(question, labels = [], free_text = [], free_text_question = "Freitext:"):
    y = []
    start = question.answer_range_start
    end = question.answer_range_end
        
    for value in range(start, end + 1):
        count_occurence = (question.single_choice_answers == value).sum();
        y.append(count_occurence)

    if len(labels) is 0:
        labels = range(start, end + 1)
    fig1, ax1 = plt.subplots()
    ax1.pie(y, startangle=90, labels = labels)
    ax1.axis('equal') 

    if len(free_text) is not 0:
        add_free_text_to_figure(free_text, ax1)


    apply_figure_config_all(question)



def plot_multiple_choice_question_heuristics(question, subplot = False, free_text = [], free_text_question = "Freitext:"):
    answers = question.multiple_choice_answers
    x = answers.columns.values
    y = []
    for nr in range(0, answers.shape[1]):
        ans = answers.iloc[:, nr].values
        #y.append(ans.count("1"))
        count_ones_occurence = (ans == 1).sum();
        y.append(count_ones_occurence)
    
    if subplot is False:
        fig, ax1 = plt.subplots();
    else:
        fig, ax1 = plt.subplot(2, 2, 1);
    plt.bar(x, y) 

    if len(free_text) is not 0:
        add_free_text_to_figure(free_text, ax1)
    
    apply_figure_config_heuristics(question)
    #return fig


def add_free_text_to_figure(text, ax, question_text = "Freitext:"):
    if len(text) >= 10:
        plt.subplots_adjust(bottom = 0.9)
    else:
        plt.subplots_adjust(bottom = len(text)/10)
    plt.text(0, 0, question_text, ha='center', va='center', transform=ax.transAxes)
    for i in range(1, len(text)+1):
        plt.text(0, -i/10, text[i-1], ha='center', va='center', transform=ax.transAxes)
        plt.text(0, -i/10, text[i-1], ha='center', va='center', transform=ax.transAxes)


def apply_figure_config_heuristics(question):
    label = 'x gewählt (n = ' + str(N_GES) + ')'
    plt.ylabel(label)
    apply_figure_config_all(question)
    plt.ylim(0, N_GES)
    plt.subplots_adjust(bottom = 0.5)


def apply_figure_config_all(question):
    plt.xticks(rotation = 70, fontsize = 8)
    plt.title(question.text)

    



def main():
    data_rare = get_rare_data()
    splitted = split_into_questionaire(data_rare)
    print(splitted.categories[0].get_questions())
    # normalized = normalize_questionaire(splitted)
    # print(normalized.categories[0].get_questions())
    visualize_statistics(splitted)


if __name__ == "__main__":
    main()
