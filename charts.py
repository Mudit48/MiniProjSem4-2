import matplotlib
matplotlib.use('Agg')  # ✅ Use a non-GUI backend for Matplotlib

import matplotlib.pyplot as plt
from io import BytesIO
from django.db.models import Count
from .models import Item

def generate_pie_chart():
    department_counts = Item.objects.values("department").annotate(count=Count("department"))

    if not department_counts:
        return None

    labels = [dept["department"] for dept in department_counts]
    sizes = [dept["count"] for dept in department_counts]
    colors = ["#439EA9", "#0A233A", "#7FC8D1", "#A3D9D9"]
    fig, ax = plt.subplots(figsize=(7, 7), facecolor='#F8FBFE')  # Light background
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        wedgeprops={"edgecolor": "white", "linewidth": 2, "antialiased": True},  # ✅ Smooth edges
        textprops={"fontsize": 14, "color": "#0A233A", "fontweight": "bold"}  # ✅ Readable labels
    )
    '''
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=["#ff9999","#66b3ff","#99ff99","#ffcc99"])
    plt.axis("equal")
    for w in wedges:
        w.set_path_effects([matplotlib.patheffects.withSimplePatchShadow()])
    
    ax.set_title("Department Contribution", fontsize=16, fontweight="bold", color="#0A233A")'
    '''
    buffer = BytesIO()
    plt.savefig(buffer, format="png",)  # ✅ Save as an image without Tkinter
    plt.close()
    buffer.seek(0)

    return buffer
