import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for Matplotlib

import matplotlib.pyplot as plt
from io import BytesIO
from django.db.models import Count
from .models import Item

def generate_pie_chart_year(department):
    year_counts = Item.objects.filter(department=department).values("year").annotate(count=Count("year"))

    if not year_counts:
        return None

    labels = [dept["year"] for dept in year_counts]
    sizes = [dept["count"] for dept in year_counts]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=["#ff9999","#66b3ff","#99ff99","#ffcc99"])
    plt.axis("equal")  

    buffer = BytesIO()
    plt.savefig(buffer, format="png")  # Save as an image without Tkinter
    plt.close()
    buffer.seek(0)

    return buffer