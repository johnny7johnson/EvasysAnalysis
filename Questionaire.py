from sklearn import preprocessing
    

class Question:

    def __init__(self, text="", multiple_choice = False, m_c_answers = [], s_c_answers = [], t_answer = "", answer_range_start = 0, answer_range_end = 0):
       # mc answers should be saved best as pandas dataframe
        self.text = text;
        self.is_multiple_choice = multiple_choice
        self.multiple_choice_answers = m_c_answers
        self.single_choice_answers = s_c_answers
        self.text_answer = t_answer

        self.answer_range_start = answer_range_start;
        self.answer_range_end = answer_range_end;

    def normalize_answers(self):
        if self.is_multiple_choice is True:
            for x in range(0, len(self.multiple_choice_answers)-1):
                self.multiple_choice_answers[:,x] = preprocessing.normalize(self.multiple_choice_answers[:,x])
        elif len(self.single_choice_answers) > 0:
            self.single_choice_answers = preprocessing.normalize([self.single_choice_answers])
        else:
            return self
        return self



class Category:
    def __init__(self, questions = []):
        self.questions = questions

    def get_questions(self):
        return self.questions    




class Questionaire:
    
    def __init__(self, categories = [], start_category = 3, start_question_in_cat = 1):
        self.all_data = []
        self.categories = categories
        self.start_category = start_category
        self.start_question = start_question_in_cat

    def get_categories(self):
        return self.categories


    #map indices of questions in questionaire to indices in quesitons array
    def get_question_by_questionaire_nr(self, categoryNr, questionNr):
        return self.categories[categoryNr - self.start_category].questions[questionNr - self.start_question]

    def normalize_question_answers_by_questionaire_nr(self, categoryNr, questionNr):
        self.categories[categoryNr - self.start_category].questions[questionNr - self.start_question].normalize_answers()
        return True



