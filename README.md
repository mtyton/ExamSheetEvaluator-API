# ExamSheetEvaluator-API
All data necessary to log into user account is in file auths.txt
## How to run it?
 - First Download the repo and unpack
 - Enter directory where you unpacked by terminal/cmd
 - In te same directory create virtual environment
 - Activate environment and install necessary libs which you find in [requirements.txt](https://github.com/mtyton/ExamSheetEvaluator-API/blob/master/requirements)
 - Enter ExamApi directory
 - ```python3 manage.py makemigrations ```
 - ```python3 manage.py migrate ```
 - ```python3 manage.py loaddata fixtures/initial_data.json``` use this to load fixtures
 - now finally you can run ```python3 manage.py runserver```
 
## About project
### Models
```
ExamSheet:
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    ...
Question:
    sheet = models.ForeignKey(ExamSheet, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=200)
    def get_solutions(self): <---returns all solutions for this question
    def get_solutions_for_student(self, examinee):<---returns all solutions from exact user for this question
    ...
Solution:
    examinee = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    to_question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    given_text = models.CharField(max_length=100)
    date = models.DateTimeField(default=now)
    def get_points(self):<---retuns 
    ...
class Point(models.Model):
    answer = models.OneToOneField(Solution, on_delete=models.DO_NOTHING, unique=True)
    points = models.IntegerField()
    ...
class Grade(models.Model):
    sheet = models.ForeignKey(ExamSheet, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    mark = models.IntegerField()

```
The idea is that every student can give answer to every question from every test, later teacher can acces all questions from his test and take all solutions or solutions for just one user, teacher can also assign points to every answer.
Finally Teacher can assing grade for every student for evety exam
### Serializers
I mostly use hyperlinked serializers to make easier geting detail data about obj

### TODO LIST
 - Work on Data Validation
 - Write more serialziers to make this API easier to use
