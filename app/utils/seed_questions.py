from app.database import questions_collection

questions = [
{
"question":"Solve: 2x + 3 = 11",
"options":["3","4","5","6"],
"correct_answer":"4",
"difficulty":0.3,
"topic":"Algebra",
"tags":["linear"]
},
{
"question":"Synonym of 'Aberration'",
"options":["Deviation","Agreement","Truth","Normal"],
"correct_answer":"Deviation",
"difficulty":0.6,
"topic":"Vocabulary",
"tags":["word"]
}
]

questions_collection.insert_many(questions)
print("Questions inserted")