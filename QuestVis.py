import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import copy
from Questionaire import *

N_GES = 19  #count subject


def visualize_statistics(questionaire, heuristics = False, filtered = False): #adjust for own usage
    q = questionaire.get_question_by_questionaire_nr #alias method as q

    if heuristics:
        question_5_1 = q(categoryNr = 5, questionNr = 1)
        answers_5_1 = question_5_1.single_choice_answers.astype(int)
        plot_scala_question_heuristics_hist(question_5_1, answers_5_1
            , labels=['Sehr häufig', '2', '3', '4', 'Fast nie'], n=len(answers_5_1))
        
        question_5_2 = q(categoryNr = 5, questionNr = 2)
        plot_multiple_choice_question_heuristics_bar(question_5_2)
    
        question_5_3 = q(categoryNr = 5, questionNr = 3)
        plot_multiple_choice_question_heuristics_bar(question_5_3)

        question_6_1 = q(categoryNr = 6, questionNr = 1)
        plot_single_choice_question_heuristics_pie(question_6_1
            , labels=['... nur, wenn sie kostenlos sind.', '... auch, wenn sie kostenpflichtig sind.']
            , free_text=['hello', 'world'])

        question_6_2 = q(categoryNr = 6, questionNr = 2)
        question_6_3 = q(categoryNr = 6, questionNr = 3)
        boolvec = ~question_6_3.text_answer.isnull()
        texts = question_6_3.text_answer.values[boolvec]
        plot_multiple_choice_question_heuristics_bar(question_6_2
            , free_text=texts
            , free_text_question=question_6_3.text)

        question_6_4 = q(categoryNr = 6, questionNr = 4)
        question_6_5 = q(categoryNr = 6, questionNr = 5)
        boolvec = ~question_6_5.text_answer.isnull()
        texts = question_6_5.text_answer.values[boolvec]
        plot_multiple_choice_question_heuristics_bar(question_6_4
            , free_text=texts
            , free_text_question=question_6_5.text)

        question_6_6 = q(categoryNr = 6, questionNr = 6)
        question_6_7 = q(categoryNr = 6, questionNr = 7)
        boolvec = ~question_6_7.text_answer.isnull()
        texts = question_6_7.text_answer.values[boolvec]
        plot_multiple_choice_question_heuristics_bar(question_6_6
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
        plot_multiple_choice_question_heuristics_bar(question_5_2, n=len(question_5_2.multiple_choice_answers))
        plt.title(title + '\n - Bereits wissenschaftlich gearbeitet')

        question_5_2 = copy.deepcopy(q(categoryNr = 5, questionNr = 2))
        question_5_2.multiple_choice_answers = question_5_2.multiple_choice_answers[~workedScientific]
        plot_multiple_choice_question_heuristics_bar(question_5_2, n=len(question_5_2.multiple_choice_answers))
        plt.title(title + '\n - Noch nie wissenschaftlich gearbeitet')

        #boxplot 
        plot_grouped_scala_distribution_boxplot(q(categoryNr = 9, questionNr = 1), workedScientific, 
            group_labels_vector=["Noch nie wissenschaftlich gearbeitet", "Bereits wissenschaftlich gearbeitet"] 
            ,scala_max_label="Ich komme gut klar.")


        #split into 2+3 (often) and 4+5 (rare)
        question_5_1 = q(categoryNr = 5, questionNr = 1)
        answers_5_1 = question_5_1.single_choice_answers
        answers_5_1[answers_5_1 == 2] = 'oft'
        answers_5_1[answers_5_1 == 3] = 'oft'
        answers_5_1[answers_5_1 == 4] = 'selten'
        answers_5_1[answers_5_1 == 5] = 'selten'
        question_6_1 = q(categoryNr = 6, questionNr = 1)
        answers_6_1 = question_6_1.single_choice_answers
        answers_6_1[answers_6_1 == 1] = 'nur wenn kostenlos'
        answers_6_1[answers_6_1 == 2] = 'auch wenn kostenpflichtig'
        #answers_6_1[5] = "trolololo"

        plot_cross_table_bar(answers_6_1, answers_5_1, question_6_1, question_5_1, custom_color_label="Häufigkeit der Nutzung")


        #split into 2+3 (often) and 4+5 (rare)
        question_5_1 = q(categoryNr = 5, questionNr = 1)
        answers_5_1 = question_5_1.single_choice_answers
        answers_5_1[answers_5_1 == 2] = 'oft'
        answers_5_1[answers_5_1 == 3] = 'oft'
        answers_5_1[answers_5_1 == 4] = 'selten'
        answers_5_1[answers_5_1 == 5] = 'selten'
        question_5_2 = q(categoryNr = 5, questionNr = 2)

        plot_grouped_multiple_choice_percentages(question_5_2, answers_5_1, question_5_1, custom_groups_label="Häufigkeit der Nutzung")
        

        question_8_1 =  q(categoryNr = 8, questionNr = 1)
        answers_8_1 = question_8_1.single_choice_answers
        answers_8_1[answers_8_1 == 1] = 'Ja'
        answers_8_1[answers_8_1 == 2] = 'Nein'

        plot_grouped_multiple_choice_percentages(question_5_2, answers_8_1, question_8_1, custom_groups_label="Bereits wissenschaftlich gearbeitet")


        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        plot_grouped_multiple_choice_percentages(q(categoryNr = 6, questionNr = 2), answers_5_1, question_5_1, custom_groups_label="Häufigkeit der Nutzung")

        q_6_2_ans = q(categoryNr = 6, questionNr = 2).multiple_choice_answers
        # q_6_2_ans = q_6_2_ans.rename(index=str, columns={ q_6_2_ans.columns.values[0]:q_6_2_ans.columns.values[0]
        #     , q_6_2_ans.columns.values[1]: q_6_2_ans.columns.values[1], q_6_2_ans.columns.values[2]: q_6_2_ans.columns.values[2]
        #     , q_6_2_ans.columns.values[3]: q_6_2_ans.columns.values[3], q_6_2_ans.columns.values[4]:q_6_2_ans.columns.values[4]
        #     , q_6_2_ans.columns.values[5]: q_6_2_ans.columns.values[5]})

        q_6_4_ans = q(categoryNr = 6, questionNr = 4).multiple_choice_answers
        q_6_4_ans = q_6_4_ans.rename(index=str, columns={ q_6_4_ans.columns.values[0]:q_6_2_ans.columns.values[0]
            , q_6_4_ans.columns.values[1]: q_6_2_ans.columns.values[1], q_6_4_ans.columns.values[2]: q_6_2_ans.columns.values[2]
            , q_6_4_ans.columns.values[3]: q_6_2_ans.columns.values[3], q_6_4_ans.columns.values[4]:q_6_2_ans.columns.values[4]
            , q_6_4_ans.columns.values[5]: q_6_2_ans.columns.values[5]})

        q_6_6_ans = q(categoryNr = 6, questionNr = 6).multiple_choice_answers
        q_6_6_ans = q_6_6_ans.rename(index=str, columns={ q_6_6_ans.columns.values[0]:q_6_2_ans.columns.values[0]
            , q_6_6_ans.columns.values[1]: q_6_2_ans.columns.values[1], q_6_6_ans.columns.values[2]: q_6_2_ans.columns.values[2]
            , q_6_6_ans.columns.values[3]: q_6_2_ans.columns.values[3], q_6_6_ans.columns.values[4]:q_6_2_ans.columns.values[4]
            , q_6_6_ans.columns.values[5]: q_6_2_ans.columns.values[5]})

        #generate group
        #literatur_group = np.zeros(q_6_2.multiple_choice_answers.shape[0])
        literatur_group = np.full(q_6_2_ans.shape[0], 'Bücher')
        g = np.full(q_6_4_ans.shape[0], 'Wissenschaftliche Paper')
        literatur_group = np.concatenate((literatur_group, g), axis=None)
        literatur_group = np.concatenate((literatur_group, np.full(q_6_6_ans.shape[0], 'Zeitschriften (CT, Chip, o.ä.)')),axis=None)
        q_6_4_ans.index = q_6_2_ans.index +q_6_2_ans.shape[0]
        q_6_6_ans.index = q_6_4_ans.index +q_6_2_ans.shape[0]+ q_6_4_ans.shape[0]
        
        answers = [q_6_2_ans, q_6_4_ans ,q_6_6_ans]
        
        all = pd.concat(answers)
        #all = q_6_2_ans.append(q_6_4_ans.append(q_6_6_ans))
        dummyQuestion = q(categoryNr = 6, questionNr = 2)
        dummyQuestion.multiple_choice_answers = all
        dummyQuestion.text = "Ich beschaffe mir Bücher, wisschenschaftliche Paper oder Zeitschriften ... "
        plot_grouped_multiple_choice_percentages(dummyQuestion, literatur_group, Question(), custom_title = "Ich beschaffe mir Bücher, wisschenschaftliche Paper oder Zeitschriften ... ")



    plt.show()
    
    
    #Ideen:
    #1) Häufigkeiten der nutzung und Beschaffung von arbeiten als Tortendiagramm/Balkendiagramm
    #2) Histogramm über nutzung von Tools
    # Häufigkeiten Bereits Paper Vefasst und Noch kein Paper Vefasst -> nutzung der tools gegenüberstellen 
    # Median von Zufriedenheit mit der eigenen Vorgehensweise
    # Korrelation der Häufigkeiten der Tools mit der Zufriedenheit der Vorgehensweise?
    # Korrelation der Häufigkeiten der Tools mit Erfolg der letzten Arbeit?
    # Korrelation der Zufriedenheit der Vorgehensweise mit dem Erfolg der letzten Arbeit?

# *************************************************************************************************************************
# ******************************************* Plot functions **************************************************************
# *************************************************************************************************************************


#   ********************************************************************
#    Grouped single choice answers as boxplot as distribution.
#    Only 2 Groups supported.  
#   *******************************************************************
def plot_grouped_scala_distribution_boxplot(scala_question, group_binary_vector, group_labels_vector = [], scala_max_label = "gut"):
    answers_group_a = scala_question.single_choice_answers[~group_binary_vector].astype(int)
    answers_group_b = scala_question.single_choice_answers[group_binary_vector].astype(int)
    
    plt.figure()
    plt.boxplot([answers_group_a, answers_group_b])
    plt.xticks([1, 2], group_labels_vector)
    plt.subplots_adjust(bottom = 0.5)
    plt.ylabel("Zufriedenheit. \n5 = " + scala_max_label)

    apply_figure_config_all(scala_question)
    


#   ********************************************************************
#    Grouped multiple choice answers as barplot as percent. 
#    Groups as colors. Anwers as bar label. 
#   *******************************************************************
def plot_grouped_multiple_choice_percentages(m_c_question, groups, group_question, custom_groups_label = "", custom_title = ""):
    countedGroups = []
    groupsizes = []
    for group in np.unique(groups):
        indices_of_group = [i for i, x in enumerate(groups == group) if x]
        filtered = m_c_question.multiple_choice_answers.iloc[indices_of_group, :]
        groupsize = len(filtered)
        heuristics = []
        for nr in range(0, m_c_question.multiple_choice_answers.shape[1]):
            ans = filtered.iloc[:, nr].values
            count_ones_occurence = (ans == 1).sum();
            percentages = count_ones_occurence/groupsize*100
            heuristics.append(percentages)
        countedGroups.append(heuristics)
        groupsizes.append(groupsize)

    #bis hier hin gut :)

    colors=['cornflowerblue','darkorange','c','r','g']
    # set width of bar
    barWidth = (1-0.2)/len(np.unique(groups))
    
    rs = []
    r0 = np.arange(len(countedGroups[0]))
    r = r0
    rs.append(r0)

    maxgroups = len(np.unique(groups))
    for num in range(1, maxgroups):
        r_new = [x + barWidth for x in r]
        rs.append(r_new)
        r = r_new
    
    fig, ax = plt.subplots()
    for num in range(0, maxgroups):
        label = "" + str(np.unique(groups)[num]) + " (n = " + str(groupsizes[num]) + " )"
        plt.bar(rs[num], countedGroups[num], color=colors[num], width=barWidth, edgecolor='white', label=label)


    plt.xticks([r[0]-0.25 + barWidth for r[0] in range(len(countedGroups[0]))], m_c_question.multiple_choice_answers.columns.values)
    apply_figure_config_heuristics(m_c_question, n=100)
    if len(custom_title) is 0:
        custom_title = "Unterschied zwischen \n'" +m_c_question.text + "'\n UND \n'" + group_question.text + "'"
    plt.title(custom_title)
    plt.xlabel(m_c_question.text)
    plt.ylabel('% ausgewählt')
    l = ax.legend()
    if len(custom_groups_label) is not 0:
        l.set_title(custom_groups_label)



#   ********************************************************************
#    Grouped single choice answers as barplot as percent. 
#    Groups as colors. Anwers as bar label. 
#   *******************************************************************
def plot_cross_table_bar(x_hist, y_hist, group_bars_question, group_color_question, custom_color_label = ""):

    df = pd.DataFrame({'colors':y_hist,'bars':x_hist}) #how many values has y?
    ct = pd.crosstab(df.bars, df.colors)
    print(ct)
    stacked = ct.stack().reset_index().rename(columns={0:'value'})

    fig, ax = plt.subplots()
    sns.barplot(x=stacked.bars, y=stacked.value, hue=stacked.colors)
    #TODO: manage on multiplechoice answers
    plt.xlabel(group_bars_question.text)
    l = ax.legend()
    l.set_title(custom_color_label)
    plt.title("Unterschied zwischen \n'" +group_bars_question.text + "'\n UND \n'" + group_color_question.text + "'")

    #https://stackoverflow.com/questions/43544694/using-pandas-crosstab-with-seaborn-stacked-barplots



#   ********************************************************************
#    Heuristics of Scala questions as histogram.  
#   *******************************************************************
def plot_scala_question_heuristics_hist(question, vector, labels = [], bins = 5 , n = -1):
    plt.figure()
    plt.hist(vector, bins = range(1,bins + 2))
    plt.xticks(np.arange(1.5, bins+1.5), (labels))
    plt.axis([1, bins+1, 0, len(vector)])
    apply_figure_config_heuristics(question, n = n)


#   ********************************************************************
#    Single Choice answers as pie plot in percent. 
#   *******************************************************************
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
    ax1.pie(y, autopct='%1.1f%%', startangle=90, labels = labels)
    ax1.axis('equal') 

    if len(free_text) is not 0:
        add_free_text_to_figure(free_text, ax1)


    apply_figure_config_all(question)
    if n < 1:
        plt.title(question.text + "  (n = "+ str(sum(y)) + " )")


#   ********************************************************************
#    Multiple choice answers as barplot in counts. 
#   *******************************************************************
def plot_multiple_choice_question_heuristics_bar(question, subplot = False, free_text = [], free_text_question = "Freitext:", n = -1):
    answers = question.multiple_choice_answers
    x = answers.columns.values
    y = []
    for nr in range(0, answers.shape[1]):
        ans = answers.iloc[:, nr].values
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



# *************************************************************************************************************************
#****************************** Help functions ****************************************************************************
# *************************************************************************************************************************

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