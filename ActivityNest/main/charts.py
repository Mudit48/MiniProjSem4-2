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

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=["#ff9999","#66b3ff","#99ff99","#ffcc99"])
    plt.axis("equal")  

    buffer = BytesIO()
    plt.savefig(buffer, format="png")  # ✅ Save as an image without Tkinter
    plt.close()
    buffer.seek(0)

    return buffer
