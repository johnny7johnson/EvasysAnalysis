import pandas as pd 
from Questionaire import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

N_GES = 19  #count subject


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

    question_6_4 = questionaire.get_question_by_questionaire_nr(categoryNr = 6, questionNr = 4)
    question_6_5 = questionaire.get_question_by_questionaire_nr(categoryNr = 6, questionNr = 5)
    boolvec = ~question_6_5.text_answer.isnull()
    texts = question_6_5.text_answer.values[boolvec]
    plot_multiple_choice_question_heuristics(question_6_4
        , free_text=texts
        , free_text_question=question_6_5.text)

    question_6_6 = questionaire.get_question_by_questionaire_nr(categoryNr = 6, questionNr = 6)
    question_6_7 = questionaire.get_question_by_questionaire_nr(categoryNr = 6, questionNr = 7)
    boolvec = ~question_6_7.text_answer.isnull()
    texts = question_6_7.text_answer.values[boolvec]
    plot_multiple_choice_question_heuristics(question_6_6
        , free_text=texts
        , free_text_question=question_6_7.text)

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

    
