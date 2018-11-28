import pandas as pd 
from Questionaire import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import copy

N_GES = 19  #count subject


def visualize_statistics(questionaire, heuristics = False, filtered = False): #adjust for own usage
    q = questionaire.get_question_by_questionaire_nr #alias method as q

    if heuristics:
        question_5_2 = q(categoryNr = 5, questionNr = 2)
        plot_multiple_choice_question_heuristics(question_5_2)
    
        question_5_3 = q(categoryNr = 5, questionNr = 3)
        plot_multiple_choice_question_heuristics(question_5_3)

        question_6_1 = q(categoryNr = 6, questionNr = 1)
        plot_single_choice_question_heuristics_pie(question_6_1
            , labels=['... nur, wenn sie kostenlos sind.', '... auch, wenn sie kostenpflichtig sind.']
            , free_text=['hello', 'world'])

        question_6_2 = q(categoryNr = 6, questionNr = 2)
        question_6_3 = q(categoryNr = 6, questionNr = 3)
        boolvec = ~question_6_3.text_answer.isnull()
        texts = question_6_3.text_answer.values[boolvec]
        plot_multiple_choice_question_heuristics(question_6_2
            , free_text=texts
            , free_text_question=question_6_3.text)

        question_6_4 = q(categoryNr = 6, questionNr = 4)
        question_6_5 = q(categoryNr = 6, questionNr = 5)
        boolvec = ~question_6_5.text_answer.isnull()
        texts = question_6_5.text_answer.values[boolvec]
        plot_multiple_choice_question_heuristics(question_6_4
            , free_text=texts
            , free_text_question=question_6_5.text)

        question_6_6 = q(categoryNr = 6, questionNr = 6)
        question_6_7 = q(categoryNr = 6, questionNr = 7)
        boolvec = ~question_6_7.text_answer.isnull()
        texts = question_6_7.text_answer.values[boolvec]
        plot_multiple_choice_question_heuristics(question_6_6
            , free_text=texts
            , free_text_question=question_6_7.text)

    #check if people already worked scientificaly
        workedScientific = (q(categoryNr = 8, questionNr = 1).single_choice_answers==1)
        question_8_2 = q(categoryNr = 8, questionNr = 2)
        answers_8_2 = question_8_2.single_choice_answers[workedScientific].astype(int)
        plot_scala_question_heuristics_hist(question_8_2, answers_8_2
            , labels=['Sehr erfolgreich', '2', '3', '4', 'War ein Reinfall'], n=len(answers_8_2))

        question_8_3 = q(categoryNr = 8, questionNr = 3)
        answers_8_3 = question_8_3.single_choice_answers[workedScientific].astype(int)
        plot_single_choice_question_heuristics_pie(question_8_3, labels=['Abschlussarbeit', 'Studienarbeit', 'Journalartikel', 'Sonstige'])

        #statisfaction with 
        question_9_1 = q(categoryNr = 9, questionNr = 1)
        answers_9_1 = question_9_1.single_choice_answers.astype(int)
        plot_scala_question_heuristics_hist(question_9_1, answers_9_1
            , labels=['Ich fühle mich überfordert', '2', '3', '4', 'Ich komme gut klar'], n=len(answers_9_1))


    if filtered:
        workedScientific = (q(categoryNr = 8, questionNr = 1).single_choice_answers==1)
        
        question_5_2 = copy.deepcopy(q(categoryNr = 5, questionNr = 2))
        title = question_5_2.text
        question_5_2.multiple_choice_answers = question_5_2.multiple_choice_answers[workedScientific]
        plot_multiple_choice_question_heuristics(question_5_2, n=len(question_5_2.multiple_choice_answers))
        plt.title(title + '\n - Bereits wissenschaftlich gearbeitet')

        question_5_2 = copy.deepcopy(q(categoryNr = 5, questionNr = 2))
        question_5_2.multiple_choice_answers = question_5_2.multiple_choice_answers[~workedScientific]
        plot_multiple_choice_question_heuristics(question_5_2, n=len(question_5_2.multiple_choice_answers))
        plt.title(title + '\n - Noch nie wissenschaftlich gearbeitet')

        question_9_1 = q(categoryNr = 9, questionNr = 1)
        title = question_9_1.text
        answers_9_1 = question_9_1.single_choice_answers[workedScientific].astype(int)
        plot_scala_question_heuristics_hist(question_9_1, answers_9_1
            , labels=['Ich fühle mich überfordert', '2', '3', '4', 'Ich komme gut klar']
            , n=len(answers_9_1))
        plt.title(title + '\n - Bereits wissenschaftlich gearbeitet')

        question_9_1 = q(categoryNr = 9, questionNr = 1)
        answers_9_1 = question_9_1.single_choice_answers[~workedScientific].astype(int)
        plot_scala_question_heuristics_hist(question_9_1, answers_9_1
            , labels=['Ich fühle mich überfordert', '2', '3', '4', 'Ich komme gut klar']
            , n=len(answers_9_1))
        # plt.figure()
        plt.title(title + '\n - Noch nie wissenschaftlich gearbeitet')
        # plt.hist(answers_9_1, bins = [1 , 2, 3, 4, 5] )
        # plt.xticks(np.arange(15, 5.5), ['Ich fühle mich überfordert', '2', '3', '4', 'Ich komme gut klar'])
        # plt.axis([1, 6, 0, 9])

    plt.show()
    
    
    #Ideen:
    #1) Häufigkeiten der nutzung und Beschaffung von arbeiten als Tortendiagramm/Balkendiagramm
    #2) Histogramm über nutzung von Tools
    # Häufigkeiten Bereits Paper Vefasst und Noch kein Paper Vefasst -> nutzung der tools gegenüberstellen 
    # Median von Zufriedenheit mit der eigenen Vorgehensweise
    # Korrelation der Häufigkeiten der Tools mit der Zufriedenheit der Vorgehensweise?
    # Korrelation der Häufigkeiten der Tools mit Erfolg der letzten Arbeit?
    # Korrelation der Zufriedenheit der Vorgehensweise mit dem Erfolg der letzten Arbeit?




def plot_scala_question_heuristics_hist(question, vector, labels = [], bins = 5 , n = -1):
    plt.figure()
    plt.hist(vector, bins = range(1,bins + 2))
    plt.xticks(np.arange(1.5, bins+1.5), (labels))
    plt.axis([1, bins+1, 0, len(vector)])
    apply_figure_config_heuristics(question, n = n)


def plot_single_choice_question_heuristics_pie(question, labels = [], free_text = [], free_text_question = "Freitext:", n = -1):
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



def plot_multiple_choice_question_heuristics(question, subplot = False, free_text = [], free_text_question = "Freitext:", n = -1):
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
    
    apply_figure_config_heuristics(question, n=n)
    #return fig


def add_free_text_to_figure(text, ax, question_text = "Freitext:"):
    plt.subplots_adjust(bottom = len(text)/10)
    plt.text(0, 0, question_text, ha='center', va='center', transform=ax.transAxes)
    for i in range(1, len(text)+1):
        plt.text(0, -i/10, text[i-1], ha='center', va='center', transform=ax.transAxes)


def apply_figure_config_heuristics(question, n = -1):
    if n < 0:
        n = N_GES
    label = 'x gewählt (n = ' + str(n) + ')'
    plt.ylabel(label)
    apply_figure_config_all(question)
    plt.ylim(0, n)
    plt.subplots_adjust(bottom = 0.5)

 
def apply_figure_config_all(question):
    plt.xticks(rotation = 70, fontsize = 8)
    plt.title(question.text)

    


#Ergebnisse:
#1) Unterschiede zwischen beschaffung unterscheidlicher literatur aufzeigen -> Heuristiken 6.2 - 6.7
#2) Unterschiede häufigkeit Nutzung der verschiedenen Literaturarten