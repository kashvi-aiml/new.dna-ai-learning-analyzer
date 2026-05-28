from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


# LOAD DATASETS

habits_df = pd.read_csv(
    "datasets/student_habits_performance.csv"
)

study_df = pd.read_csv(
    "datasets/student_study_habits.csv"
)

# HOME PAGE

@app.route('/')
def home():

    return render_template("index.html")

# ANALYSIS PAGE

@app.route('/analysis')
def analysis():

    return render_template("analysis.html")

# ANALYZE STUDENT DATA

@app.route('/analyze', methods=['POST'])
def analyze():

    # USER INPUTS
    
    study_hours = float(request.form['study_hours'])

    sleep_hours = float(request.form['sleep_hours'])

    social_media = float(request.form['social_media'])

    attendance = float(request.form['attendance'])

    # Input Validation

    if study_hours < 0 or study_hours > 24:
        return "Study hours must be between 0 and 24."

    if sleep_hours < 0 or sleep_hours > 24:
        return "Sleep hours must be between 0 and 24."

    if social_media < 0 or social_media > 24:
        return "Social media usage must be between 0 and 24."

    if attendance < 0 or attendance > 100:
        return "Attendance percentage must be between 0 and 100."

    # DATASET PATTERN REFERENCES

    avg_study = habits_df[
        'study_hours_per_day'
    ].mean()

    avg_sleep = habits_df[
        'sleep_hours'
    ].mean()

    avg_social = habits_df[
        'social_media_hours'
    ].mean()

    avg_attendance = habits_df[
        'attendance_percentage'
    ].mean()


    # ==========================================
    # BEHAVIORAL SCORING
    # ==========================================

    focus_score = int(

        (
            (study_hours / avg_study) * 45
        )

        +

        (
            (attendance / avg_attendance) * 35
        )

        +

        (
            ((avg_social / social_media)
            if social_media > 0 else 1) * 20
        )

    )


    wellness_score = int(

        (
            (sleep_hours / avg_sleep) * 70
        )

        +

        (
            (attendance / avg_attendance) * 30
        )

    )


    consistency_score = int(

        (
            (attendance / avg_attendance) * 60
        )

        +

        (
            (study_hours / avg_study) * 40
        )

    )


    # LIMIT VALUES

    focus_score = min(max(focus_score, 0), 100)

    wellness_score = min(max(wellness_score, 0), 100)

    consistency_score = min(max(consistency_score, 0), 100)

    # OVERALL LEARNING PROFILE

    overall_score = int(

        (
            focus_score +
            wellness_score +
            consistency_score
        ) / 3

    )

    # LEARNING PROFILE GENERATION

    if overall_score >= 85:

        performance_level = (
            "Highly Structured Learning Profile"
        )

    elif overall_score >= 70:

        performance_level = (
            "Balanced Productivity Profile"
        )

    elif overall_score >= 55:

        performance_level = (
            "Moderately Consistent Learning Profile"
        )

    else:

        performance_level = (
            "Developing Academic Stability Profile"
        )

    # CONTEXTUAL AI INSIGHTS

    recommendations = []


    # FOCUS INTERPRETATION

    if focus_score >= 80:

        recommendations.append(

            "Your current routine reflects strong concentration stability and sustained learning engagement."

        )

    elif focus_score >= 60:

        recommendations.append(

            "Your productivity pattern appears balanced, though occasional distractions may affect deeper focus sessions."

        )

    else:

        recommendations.append(

            "Your current workflow may be fragmenting concentration, reducing long-duration focus efficiency."

        )


    # WELLNESS INTERPRETATION

    if wellness_score >= 80:

        recommendations.append(

            "Your recovery and wellness balance appear supportive of consistent cognitive performance."

        )

    elif wellness_score >= 60:

        recommendations.append(

            "Your mental recovery pattern appears moderately stable, though energy consistency may fluctuate during intensive study periods."

        )

    else:

        recommendations.append(

            "Irregular recovery patterns may be affecting concentration, motivation, and sustained productivity."

        )


    # CONSISTENCY INTERPRETATION

    if consistency_score >= 80:

        recommendations.append(

            "Your academic engagement reflects disciplined participation and structured learning consistency."

        )

    elif consistency_score >= 60:

        recommendations.append(

            "Your learning consistency appears stable overall, though routine optimization may improve long-term efficiency."

        )

    else:

        recommendations.append(

            "Inconsistent academic engagement patterns may be limiting structured progress and retention quality."

        )

    # ADAPTIVE STUDY STRATEGY

    study_plan = []


    if focus_score < 65:

        study_plan.append(
            "Short deep-focus study cycles"
        )

        study_plan.append(
            "Reduced multitasking environments"
        )


    if wellness_score < 65:

        study_plan.append(
            "Structured recovery and sleep stabilization"
        )

        study_plan.append(
            "Balanced study-break intervals"
        )


    if consistency_score < 65:

        study_plan.append(
            "Daily academic tracking routine"
        )

        study_plan.append(
            "Fixed revision scheduling"
        )


    if overall_score >= 75:

        study_plan.append(
            "Advanced concept application sessions"
        )

        study_plan.append(
            "Project-based learning practice"
        )


    # FALLBACK

    if len(study_plan) == 0:

        study_plan.append(
            "Maintain current balanced learning routine"
        )

    # MATCHED STUDENT PATTERNS

    similar_students = habits_df[

        (habits_df['study_hours_per_day']
         >= study_hours - 1)

        &

        (habits_df['study_hours_per_day']
         <= study_hours + 1)

    ]

    similar_count = len(similar_students)

    # RENDER RESULTS

    return render_template(

        "results.html",

        focus_score=focus_score,

        wellness_score=wellness_score,

        consistency_score=consistency_score,

        overall_score=overall_score,

        performance_level=performance_level,

        recommendations=recommendations,

        study_plan=study_plan,

        similar_count=similar_count
    )

# RUN APPLICATION

if __name__ == "__main__":

    app.run(debug=True)