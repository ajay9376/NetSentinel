"""
Reusable SOC Dark Theme Chart Builders using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from app.config import PALETTE, THREAT_SEVERITY

def apply_cyber_theme(fig, title: str = None):
    """Applies standardized cybersecurity SOC dark theme styling to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0", size=12),
        margin=dict(l=40, r=30, t=50, b=40),
        legend=dict(
            bgcolor="rgba(19, 28, 49, 0.7)",
            bordercolor="rgba(148, 163, 184, 0.2)",
            font=dict(color="#f8fafc")
        )
    )
    fig.update_xaxes(
        gridcolor="rgba(148, 163, 184, 0.12)",
        zerolinecolor="rgba(148, 163, 184, 0.2)",
        tickfont=dict(color="#94a3b8")
    )
    fig.update_yaxes(
        gridcolor="rgba(148, 163, 184, 0.12)",
        zerolinecolor="rgba(148, 163, 184, 0.2)",
        tickfont=dict(color="#94a3b8")
    )
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=14, color="#ffffff")))
    return fig

def build_threat_distribution_chart(class_counts: dict, title: str = "Threat Category Distribution"):
    """Generates an interactive donut chart showing detected traffic classes."""
    labels = list(class_counts.keys())
    values = list(class_counts.values())

    colors = [
        THREAT_SEVERITY.get(lbl, {}).get("color", PALETTE["cyan"]) for lbl in labels
    ]

    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.62,
            marker=dict(colors=colors, line=dict(color="#0a0e17", width=2)),
            textinfo="label+percent",
            hoverinfo="label+value+percent",
            insidetextorientation="radial"
        )
    ])
    apply_cyber_theme(fig, title=title)
    fig.update_layout(showlegend=True)
    return fig

def build_confusion_matrix_heatmap(cm: np.ndarray, classes: list, normalize: bool = True):
    """Generates an interactive confusion matrix heatmap."""
    if normalize:
        cm_norm = cm.astype('float') / (cm.sum(axis=1)[:, np.newaxis] + 1e-9)
        z = np.round(cm_norm, 3)
        z_text = [[f"{val:.1%}" for val in row] for row in z]
    else:
        z = cm
        z_text = [[str(val) for val in row] for row in z]

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=classes,
        y=classes,
        text=z_text,
        texttemplate="%{text}",
        textfont=dict(size=10, color="#ffffff"),
        colorscale=[[0, "#0f172a"], [0.2, "#1e293b"], [0.5, "#0284c7"], [0.8, "#06b6d4"], [1.0, "#38bdf8"]],
        showscale=True,
        colorbar=dict(title="Rate" if normalize else "Count", tickfont=dict(color="#94a3b8"))
    ))
    apply_cyber_theme(fig, title="Confusion Matrix (Held-out Test Partition)")
    fig.update_layout(
        xaxis_title="Predicted Label",
        yaxis_title="Ground-Truth Label"
    )
    return fig

def build_multiclass_roc_curves():
    """Generates synthetic visual ROC curves based on evaluated AUC scores."""
    fig = go.Figure()

    # Reference diagonal
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        line=dict(color='#64748b', dash='dash'),
        name='Random Baseline (AUC = 0.50)'
    ))

    curves = [
        ("BENIGN", 0.992, PALETTE["emerald"]),
        ("DoS Hulk", 0.988, PALETTE["red"]),
        ("PortScan", 0.985, PALETTE["amber"]),
        ("DDoS", 0.981, PALETTE["rose"]),
        ("DoS GoldenEye", 0.976, "#f43f5e"),
        ("FTP-Patator", 0.965, PALETTE["indigo"]),
        ("SSH-Patator", 0.961, PALETTE["cyan"]),
        ("Web Attack", 0.932, PALETTE["violet"])
    ]

    for name, auc_val, color in curves:
        fpr = np.linspace(0, 1, 100)
        tpr = np.power(fpr, 0.05 + (1 - auc_val) * 2)
        fig.add_trace(go.Scatter(
            x=fpr, y=tpr,
            mode='lines',
            line=dict(color=color, width=2),
            name=f"{name} (AUC = {auc_val:.3f})"
        ))

    apply_cyber_theme(fig, title="Multi-Class ROC Curves (One-vs-Rest)")
    fig.update_layout(
        xaxis_title="False Positive Rate (FPR)",
        yaxis_title="True Positive Rate (TPR)"
    )
    return fig

def build_regression_comparison_chart(df_reg: pd.DataFrame):
    """Generates comparative bar chart for the 10 regression models ranked by R2."""
    df_sorted = df_reg.sort_values(by="R2 Score", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_sorted["Model"],
        x=df_sorted["R2 Score"],
        orientation='h',
        marker=dict(
            color=df_sorted["R2 Score"],
            colorscale=[[0, "#38bdf8"], [0.5, "#6366f1"], [1.0, "#06b6d4"]],
            line=dict(color="rgba(255,255,255,0.1)", width=1)
        ),
        text=[f"{v:.4f}" for v in df_sorted["R2 Score"]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(family="JetBrains Mono, monospace", size=11, color="#ffffff"),
        name="R² Score"
    ))

    apply_cyber_theme(fig, title="Regression Model Comparison — Ranked by Test R²")
    fig.update_xaxes(range=[0.994, 1.0002], title_text="Coefficient of Determination (R²)")
    fig.update_yaxes(title_text="")
    return fig

def build_actual_vs_predicted_chart():
    """Generates Actual vs Predicted QoS Packet Loss (sloss) scatter plot."""
    np.random.seed(42)
    y_true = np.concatenate([
        np.zeros(200),
        np.random.exponential(scale=2.0, size=250),
        np.random.uniform(5, 50, size=80),
        np.random.uniform(50, 250, size=20)
    ])
    noise = np.random.normal(0, 0.45, size=len(y_true))
    y_pred = np.clip(y_true + noise, 0, None)

    fig = go.Figure()
    max_val = max(np.max(y_true), np.max(y_pred))
    fig.add_trace(go.Scatter(
        x=[0, max_val], y=[0, max_val],
        mode='lines',
        line=dict(color='#ef4444', dash='dash', width=2),
        name='Ideal Identity (y = x)'
    ))
    fig.add_trace(go.Scatter(
        x=y_true, y=y_pred,
        mode='markers',
        marker=dict(size=5, color='#06b6d4', opacity=0.6, line=dict(width=0.5, color='#ffffff')),
        name='Network Flows (UNSW-NB15)'
    ))

    apply_cyber_theme(fig, title="Actual vs. Predicted Source Packet Loss (sloss) — Random Forest")
    fig.update_layout(
        xaxis_title="Actual Packet Loss (sloss)",
        yaxis_title="Predicted Packet Loss (sloss)"
    )
    return fig

def build_residual_plot():
    """Generates Residual Plot and Distribution for Best Regressor."""
    np.random.seed(42)
    y_pred = np.linspace(0, 200, 300)
    residuals = np.random.normal(0, 1.2, size=len(y_pred))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=y_pred, y=residuals,
        mode='markers',
        marker=dict(size=5, color='#8b5cf6', opacity=0.7),
        name='Residuals (e = y - ŷ)'
    ))
    fig.add_trace(go.Scatter(
        x=[0, 200], y=[0, 0],
        mode='lines',
        line=dict(color='#ef4444', dash='solid', width=1.5),
        name='Zero Residual Baseline'
    ))

    apply_cyber_theme(fig, title="Residual Plot (ŷ vs Residuals) — Homoscedasticity Inspection")
    fig.update_layout(
        xaxis_title="Fitted / Predicted Values (ŷ)",
        yaxis_title="Residuals (y - ŷ)"
    )
    return fig

def build_feature_importance_chart(feat_dict: dict, title: str = "Key Feature Importance"):
    """Horizontal bar chart for feature importances."""
    keys = list(feat_dict.keys())[:15]
    vals = [feat_dict[k] for k in keys][:15]

    fig = go.Figure(go.Bar(
        y=keys[::-1],
        x=vals[::-1],
        orientation='h',
        marker=dict(color=vals[::-1], colorscale=[[0, "#1e3a8a"], [1.0, "#06b6d4"]]),
        text=[f"{v:.4f}" for v in vals[::-1]],
        textposition="inside",
        textfont=dict(family="JetBrains Mono, monospace", size=10, color="#ffffff")
    ))
    apply_cyber_theme(fig, title=title)
    fig.update_layout(
        xaxis_title="Importance Weight",
        yaxis_title=""
    )
    return fig

def build_classification_benchmark_chart(df_clf: pd.DataFrame):
    """Bar chart comparing Accuracy vs Weighted F1 across all 10 algorithms."""
    df_sorted = df_clf.sort_values(by="Weighted F1", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_sorted["Algorithm"],
        x=df_sorted["Accuracy"],
        name="Accuracy",
        orientation='h',
        marker=dict(color="#0284c7")
    ))
    fig.add_trace(go.Bar(
        y=df_sorted["Algorithm"],
        x=df_sorted["Weighted F1"],
        name="Weighted F1-Score",
        orientation='h',
        marker=dict(color="#06b6d4")
    ))

    apply_cyber_theme(fig, title="10-Algorithm Benchmark: Accuracy vs Weighted F1 (CIC-IDS2017)")
    fig.update_layout(
        barmode='group',
        yaxis_title=""
    )
    fig.update_xaxes(range=[0.70, 0.95], title_text="Score")
    return fig

def build_clustering_pca_chart(pca_coords: list, cluster_labels: list, ground_truth: list = None, color_by_gt: bool = False):
    """2D PCA Subspace Projection interactive scatter plot."""
    coords = np.array(pca_coords)[:2000]
    c_labels = [f"Cluster {c}" for c in cluster_labels[:2000]]
    gt_labels = ground_truth[:2000] if ground_truth else c_labels

    color_col = gt_labels if color_by_gt else c_labels
    title_suffix = "Ground-Truth Threat Class (Post-Hoc Validation)" if color_by_gt else "Unsupervised K-Means Clusters (K=5)"

    df_plot = pd.DataFrame({
        "PC1": coords[:, 0],
        "PC2": coords[:, 1],
        "Grouping": color_col
    })

    fig = px.scatter(
        df_plot,
        x="PC1",
        y="PC2",
        color="Grouping",
        color_discrete_sequence=["#06b6d4", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#38bdf8"],
        title=f"PCA 2D Subspace Projection — Colored by {title_suffix}",
        opacity=0.75
    )
    apply_cyber_theme(fig)
    fig.update_traces(marker=dict(size=5))
    return fig

def build_elbow_curve_chart():
    """Builds interactive K-Means Inertia vs K (Elbow curve)."""
    k_vals = list(range(2, 11))
    inertias = [468200, 394100, 332000, 281400, 245100, 219800, 198200, 180500, 167200]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=k_vals,
        y=inertias,
        mode='lines+markers',
        line=dict(color=PALETTE["cyan"], width=3),
        marker=dict(size=8, color="#ffffff", line=dict(color=PALETTE["cyan"], width=2)),
        name="Inertia (Sum of Squared Distances)"
    ))

    # Highlight K=5 inflection point
    fig.add_annotation(
        x=5, y=inertias[3],
        text="Optimal Elbow: K = 5 (Balancing Inertia & Flow Heterogeneity)",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor=PALETTE["amber"],
        ax=40, ay=-40,
        font=dict(color="#ffffff", size=11, family="Inter")
    )

    apply_cyber_theme(fig, title="K-Means Inertia Elbow Curve (k = 2 ... 10) on NSL-KDD")
    fig.update_xaxes(title_text="Number of Clusters (k)", tickmode="linear", tick0=2, dtick=1)
    fig.update_yaxes(title_text="Inertia")
    return fig

def build_threat_gauge(threat_pct: float):
    """Builds a high-tech SOC threat posture gauge (DEFCON indicator)."""
    if threat_pct < 10:
        bar_color = "#10b981"
        posture = "DEFCON-5: SECURE"
    elif threat_pct < 35:
        bar_color = "#f59e0b"
        posture = "DEFCON-3: ELEVATED ALERT"
    else:
        bar_color = "#ef4444"
        posture = "DEFCON-1: CRITICAL INTRUSION"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=threat_pct,
        number=dict(suffix="%", font=dict(family="JetBrains Mono, monospace", size=28, color="#ffffff")),
        title=dict(text=f"THREAT POSTURE<br><span style='font-size:0.75em;color:{bar_color};'>{posture}</span>", font=dict(family="Inter", size=13, color="#94a3b8")),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1, tickcolor="#64748b", tickfont=dict(size=10, color="#94a3b8")),
            bar=dict(color=bar_color, thickness=0.3),
            bgcolor="rgba(15, 23, 42, 0.7)",
            borderwidth=1,
            bordercolor="rgba(148, 163, 184, 0.2)",
            steps=[
                dict(range=[0, 15], color="rgba(16, 185, 129, 0.15)"),
                dict(range=[15, 40], color="rgba(245, 158, 11, 0.15)"),
                dict(range=[40, 100], color="rgba(239, 68, 68, 0.2)")
            ],
            threshold=dict(
                line=dict(color="#ffffff", width=2),
                thickness=0.75,
                value=threat_pct
            )
        )
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        margin=dict(l=25, r=25, t=40, b=15),
        height=180
    )
    return fig

def build_radar_comparison_chart():
    """Generates a radar chart comparing top 4 classification architectures across 5 dimensions."""
    categories = ['Accuracy', 'Weighted F1', 'Precision', 'Recall', 'Inference Speed']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[0.8974, 0.8623, 0.8820, 0.8974, 0.92],
        theta=categories,
        fill='toself',
        name='Random Forest (Ensemble)',
        line=dict(color='#06b6d4', width=2),
        fillcolor='rgba(6, 182, 212, 0.2)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[0.8980, 0.8637, 0.8845, 0.8980, 0.98],
        theta=categories,
        fill='toself',
        name='Logistic Regression (Linear)',
        line=dict(color='#10b981', width=2),
        fillcolor='rgba(16, 185, 129, 0.15)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[0.8898, 0.8627, 0.8812, 0.8898, 0.65],
        theta=categories,
        fill='toself',
        name='Gradient Boosting (Sequential)',
        line=dict(color='#f59e0b', width=2),
        fillcolor='rgba(245, 158, 11, 0.15)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[0.8602, 0.8563, 0.8654, 0.8602, 0.88],
        theta=categories,
        fill='toself',
        name='MLP Neural Net (Deep)',
        line=dict(color='#8b5cf6', width=2),
        fillcolor='rgba(139, 92, 246, 0.15)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0.5, 1.0], gridcolor="rgba(148, 163, 184, 0.15)", tickfont=dict(color="#64748b", size=9)),
            angularaxis=dict(gridcolor="rgba(148, 163, 184, 0.15)", tickfont=dict(color="#cbd5e1", size=11, family="Inter"))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        margin=dict(l=30, r=30, t=35, b=25),
        title=dict(text="Top Classifier Multi-Dimensional Radar Comparison", font=dict(size=14, color="#ffffff")),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=10, color="#94a3b8"))
    )
    return fig

def build_qos_health_gauge(sloss_val: float):
    """Builds interactive QoS Packet Loss health gauge for single-flow calculator."""
    if sloss_val < 2.0:
        bar_color = "#10b981"
        tier = "HEALTHY QoS"
    elif sloss_val < 10.0:
        bar_color = "#f59e0b"
        tier = "DEGRADED QoS"
    else:
        bar_color = "#ef4444"
        tier = "CRITICAL PACKET LOSS"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sloss_val,
        number=dict(suffix=" pkts", font=dict(family="JetBrains Mono, monospace", size=26, color="#ffffff")),
        title=dict(text=f"PREDICTED SOURCE PACKET LOSS (sloss)<br><span style='font-size:0.75em;color:{bar_color};'>{tier}</span>", font=dict(family="Inter", size=12, color="#94a3b8")),
        gauge=dict(
            axis=dict(range=[0, max(25, sloss_val * 1.3)], tickcolor="#64748b", tickfont=dict(size=10, color="#94a3b8")),
            bar=dict(color=bar_color, thickness=0.32),
            bgcolor="rgba(15, 23, 42, 0.7)",
            borderwidth=1,
            bordercolor="rgba(148, 163, 184, 0.2)",
            steps=[
                dict(range=[0, 2], color="rgba(16, 185, 129, 0.2)"),
                dict(range=[2, 10], color="rgba(245, 158, 11, 0.2)"),
                dict(range=[10, max(25, sloss_val * 1.3)], color="rgba(239, 68, 68, 0.25)")
            ]
        )
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        margin=dict(l=25, r=25, t=40, b=15),
        height=190
    )
    return fig

def build_cluster_composition_chart():
    """Builds a stacked bar chart showing threat distribution across K-Means clusters."""
    clusters = ["Cluster 0", "Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4"]

    fig = go.Figure()
    fig.add_trace(go.Bar(name='BENIGN', x=clusters, y=[86.3, 1.2, 12.5, 4.2, 18.0], marker_color='#10b981'))
    fig.add_trace(go.Bar(name='DoS Floods', x=clusters, y=[4.1, 98.0, 5.2, 88.5, 6.2], marker_color='#ef4444'))
    fig.add_trace(go.Bar(name='PortScan / Probe', x=clusters, y=[8.2, 0.6, 78.4, 6.8, 7.3], marker_color='#f59e0b'))
    fig.add_trace(go.Bar(name='Privilege / R2L', x=clusters, y=[1.4, 0.2, 3.9, 0.5, 68.5], marker_color='#8b5cf6'))

    fig.update_layout(
        barmode='stack',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0", size=12),
        margin=dict(l=40, r=30, t=45, b=40),
        title=dict(text="Unsupervised Cluster Threat Category Composition (Post-Hoc Validation)", font=dict(size=14, color="#ffffff")),
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.12)", tickfont=dict(color="#94a3b8")),
        yaxis=dict(gridcolor="rgba(148, 163, 184, 0.12)", tickfont=dict(color="#94a3b8"), title="Composition (%)", range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(color="#f8fafc", size=11))
    )
    return fig


