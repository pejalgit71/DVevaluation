import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Munzner's Nested Model",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Munzner’s Nested Model for Visualization Design")
st.subheader("From a real-world question to an efficient visualization")
st.caption(
    "Teaching app based on the four-layer model described in the course material. "
    "Examples and sample data in this app are illustrative."
)

st.info(
    "Core idea: design and validate a visualization at four connected levels. "
    "A problem at an outer level can undermine decisions made at the inner levels."
)

layers = [
    {
        "number": 1,
        "name": "Domain problem and task",
        "question": "What problem does the user need to solve?",
        "focus": "People, domain vocabulary, goals, and tasks",
        "example": "A lecturer wants to identify courses with unusually high failure rates.",
        "validation": "Confirm the task with lecturers and academic decision-makers.",
        "risk": "Solving the wrong problem or showing metrics that do not answer the user's question.",
    },
    {
        "number": 2,
        "name": "Data and abstraction",
        "question": "Which data, data types, and operations represent the problem?",
        "focus": "Tables, attributes, items, attributes, aggregates, comparisons, and filters",
        "example": "Use student results with course, semester, mark, and pass/fail status; calculate failure rate by course.",
        "validation": "Check data definitions, missing values, aggregation rules, and whether the abstraction supports the task.",
        "risk": "Using an inappropriate metric, grouping, or data representation.",
    },
    {
        "number": 3,
        "name": "Visual encoding and interaction",
        "question": "How should the data be shown and explored?",
        "focus": "Charts, visual channels, layout, selection, filtering, and tooltips",
        "example": "Use a sorted bar chart of failure rates, with semester and course filters.",
        "validation": "Test readability, comparisons, accessibility, and whether users can complete the task.",
        "risk": "A misleading, cluttered, or difficult-to-use chart.",
    },
    {
        "number": 4,
        "name": "Algorithms",
        "question": "How will the visualization be computed efficiently?",
        "focus": "Data processing, aggregation, rendering, responsiveness, and scalability",
        "example": "Group records by course and semester, calculate rates, and update the chart after filtering.",
        "validation": "Test correctness, response time, and performance on realistic data volumes.",
        "risk": "Slow, incorrect, or unscalable calculations and interactions.",
    },
]

tab_overview, tab_layers, tab_demo, tab_quiz = st.tabs(
    ["🏠 Overview", "🧱 Explore the four layers", "📈 Interactive example", "🧠 Knowledge check"]
)

with tab_overview:
    st.header("The model at a glance")
    st.write(
        "Move from understanding the domain problem, to abstracting data and tasks, "
        "to choosing visual encodings and interactions, and finally to implementing "
        "the calculations efficiently."
    )

    # Four connected layers, displayed as a nested sequence.
    fig = go.Figure()
    layer_labels = [
        "1 · Domain problem & task",
        "2 · Data & abstraction",
        "3 · Visual encoding & interaction",
        "4 · Algorithms",
    ]
    descriptions = [
        "Why and for whom?",
        "Which data and operations?",
        "How will people see and explore it?",
        "How will it run correctly and efficiently?",
    ]
    widths = [100, 82, 64, 46]
    for i, (label, desc, width) in enumerate(zip(layer_labels, descriptions, widths)):
        fig.add_trace(
            go.Bar(
                x=[width],
                y=[label],
                orientation="h",
                text=[desc],
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate=f"<b>{label}</b><br>{desc}<extra></extra>",
                showlegend=False,
            )
        )
    fig.update_layout(
        title="Four connected layers (conceptual illustration)",
        xaxis=dict(visible=False, range=[0, 105]),
        yaxis=dict(autorange="reversed", title=None),
        barmode="overlay",
        height=330,
        margin=dict(l=10, r=10, t=60, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "The nested bars are a teaching illustration of the layers—not a quantitative chart "
        "and not a claim that one layer is more important than another."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Why start with the problem?")
        st.write(
            "The domain task determines what information matters. For example, a lecturer "
            "trying to find courses needing support needs a different view from a student "
            "tracking their own marks."
        )
    with c2:
        st.markdown("### Why validate every layer?")
        st.write(
            "A chart may look attractive but still fail if the metric is wrong, the data is "
            "incomplete, the interaction is confusing, or the computation is too slow."
        )

    st.markdown("### A quick example")
    st.code(
        "Domain task: Find courses with high failure rates\n"
        "        ↓\n"
        "Abstraction: Course + semester + pass/fail status; calculate failure rate\n"
        "        ↓\n"
        "Visual design: Sorted bar chart + semester filter + hover details\n"
        "        ↓\n"
        "Algorithm: Filter records → group by course → calculate rate → render chart",
        language="text",
    )

with tab_layers:
    st.header("Explore each layer")
    chosen = st.selectbox(
        "Choose a layer",
        options=layers,
        format_func=lambda item: f"Layer {item['number']}: {item['name']}",
    )
    st.markdown(f"## Layer {chosen['number']}: {chosen['name']}")
    st.markdown(f"**Key question:** {chosen['question']}")
    st.write(f"**Focus:** {chosen['focus']}")
    st.success(f"**Running example:** {chosen['example']}")
    left, right = st.columns(2)
    with left:
        st.markdown("#### How to validate this layer")
        st.write(chosen["validation"])
    with right:
        st.markdown("#### What can go wrong?")
        st.warning(chosen["risk"])

    st.divider()
    st.markdown("### What should you ask?")
    prompts = {
        1: [
            "Who will use the visualization?",
            "What decision or action should it support?",
            "What does success look like to the user?",
        ],
        2: [
            "What are the records and attributes?",
            "Are the values categorical, ordered, temporal, or quantitative?",
            "Which transformations or aggregations are needed?",
        ],
        3: [
            "Which chart makes the comparison easiest?",
            "Which visual channels encode the values?",
            "Which filters, selections, or tooltips help the user?",
        ],
        4: [
            "Are calculations correct and reproducible?",
            "How does performance change as the dataset grows?",
            "Can filtering and chart updates finish quickly enough?",
        ],
    }
    for prompt in prompts[chosen["number"]]:
        st.markdown(f"- {prompt}")

with tab_demo:
    st.header("Interactive example: investigate course failure rates")
    st.write(
        "Explore a small synthetic dataset. Change the semester and failure-rate threshold "
        "to see how the domain task, abstraction, visual design, and computation work together."
    )

    # Synthetic sample records; these are not real student records.
    sample = pd.DataFrame(
        [
            ("Data Visualisation", "Semester 1", 100, 18),
            ("Data Visualisation", "Semester 2", 90, 9),
            ("Web Application", "Semester 1", 110, 22),
            ("Web Application", "Semester 2", 105, 17),
            ("Database Systems", "Semester 1", 95, 8),
            ("Database Systems", "Semester 2", 100, 12),
            ("Programming", "Semester 1", 120, 30),
            ("Programming", "Semester 2", 115, 23),
            ("Computer Ethics", "Semester 1", 85, 5),
            ("Computer Ethics", "Semester 2", 88, 7),
            ("Computer Networks", "Semester 1", 92, 14),
            ("Computer Networks", "Semester 2", 96, 11),
        ],
        columns=["Course", "Semester", "Students", "Failed"],
    )
    sample["Passed"] = sample["Students"] - sample["Failed"]
    sample["Failure rate (%)"] = sample["Failed"] / sample["Students"] * 100

    a, b = st.columns([1, 1])
    with a:
        semesters = st.multiselect(
            "Select semester(s)",
            options=sample["Semester"].unique().tolist(),
            default=sample["Semester"].unique().tolist(),
        )
    with b:
        threshold = st.slider("Highlight courses at or above this failure rate (%)", 0, 40, 15)

    filtered = sample[sample["Semester"].isin(semesters)].copy()
    if filtered.empty:
        st.warning("Select at least one semester to display the chart.")
    else:
        # Pool student counts across selected semesters before computing the rate.
        summary = (
            filtered.groupby("Course", as_index=False)[["Students", "Failed", "Passed"]]
            .sum()
        )
        summary["Failure rate (%)"] = summary["Failed"] / summary["Students"] * 100
        summary["Status"] = summary["Failure rate (%)"].apply(
            lambda value: "At/above threshold" if value >= threshold else "Below threshold"
        )
        summary = summary.sort_values("Failure rate (%)", ascending=False)

        metric1, metric2, metric3 = st.columns(3)
        total_students = int(summary["Students"].sum())
        total_failed = int(summary["Failed"].sum())
        overall_rate = total_failed / total_students * 100 if total_students else 0
        metric1.metric("Students in selected data", f"{total_students:,}")
        metric2.metric("Students who failed", f"{total_failed:,}")
        metric3.metric("Overall failure rate", f"{overall_rate:.1f}%")

        fig2 = px.bar(
            summary,
            x="Course",
            y="Failure rate (%)",
            color="Status",
            hover_data={
                "Students": True,
                "Failed": True,
                "Passed": True,
                "Failure rate (%)": ":.1f",
                "Status": False,
            },
            title="Failure rate by course",
            labels={"Course": "Course", "Failure rate (%)": "Failure rate (%)"},
        )
        fig2.add_hline(
            y=threshold,
            line_dash="dash",
            annotation_text=f"Threshold: {threshold}%",
            annotation_position="top left",
        )
        fig2.update_layout(xaxis_tickangle=-25, height=480, legend_title_text="Threshold status")
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Data behind the chart")
        display = summary.copy()
        display["Failure rate (%)"] = display["Failure rate (%)"].round(1)
        st.dataframe(display, use_container_width=True, hide_index=True)

        above = summary[summary["Failure rate (%)"] >= threshold]
        if above.empty:
            st.success("No course meets or exceeds the selected threshold.")
        else:
            st.warning(
                "Courses to investigate: "
                + ", ".join(above["Course"].tolist())
                + ". A high rate is a signal for further investigation, not proof of the cause."
            )

    with st.expander("How this demo maps to the four layers"):
        st.markdown(
            """
            1. **Domain problem and task:** identify courses whose failure rates meet a chosen threshold.
            2. **Data and abstraction:** records contain course, semester, student count, and failed count.
               For multiple selected semesters, counts are pooled first; the rate is then recalculated.
            3. **Visual encoding and interaction:** a bar chart supports comparison; the semester selector,
               threshold line, colour category, and hover details support exploration.
            4. **Algorithms:** filter rows, group by course, sum counts, calculate percentages, sort, and render.
            """
        )
    st.caption(
        "All data are synthetic and for teaching only. They must not be interpreted as actual university results."
    )

with tab_quiz:
    st.header("Knowledge check")
    questions = [
        {
            "q": "A lecturer says, 'I need to identify courses where students may need more support.' Which layer should be clarified first?",
            "options": [
                "Layer 1: Domain problem and task",
                "Layer 3: Visual encoding and interaction",
                "Layer 4: Algorithms",
            ],
            "answer": "Layer 1: Domain problem and task",
            "explanation": "First clarify the user, goal, and decision. Then determine the data, visual design, and implementation.",
        },
        {
            "q": "Deciding to calculate failure rate by course and semester is mainly part of which layer?",
            "options": [
                "Layer 1: Domain problem and task",
                "Layer 2: Data and abstraction",
                "Layer 3: Visual encoding and interaction",
            ],
            "answer": "Layer 2: Data and abstraction",
            "explanation": "This specifies the data fields, grouping, and derived measure needed to represent the task.",
        },
        {
            "q": "Choosing a sorted bar chart and adding a semester filter is mainly part of which layer?",
            "options": [
                "Layer 2: Data and abstraction",
                "Layer 3: Visual encoding and interaction",
                "Layer 4: Algorithms",
            ],
            "answer": "Layer 3: Visual encoding and interaction",
            "explanation": "This layer determines how information is visually represented and how users explore it.",
        },
        {
            "q": "Optimising the group-by calculation so the chart updates quickly is mainly part of which layer?",
            "options": [
                "Layer 1: Domain problem and task",
                "Layer 3: Visual encoding and interaction",
                "Layer 4: Algorithms",
            ],
            "answer": "Layer 4: Algorithms",
            "explanation": "This layer concerns the computational methods used to execute the visualization efficiently.",
        },
        {
            "q": "A chart looks attractive, but it uses the wrong definition of 'failure rate'. What does this demonstrate?",
            "options": [
                "Visual appearance is enough to validate a visualization",
                "A problem in an earlier layer can undermine the final visualization",
                "Algorithms do not affect visualization quality",
            ],
            "answer": "A problem in an earlier layer can undermine the final visualization",
            "explanation": "Visual quality cannot repair an incorrect domain interpretation or data abstraction.",
        },
    ]

    with st.form("quiz_form"):
        responses = {}
        for i, item in enumerate(questions, start=1):
            st.markdown(f"**{i}. {item['q']}**")
            responses[i] = st.radio(
                "Choose one answer:",
                item["options"],
                key=f"question_{i}",
                index=None,
                label_visibility="collapsed",
            )
        submitted = st.form_submit_button("Check my answers")

    if submitted:
        score = 0
        for i, item in enumerate(questions, start=1):
            if responses[i] == item["answer"]:
                score += 1
                st.success(f"Question {i}: Correct. {item['explanation']}")
            else:
                st.error(
                    f"Question {i}: Correct answer: **{item['answer']}**. {item['explanation']}"
                )
        st.metric("Your score", f"{score} / {len(questions)}")
        if score == len(questions):
            st.balloons()
            st.success("Excellent—you understand the four layers and why each needs validation.")
        elif score >= 3:
            st.info("Good progress. Review the layer descriptions and try again.")
        else:
            st.info("Review the four layers in the Explore tab, then try again.")

st.divider()
st.markdown("### Summary")
st.markdown(
    """
    - **Layer 1 — Domain problem and task:** understand the user's goal.
    - **Layer 2 — Data and abstraction:** choose appropriate data representations and operations.
    - **Layer 3 — Visual encoding and interaction:** decide how people see and explore the information.
    - **Layer 4 — Algorithms:** compute and update the visualization correctly and efficiently.

    **Remember:** validate the visualization at every layer, not only by judging the final chart.
    """
)
st.caption(
    "Conceptual teaching aid. Refer to Tamara Munzner's original work for the full model and terminology."
)
